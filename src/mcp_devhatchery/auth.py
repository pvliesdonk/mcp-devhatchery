'''
Authentication middleware and owner context helpers.

M1 supports two modes:
- AUTH_MODE=none   → dev convenience, sets owner='dev'
- AUTH_MODE=bearer → static bearer tokens from TOKENS_JSON

OIDC/OAuth 2.1 will be added in M2.
'''
from __future__ import annotations

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
from .config import settings
import hmac


class OwnerContext:
    '''
    Request-scoped identity carrier used by route handlers and services
    to label containers/volumes/images with an 'owner'.
    '''

    def __init__(self, owner: Optional[str]):
        self.owner = owner


class BearerAuthMiddleware(BaseHTTPMiddleware):
    '''
    Simple Bearer-token auth for M1.

    - Tokens are loaded from settings once at startup.
    - Constant-time comparison avoids timing leaks between candidates.
    - On success, sets request.state.owner to an OwnerContext
      for downstream usage (labels, filtering, etc.).
    '''

    def __init__(self, app):
        super().__init__(app)
        # Cache tokens in-memory at startup. Expected shape: list of dicts with 'id' and 'token'.
        self._tokens = {t.get('id'): t.get('token') for t in settings.tokens()}

    async def dispatch(self, request: Request, call_next):
        # Dev mode: accept unauthenticated requests with a dummy owner.
        if settings.auth_mode == 'none':
            request.state.owner = OwnerContext(owner='dev')
            return await call_next(request)

        # M1 supports only bearer; OIDC comes in M2.
        if settings.auth_mode != 'bearer':
            raise HTTPException(status_code=401, detail='Unsupported auth mode for M1')

        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            raise HTTPException(status_code=401, detail='Missing Bearer token')
        token = auth.split(' ', 1)[1].strip()

        # Constant-time compare across known tokens.
        for owner_id, secret in self._tokens.items():
            if secret and hmac.compare_digest(secret, token):
                request.state.owner = OwnerContext(owner=owner_id)
                return await call_next(request)

        raise HTTPException(status_code=401, detail='Invalid token')

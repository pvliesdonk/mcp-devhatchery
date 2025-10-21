from __future__ import annotations

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
from .config import settings
import hmac, hashlib

class OwnerContext:
    def __init__(self, owner: Optional[str]):
        self.owner = owner

class BearerAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Hash tokens once at startup
        self._tokens = {t.get('id'): t.get('token') for t in settings.tokens()}

    async def dispatch(self, request: Request, call_next):
        # Dev mode: allow unauthenticated when AUTH_MODE=none
        if settings.auth_mode == 'none':
            request.state.owner = OwnerContext(owner='dev')
            return await call_next(request)

        if settings.auth_mode != 'bearer':
            # OIDC will be added in M2
            raise HTTPException(status_code=401, detail='Unsupported auth mode for M1')

        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            raise HTTPException(status_code=401, detail='Missing Bearer token')
        token = auth.split(' ', 1)[1].strip()
        # constant-time compare across known tokens
        for owner_id, secret in self._tokens.items():
            if secret and hmac.compare_digest(secret, token):
                request.state.owner = OwnerContext(owner=owner_id)
                return await call_next(request)
        raise HTTPException(status_code=401, detail='Invalid token')

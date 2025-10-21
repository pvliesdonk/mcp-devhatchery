# ADR-0003: Auth Ladder

**Status:** Proposed

- **Decision:** Modes are mutually exclusive: `none` (dev), `bearer` (static tokens), `oidc` (OAuth 2.1 Auth Code + PKCE via Authelia). **No password grant.**
- **Consequences:** Simple early auth and a clear path to production; standards-compliant.
- **Alternatives:** Basic auth against local db; ROPC (discouraged in OAuth 2.1).

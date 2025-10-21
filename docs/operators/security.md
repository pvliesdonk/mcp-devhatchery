# Security

- Control-plane is the only process that talks to Docker.
- Runners: non-privileged; `cap-drop=ALL`; `no-new-privileges`; resource caps; network off unless enabled.
- Mount Broker: alias-based realpath checks; RO by default; RW explicit per alias; loud audit banner.
- Auth ladder: none → bearer → oidc (Auth Code + PKCE). No password grant.
- Roots restrict default path resolution; out-of-root ops require explicit absolute paths.

# Operator Setup

## Prereqs
- Docker Engine with access for the control-plane container
- GitHub token for CI (optional)

## Run (compose snippet)
```yaml
services:
  devhatchery:
    image: ghcr.io/pvliesdonk/mcp-devhatchery:edge
    env_file: .env
    volumes:
      - devhatchery-exports:/exports
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - 8080:8080
volumes:
  devhatchery-exports: {}
```

> Bind-mounts into runners are controlled by the Mount Broker; see **Operators → Exports** and **Security**.

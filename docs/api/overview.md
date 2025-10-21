# API Overview

The server exposes MCP **Tools**, **Resources**, and respects **Roots**.
- Tools: mutate or perform actions (spawn, exec, write).
- Resources: read-only file content.
- Roots: constrain default scope and listings.

All tool calls return structured errors with `code`, `message`, `hint?`, and `details?`.

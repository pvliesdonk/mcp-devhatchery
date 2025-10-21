# Resources

## resources/list -> [Resource]
Enumerates direct resources under Roots (conservative patterns).

## resources/read(uri) -> bytes
Reads a specific resource, streaming with size caps.

## resources/templates -> [Template]
Advertised patterns: `file:///work/{path}`, `file:///export/{path}` (constrained by Roots).

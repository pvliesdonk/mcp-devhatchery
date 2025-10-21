# Tool: exports

## write({workspace, destination, format, include?, exclude?}) -> {bytes_written, sha256?, path}
Writes to control-plane `EXPORT_ROOT`. Uses atomic rename and optional MANIFEST.

Formats: `tar.zst` (default), `tar.gz`, `tar`, `dir`.

from __future__ import annotations

from pydantic import BaseModel, Field
import os, json

class Settings(BaseModel):
    # Auth
    auth_mode: str = Field(default=os.getenv('AUTH_MODE', 'bearer'))
    tokens_json: str = Field(default=os.getenv('TOKENS_JSON', '[]'))

    # Images / Startup
    default_image: str = Field(default=os.getenv('DEFAULT_IMAGE', 'ubuntu:24.04'))
    prepull_images: str = Field(default=os.getenv('PREPULL_IMAGES', '[\"ubuntu:24.04\"]'))
    warm_pool_map: str = Field(default=os.getenv('WARM_POOL_MAP', '{\"ubuntu:24.04\":1}'))
    idle_timeout_s: int = Field(default=int(os.getenv('IDLE_TIMEOUT_S', '900')))

    # Persistence
    persistent_by_default: bool = Field(default=os.getenv('PERSISTENT_BY_DEFAULT', 'true').lower()=='true')
    apt_cache_persist: bool = Field(default=os.getenv('APT_CACHE_PERSIST', 'false').lower()=='true')

    # Exports
    export_root: str = Field(default=os.getenv('EXPORT_ROOT', '/exports'))

    # Mount broker
    enable_host_bind_mounts: bool = Field(default=os.getenv('ENABLE_HOST_BIND_MOUNTS', 'false').lower()=='true')
    allowed_roots_json: str = Field(default=os.getenv('ALLOWED_ROOTS_JSON', '[]'))

    # Limits
    max_cpu: float = Field(default=float(os.getenv('MAX_CPU', '2.0')))
    max_mem_mb: int = Field(default=int(os.getenv('MAX_MEM_MB', '8192')))
    max_containers_per_owner: int = Field(default=int(os.getenv('MAX_CONTAINERS_PER_OWNER', '6')))

    def tokens(self) -> list[dict]:
        try:
            return json.loads(self.tokens_json)
        except Exception:
            return []

    def allowed_roots(self) -> list[dict]:
        try:
            return json.loads(self.allowed_roots_json)
        except Exception:
            return []

settings = Settings()

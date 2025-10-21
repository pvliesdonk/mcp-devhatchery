from __future__ import annotations

import docker, re, random, string
from typing import Optional, Dict, Any, List

LABEL_APP = 'com.liesdonk.devhatchery.app'
LABEL_OWNER = 'com.liesdonk.devhatchery.owner'
LABEL_WORKSPACE = 'com.liesdonk.devhatchery.workspace'
LABEL_ROLE = 'com.liesdonk.devhatchery.role'

ROLE_RUNNER = 'runner'

_slug_re = re.compile(r'[^a-z0-9-]+')


def _slugify(s: str) -> str:
    s = s.strip().lower().replace(' ', '-')
    s = _slug_re.sub('-', s)
    s = s.strip('-') or 'ws'
    return s[:63]


class DockerBackend:
    def __init__(self) -> None:
        self.client = docker.from_env()

    def volume_name(self, owner: str, workspace: str) -> str:
        return f'devhatchery_ws_{_slugify(owner)}_{_slugify(workspace)}'

    def ensure_volume(self, owner: str, workspace: str):
        name = self.volume_name(owner, workspace)
        try:
            vol = self.client.volumes.get(name)
        except docker.errors.NotFound:
            vol = self.client.volumes.create(name=name, labels={
                LABEL_APP: 'devhatchery',
                LABEL_OWNER: owner,
                LABEL_WORKSPACE: workspace,
            })
        return vol

    def container_name(self, owner: str, workspace: str) -> str:
        short = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        return f'devhatchery_ct_{_slugify(owner)}_{_slugify(workspace)}_{short}'

    def list_containers(self, owner: Optional[str] = None) -> List[Dict[str, Any]]:
        filters = { 'label': [f'{LABEL_APP}=devhatchery', f'{LABEL_ROLE}={ROLE_RUNNER}'] }
        if owner:
            filters['label'].append(f'{LABEL_OWNER}={owner}')
        items = []
        for c in self.client.containers.list(all=False, filters=filters):
            lbl = c.labels or {}
            items.append({
                'id': c.id,
                'name': c.name,
                'image': c.image.tags[0] if c.image.tags else c.image.short_id,
                'workspace': lbl.get(LABEL_WORKSPACE, ''),
                'owner': lbl.get(LABEL_OWNER, ''),
                'created_at': c.attrs.get('Created'),
                'state': c.status,
            })
        return items

    def find_running(self, owner: str, workspace: str, image: str) -> Optional[str]:
        filters = { 'label': [
            f'{LABEL_APP}=devhatchery',
            f'{LABEL_ROLE}={ROLE_RUNNER}',
            f'{LABEL_OWNER}={owner}',
            f'{LABEL_WORKSPACE}={workspace}',
        ]}
        for c in self.client.containers.list(all=False, filters=filters):
            if image in (c.image.tags or []):
                return c.id
        return None

    def attach_or_spawn(self, owner: str, workspace: str, image: str, *,
                        persistent: bool = True, cpu: Optional[float] = None,
                        mem_mb: Optional[int] = None, network: str = 'default') -> Dict[str, Any]:
        cid = self.find_running(owner, workspace, image)
        if cid:
            return { 'container_id': cid, 'status': 'ready' }

        mounts = []
        if persistent:
            vol = self.ensure_volume(owner, workspace)
            mounts = [{ 'Target': '/work', 'Source': vol.name, 'Type': 'volume', 'ReadOnly': False }]

        host_config = self.client.api.create_host_config(
            mounts=mounts,
            mem_limit=f'{mem_mb}m' if mem_mb else None,
            nano_cpus=int(cpu*1e9) if cpu else None,
            network_mode=None if network == 'default' else 'none',
            security_opt=['no-new-privileges'],
            cap_drop=['ALL'],
            read_only=False,
            pids_limit=512,
        )
        labels = {
            LABEL_APP: 'devhatchery',
            LABEL_ROLE: ROLE_RUNNER,
            LABEL_OWNER: owner,
            LABEL_WORKSPACE: workspace,
        }
        name = self.container_name(owner, workspace)
        container = self.client.api.create_container(
            image=image, name=name, labels=labels, host_config=host_config,
            environment={ 'WORKDIR': '/work' }, tty=True, stdin_open=True,
            command=['bash','-lc','while true; do sleep 3600; done'],
        )
        self.client.api.start(container=container.get('Id'))
        return { 'container_id': container.get('Id'), 'status': 'starting' }

    def stop(self, container_id: str) -> None:
        try:
            c = self.client.containers.get(container_id)
            c.stop(timeout=5)
        except docker.errors.NotFound:
            return

    def remove(self, container_id: str) -> None:
        try:
            c = self.client.containers.get(container_id)
            c.remove(force=True)
        except docker.errors.NotFound:
            return

    def snapshot_to_image(self, container_id: str, new_image_tag: str) -> str:
        repo, tag = (new_image_tag.split(':', 1) + ['latest'])[:2]
        img = self.client.api.commit(container=container_id, repository=repo, tag=tag)
        return img.get('Id')

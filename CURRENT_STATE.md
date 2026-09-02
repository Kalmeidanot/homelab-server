# Current State

Last updated: 2026-09-02

## Host

- Hostname: homelab
- Operating system: Ubuntu Server 26.04.1 LTS
- Architecture: x86-64
- Local administrator: kaian
- Remote administration: OpenSSH Server
- Current Ethernet IPv4: 10.0.0.6 via DHCP

## Storage

Internal system disk:

- SK hynix HFS256GEJ9X113N
- Nominal capacity: 256 GB
- Ubuntu reported capacity: about 238.5 GB
- EFI partition: about 1 GB FAT32 mounted at /boot/efi
- Root partition: about 237 GB ext4 mounted at /

External storage:

- WD My Book 12 TB
- Configured with an ext4 filesystem labeled STORAGE
- Mounted read/write at /srv/storage
- Provides bulk storage, including /srv/storage/media

## Services

Currently installed/configured:

- Ubuntu Server
- OpenSSH Server
- Cockpit and cockpit-files
- Samba; authenticated Media share at /srv/storage/media is operational
- Docker Engine 29.7.2 from Docker's official Ubuntu repository
- Docker Compose v5.5.0
- Docker and containerd services are active
- Jellyfin deployed through Docker Compose with host networking
- Codex CLI and bubblewrap administration tooling

Not yet installed:

- Tailscale
- Immich

## Docker

- Docker Engine: 29.7.2
- Docker Compose: v5.5.0
- docker service: active
- containerd service: active
- Docker access currently requires sudo; kaian is not in the docker group
- Installation validation: hello-world completed successfully

## Jellyfin

- Compose definition: ~/nas-admin/compose/jellyfin/compose.yaml
- Image: jellyfin/jellyfin:latest
- Container: jellyfin
- Restart policy: unless-stopped
- Network mode: host
- Browser access: http://10.0.0.6:8096
- Configuration: /srv/jellyfin/config
- Cache: /srv/jellyfin/cache
- Media: /srv/storage/media mounted read-only at /media
- Intel render device: /dev/dri/renderD128
- Supplemental render group GID: 991
- Movies library: /media/movies
- TV library: /media/tv-series
- Initial setup and browser/TV playback testing completed successfully
- Initial metadata/library scan is still being allowed to finish
- Hardware-accelerated transcoding has not yet been formally validated

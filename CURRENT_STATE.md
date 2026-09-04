# Current State

Last updated: 2026-09-04

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
- Tailscale from Tailscale's official Ubuntu 26.04 Resolute repository;
  `tailscaled` is enabled and active
- Docker Engine 29.7.2 from Docker's official Ubuntu repository
- Docker Compose v5.5.0
- Docker and containerd services are active
- Jellyfin deployed through Docker Compose with host networking
- Codex CLI and bubblewrap administration tooling
- Post-deployment reboot validation completed successfully: remote SSH access returned,
  Cockpit and Docker/containerd started automatically, /srv/storage remained available,
  and existing server services remained operational

Not yet installed:

- Immich

## Remote Access

- Tailscale hostname: homelab
- Tailscale IPv4: 100.83.35.13
- Normal home-LAN IPv4 remains 10.0.0.6
- Tailscale is used for private remote access only
- No exit node, subnet router, Tailscale SSH, or Funnel/public exposure is enabled
- Router port forwarding has not intentionally exposed Jellyfin port 8096 publicly
- Off-site Jellyfin access over Tailscale is validated at
  http://100.83.35.13:8096: authentication and video playback both succeeded

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
- Reboot/autostart validation completed successfully: the container started through
  its restart policy and the web interface became available without manual startup
- Initial metadata/library scan is still being allowed to finish
- Hardware acceleration: Intel Quick Sync (QSV) using Intel UHD Graphics 770
- Intel iHD VA-API driver and /dev/dri/renderD128 access validated inside the container
- A real H.264 QSV transcode was successfully validated through forced playback
  transcoding; the Jellyfin FFmpeg log confirmed VA-API initialization, QSV device
  derivation and use of the h264_qsv encoder
- Other codec and tone-mapping transcoding scenarios have not been individually validated

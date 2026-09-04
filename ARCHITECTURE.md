# Server Architecture

## Design principles

Keep the first version simple and understandable.

The server runs Ubuntu Server directly on the hardware.

Applications primarily run through Docker Compose. Docker commands currently use
sudo because the administrator account is not a member of the docker group.

## Internal SSD

The internal SSD is intended for:

- Ubuntu
- Docker Engine
- Docker application configuration
- databases
- Immich PostgreSQL
- Jellyfin configuration and cache
- server-management documentation

## WD My Book 12 TB

The external HDD is configured as an ext4 filesystem labeled STORAGE and mounted
read/write at /srv/storage. It provides bulk data storage such as:

- photos and videos
- movies
- TV
- shared files
- other large personal data

Media is stored below /srv/storage/media and is shared over Samba for authenticated
read/write access. Containers should receive only the access they require; Jellyfin
mounts this media tree read-only at /media.

## Core services

- Docker Engine / Docker Compose: installed and operational
- Samba: installed and operational
- Jellyfin: deployed with Docker Compose and host networking
- Tailscale: installed and operational for private remote access
- Immich: planned

## Remote access

Tailscale is the current safe/default method for remote Jellyfin access. The
server participates as `homelab` with Tailscale IPv4 100.83.35.13 while retaining
its normal home-LAN IPv4 10.0.0.6. Jellyfin is reachable by authenticated devices
on the same tailnet at http://100.83.35.13:8096.

The server is not configured as a Tailscale exit node or subnet router. Tailscale
SSH and Funnel are not enabled, and Jellyfin port 8096 has not intentionally been
published through router port forwarding.

### Low-priority backlog: Universal Jellyfin remote access

Investigate later how to securely access Jellyfin from arbitrary TVs/devices that
cannot run Tailscale, preferably through a normal HTTPS hostname. Compare reverse
proxy, domain, and TLS approaches and their security implications. Tailscale
remains the current safe/default remote-access method.

## Jellyfin

Jellyfin runs from compose/jellyfin/compose.yaml using the official
jellyfin/jellyfin:latest image. Persistent configuration and cache data live on
the internal SSD under /srv/jellyfin. Bulk media remains on the external disk.

The container receives /dev/dri/renderD128 and supplemental group GID 991 for
Intel graphics acceleration. Jellyfin is configured to use Intel Quick Sync
(QSV). The Intel iHD driver, VA-API device access and a real H.264 QSV playback
transcode have been successfully validated. This confirms the hardware path for
that tested scenario; it does not establish that every codec or tone-mapping
scenario has been tested.

## Administration

Primary administration method:

- SSH from the main Windows PC

The Lenovo is intended to operate headless once remote access and reboot recovery have been verified.

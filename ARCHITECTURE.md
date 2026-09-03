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
- Tailscale: planned
- Immich: planned

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

# Server Architecture

## Design principles

Keep the first version simple and understandable.

The server runs Ubuntu Server directly on the hardware.

Applications will primarily run through Docker Compose.

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

The external HDD is intended for bulk data such as:

- photos and videos
- movies
- TV
- shared files
- other large personal data

The exact filesystem and directory structure will be decided before the disk is configured.

## Planned core services

- Docker Engine / Docker Compose
- Samba
- Tailscale
- Immich
- Jellyfin

## Administration

Primary administration method:

- SSH from the main Windows PC

The Lenovo is intended to operate headless once remote access and reboot recovery have been verified.

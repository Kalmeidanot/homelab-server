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
- Immich: deployed with Docker Compose

## Remote access

Tailscale is the current safe/default method for remote Jellyfin and Immich
access. The server participates as `homelab` with Tailscale IPv4 100.83.35.13
while retaining its normal home-LAN IPv4 10.0.0.6. Jellyfin is reachable by
authenticated devices on the same tailnet at http://100.83.35.13:8096.
Immich is reachable by authenticated devices on the same tailnet at
http://100.83.35.13:2283.

The server is not configured as a Tailscale exit node or subnet router. Tailscale
SSH and Funnel are not enabled, and Jellyfin port 8096 has not intentionally been
published through router port forwarding. Immich port 2283 likewise has not been
intentionally exposed directly to the public Internet.

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

## Immich

Immich v3.1.0 runs as a Docker Compose stack from compose/immich. The application
stack consists of the Immich server, machine-learning service, PostgreSQL, and
Valkey. PostgreSQL and Valkey are internal stack dependencies rather than
intentionally exposed user-facing host services.

Persistent data is separated by workload: PostgreSQL data lives on the internal
SSD at /srv/immich/postgres, while large Immich-managed photo/video content,
thumbnails, generated or encoded media, backups, and other upload-location data
live on the WD My Book at /srv/storage/photos/immich. The latter is application-
managed storage and must not be treated as a manually managed Samba photo tree.

The host prerequisite vm.overcommit_memory=1 is persisted in
/etc/sysctl.d/99-immich.conf for Valkey. Immich is available on the LAN at
http://10.0.0.6:2283 and privately off-site through Tailscale at
http://100.83.35.13:2283. Initial functional, remote-access, and reboot/autostart
validation has completed successfully.

### Future evaluation: Lightroom archive

Evaluate a future human-managed Adobe Lightroom archive at
/srv/storage/photos/lightroom, potentially exposed through a separate Samba
Photos share and indexed by Immich as a read-only External Library. This is
future work only: no directory, share, External Library, or archive modification
has been performed. It must remain conceptually separate from Immich-managed
upload storage.

## Administration

Primary administration method:

- SSH from the main Windows PC

The Lenovo is intended to operate headless once remote access and reboot recovery have been verified.

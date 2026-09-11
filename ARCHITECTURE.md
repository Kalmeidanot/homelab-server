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
read/write at /srv/storage and remains permanently connected. It provides bulk
data storage such as:

- photos and videos
- movies
- TV
- shared files
- other large personal data

Storage roles are separate:

- /srv/storage/media: Jellyfin-oriented media storage, exposed through the
  existing authenticated read/write Media Samba share
- /srv/storage/media/movies: active Jellyfin Movies library (/media/movies)
- /srv/storage/media/Pokemon/movies: retained Pokémon feature movies, outside
  the active Movies library path but still within the Media Samba share and
  Jellyfin's read-only /media mount; separate from Pokémon TV content
- /srv/storage/media/disney: retained Disney/Pixar family movies and explicitly
  approved additional titles, outside the active Movies library path; still
  within the Media Samba share and Jellyfin's read-only /media mount
- /srv/storage/photos/immich: Immich-managed application storage that must not
  be manually reorganized
- /srv/storage/archive: human-managed long-term archive, exposed through the
  authenticated read/write Archive Samba share for kaian
- /srv/storage/archive/merged: consolidated human-managed personal archive
- /srv/storage/archive/merged/Bilder og Video: organized photo/video tree intended
  for Immich External Library indexing, separate from Immich-managed uploads

The separate archive-management project completed automated organization using
an intentional year / Norwegian month / event / device hierarchy, preserving
original filenames and meaningful context. Former physical source drives have
been evacuated within the intended scope and are no longer routine dependencies.
Duplikater, Other, Explicitly review-blocked and Unreadable - Damaged are separate
preservation/review categories. The H7 handoff records four optional user-manual
cleanup files remaining; completed organization does not imply every review item
was deleted or every placement uncertainty resolved.

/srv/storage/archive/merged/hidden is USER_MANAGED_EXCLUDED. Automated work must
not enumerate, stat, scan, hash, classify or modify that tree without a new explicit
user authorization naming it.

Start future archive work at /srv/storage/archive/00 - FUTURE AI START HERE.txt.
The long-term management bundle is /srv/storage/archive/Archive.Management;
the active detailed control plane is /home/kaian/media-archive-control. The bundle
contains rules, current decisions, recovery guidance and the durable control
snapshot control-snapshots/final-handoff-20260909T193542Z. It supports continuity
without chat history or the internal SSD, provided the archive disk survives;
it is not a second independent media backup. Read the latest pointers before
future maintenance and never restore intentionally deleted media from old records.

The existing authenticated read/write Samba Archive share continues to expose
/srv/storage/archive for human management. Samba access and Immich container
access are separate controls; no Samba configuration changed during this task.

Containers should receive only the access they require; Jellyfin mounts
/srv/storage/media read-only at /media.

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

### Personal archive External Library

The existing library is indexed at /mnt/archive/bilder-og-video. Its sole archive
bind is intentionally READ-WRITE following explicit user authorization on 2026-09-11:
`/srv/storage/archive/merged/Bilder og Video:/mnt/archive/bilder-og-video:rw`.
Docker RW=true and container rw flags were independently verified. Only Bilder og
Video is mounted; hidden and all sibling categories remain outside Immich's access.

The user may delete external assets through Immich, including their underlying
archive files when trash is emptied. This service capability grants no deletion
permission to AI/Codex. Reconcile later user actions with archive control history;
do not automatically recover intentionally removed originals.

Albums, favorites and application grouping do not reorganize physical year/month/
event folders. External originals stay in the archive; uploads, thumbnails/previews,
encoded playback data, PostgreSQL and model cache retain their existing locations.
No sidecar/XMP-writing, metadata-editing or folder-reorganization setting was changed.
The writable mount itself permits filesystem writes; it is not a deletion-only ACL.

Only immich_server was recreated with its existing image/restart policy. Host
permissions and dependency containers were unchanged. Disposeable/Xenomorph.jpg
was left intact for the user's deletion test; UI deletion remains unverified.
See changes/2026-09-11-immich-external-library-write-access.md for validation and
read-only rollback. The 2026-09-10 read-only deployment record remains historical.

### Future evaluation: Lightroom archive

Evaluate a future human-managed Adobe Lightroom archive at
/srv/storage/photos/lightroom, potentially exposed through a separate Samba
Photos share and indexed by Immich as a read-only External Library. This is
future work only: no Lightroom-specific directory, Photos share, or External
Library has been configured. This proposal is separate from the general-purpose
/srv/storage/archive area and must remain conceptually separate from
Immich-managed upload storage.

## Administration

Primary administration method:

- SSH from the main Windows PC

The Lenovo is intended to operate headless once remote access and reboot recovery have been verified.

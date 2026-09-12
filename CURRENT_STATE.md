# Current State

Last updated: 2026-09-12

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
- Remains permanently connected to the homelab
- /srv/storage/archive is the human-managed bulk archive area
- /srv/storage/archive/merged is the consolidated personal archive root;
  automated organization was completed by the separate archive-management project
- The archive is separate from Jellyfin media at /srv/storage/media and
  Immich-managed storage at /srv/storage/photos/immich

## Services

Currently installed/configured:

- Ubuntu Server
- OpenSSH Server
- Cockpit and cockpit-files
- Samba; authenticated read/write Media share at /srv/storage/media and Archive
  share at /srv/storage/archive are operational
- Tailscale from Tailscale's official Ubuntu 26.04 Resolute repository;
  `tailscaled` is enabled and active
- Docker Engine 29.7.2 from Docker's official Ubuntu repository
- Docker Compose v5.5.0
- Docker and containerd services are active
- Jellyfin deployed through Docker Compose with host networking
- Immich v3.1.0 deployed through Docker Compose; local and Tailscale access,
  uploads, machine learning, and reboot/autostart behavior are validated
- Codex CLI and bubblewrap administration tooling
- Post-deployment reboot validation completed successfully: remote SSH access returned,
  Cockpit and Docker/containerd started automatically, /srv/storage remained available,
  and existing server services remained operational

## Ubuntu Maintenance

- The 2026-09-04 maintenance pass completed successfully, including Docker/containerd
  and Ubuntu kernel/security package updates.
- The server is currently booted into Linux 7.0.0-31-generic.
- Three updates remain deferred by Ubuntu phased updates: libaudit-common, libaudit1,
  and libflashrom1. They were not forced and should roll out normally.
- The separate available firmware update has not been performed.

### Known Cockpit Software Updates issue

- Cockpit itself is operational, but its Software Updates page currently reports
  `Cannot refresh cache whilst offline` even though the server is online and normal
  apt networking and update operations work.
- This appears to be the known Cockpit/PackageKit/NetworkManager false-offline
  behavior on Ubuntu Server. Do not change working server networking solely to fix
  this cosmetic/update-UI issue.
- apt is the authoritative update method until this low-priority issue is revisited.

## Remote Access

- Tailscale hostname: homelab
- Tailscale IPv4: 100.83.35.13
- Normal home-LAN IPv4 remains 10.0.0.6
- Tailscale DNS name: homelab.tail328fad.ts.net
- Tailscale remains the private remote-access path for administration and Immich;
  Jellyfin also has intentional public HTTPS access through Tailscale Funnel
- No exit node, subnet router, or Tailscale SSH is enabled
- LAN Jellyfin access: http://10.0.0.6:8096
- Private Tailscale Jellyfin access remains http://100.83.35.13:8096;
  off-site authentication and video playback over this private path are validated
- Public Tailscale Funnel Jellyfin access: https://homelab.tail328fad.ts.net/
  proxies HTTPS to http://127.0.0.1:8096
- On 2026-09-12, the user enabled Funnel with `sudo tailscale funnel --bg 8096`
  and approved the Tailscale web flow; the CLI confirmed successful configuration
  and background operation. Public HTTPS TV authentication/playback remains
  pending validation; the remote TV has a Jellyfin app but has not yet been tested
- Only Jellyfin is exposed through Funnel; Immich, Cockpit, SSH, Samba and other
  services are not exposed through Funnel. Jellyfin accounts should use strong
  unique passwords because the public endpoint exposes the login surface
- Jellyfin port 8096 was not directly exposed with router port forwarding;
  no router configuration was changed
- Off-site Immich access over Tailscale is validated at
  http://100.83.35.13:2283; Immich remains private, with remote access through
  Tailscale only, and is not exposed through Funnel or direct port forwarding

## Operational Reference

- runbooks/everyday-commands.txt is the canonical everyday command reference for
  routine access, health checks, service checks, and safe restart/shutdown tasks

## Samba Archive Share

- Archive maps to /srv/storage/archive with authenticated read/write access for kaian
- Windows access: `\\homelab\Archive`; IP-path fallback: `\\10.0.0.6\Archive`
- Both /srv/storage/archive and /srv/storage/archive/merged were created with
  owner/group kaian:kaian and directory permissions 0775
- Windows access, visibility of merged, and create/write/rename/delete behavior
  were successfully validated; temporary test items were removed
- Immich indexes only Bilder og Video through its separate, intentionally writable
  External Library bind; sibling categories and hidden are not mounted.

## Personal Media Archive

- Primary archive: /srv/storage/archive/merged; normal organized photos/videos:
  /srv/storage/archive/merged/Bilder og Video
- Intentional hierarchy: year / Norwegian month / meaningful event / device where
  appropriate. Original filenames and useful event/day structure are preserved.
- Additional intentional categories include Duplikater (additional exact copies),
  Other (non-media), Explicitly review-blocked, and Unreadable - Damaged.
- /srv/storage/archive/merged/hidden is USER_MANAGED_EXCLUDED: no automated
  enumeration, stat, scan, hashing, classification, reorganization or modification
  unless the user explicitly authorizes that tree in a future task.
- Former physical source drives were evacuated within the project's intended
  scope; routine organization no longer depends on them.
- Durable future-AI entry: /srv/storage/archive/00 - FUTURE AI START HERE.txt
- Long-term rules, decisions, state and recovery instructions:
  /srv/storage/archive/Archive.Management
- Active detailed control plane: /home/kaian/media-archive-control
- Durable control snapshot: Archive.Management/control-snapshots/
  final-handoff-20260909T193542Z (beneath /srv/storage/archive). This protects
  continuity after chat/internal-SSD loss if the archive disk survives; it is
  not an independent backup of the archive media.
- Evidence basis: the H7 handoff dated 2026-09-09 19:35:42 UTC records completed
  automated organization with four SEQ-515 files pending optional user-manual
  cleanup. That dated exception was not rechecked or acted on in this task.
  Intentional deletions and retained review categories must not be treated as
  failed transfers or automatically recovered.
- See changes/2026-09-10-complete-personal-media-archive.md. Detailed multi-day
  project history remains in Archive.Management rather than this repository.

## Docker

- Docker Engine: 29.7.2
- Docker Compose: v5.5.0
- docker service: active
- containerd service: active
- Docker access currently requires sudo; kaian is not in the docker group
- Installation validation: hello-world completed successfully

## Jellyfin

- Running server/API version verified on 2026-09-07: 10.11.11
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
- 14 approved Pokémon feature-movie folders were moved intact from
  /srv/storage/media/movies to /srv/storage/media/Pokemon/movies on 2026-09-07,
  outside the active Movies library path. Pokémon TV content was not moved;
  Jellyfin configuration and manual library scans were left to the administrator.
- 117 approved Disney/Pixar family and additional user-selected movie folders
  were moved intact from /srv/storage/media/movies to /srv/storage/media/disney
  on 2026-09-07; the latter is outside the configured /media/movies library path
- Jellyfin configuration was not changed and no library scan was manually
  triggered for this move; library refresh is left to the administrator
- TV library: /media/tv-series
- Initial setup and browser/TV playback testing completed successfully
- Reboot/autostart validation completed successfully: the container started through
  its restart policy and the web interface became available without manual startup
- Administrator confirmed a fresh library scan completed after the media moves
- On 2026-09-07, 36 approved empty BoxSets were removed through the supported
  HTTP API after immediate type and recursive-membership checks. All 23 populated
  collections and their membership remained intact; no empty collections remained
  at verification. Media IDs and filesystem metadata were unchanged, and the
  Jellyfin health endpoint reported Healthy. No restart or manual scan was triggered
- Hardware acceleration: Intel Quick Sync (QSV) using Intel UHD Graphics 770
- Intel iHD VA-API driver and /dev/dri/renderD128 access validated inside the container
- A real H.264 QSV transcode was successfully validated through forced playback
  transcoding; the Jellyfin FFmpeg log confirmed VA-API initialization, QSV device
  derivation and use of the h264_qsv encoder
- Other codec and tone-mapping transcoding scenarios have not been individually validated

## Immich

- Version: v3.1.0
- Compose directory: ~/nas-admin/compose/immich
- Compose definition: ~/nas-admin/compose/immich/docker-compose.yml
- Secret environment file: ~/nas-admin/compose/immich/.env (Git-ignored and untracked)
- Containers: immich_server, immich_machine_learning, immich_postgres, and
  immich_redis; all four were confirmed healthy after initial startup
- Browser access: http://10.0.0.6:2283
- Tailscale/off-site access: http://100.83.35.13:2283
- Immich-managed uploads and derived data: /srv/storage/photos/immich on the
  WD My Book; this tree must not be manually edited behind Immich's back
- PostgreSQL data: /srv/immich/postgres on the internal SSD
- External archive mount changed to READ-WRITE and verified on 2026-09-11:
  /srv/storage/archive/merged/Bilder og Video -> /mnt/archive/bilder-og-video.
  Docker reports RW=true and container mount metadata reports rw. Only this
  organized tree is exposed; no whole archive/merged mount or hidden access.
- The user already created/scanned this External Library. User-directed deletion
  through Immich can now remove the underlying file when trash is emptied.
  This does not authorize Codex/AI deletion or change archive organization rules.
- Only immich_server was recreated, without pulling/upgrading images; other
  container IDs, existing mounts, managed uploads, database and restart policies
  were unchanged. All four containers healthy; local HTTP 200; database ready.
- No host permission, XMP/sidecar/metadata setting or folder-organization change.
  The writable filesystem boundary permits writes; no new unrelated app features
  were enabled. Albums/favorites remain application state, not physical moves.
- Disposeable/Xenomorph.jpg remains unchanged for the USER's Immich UI deletion
  test. Capitalization is significant on Linux. No temporary write test was used.
- See changes/2026-09-11-immich-external-library-write-access.md for evidence and
  exact read-only rollback. User UI deletion outcome remains pending.
- External Library originals stay in the human-managed archive; later indexing
  creates derived/application data in the existing Immich storage architecture,
  not another copy of the originals under the upload location.
- PostgreSQL and Valkey are not intentionally exposed as user-facing host services
- Host prerequisite: /etc/sysctl.d/99-immich.conf sets vm.overcommit_memory=1;
  the runtime setting was verified as 1
- Initial/admin account creation, browser and phone uploads, immediate mobile-upload
  visibility, timeline, thumbnails, photo viewing, and machine-learning health were
  successfully validated
- Test data was confirmed under both persistent storage paths. At that point the
  Immich-managed tree used about 266 MB and PostgreSQL used about 312 MB; these
  were initial observations, not expected fixed sizes
- Remote phone access through Tailscale was validated away from the home LAN
- Reboot/autostart validation succeeded: Ubuntu and SSH returned, the Compose stack
  returned automatically, and Immich became available without manual startup

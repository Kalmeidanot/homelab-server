# Current State

Last updated: 2026-09-17

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

- The 2026-09-14 Ubuntu maintenance pass completed successfully, based on
  user-confirmed results. The upgrade simulation showed 9 packages upgrading,
  0 installing, 0 removing, and 0 held back; the real upgrade succeeded.
- Updated packages: containerd.io, dmidecode, docker-buildx-plugin, libaudit-common,
  libaudit1, libflashrom1, mdadm, sos, and tailscale. This includes the three
  packages previously deferred by phased updates on 2026-09-04.
- A reboot was required due to libc6 and completed successfully. The kernel
  remained Linux 7.0.0-31-generic and LAN IPv4 remained 10.0.0.6.
- After reboot, SSH returned; ssh, cockpit.socket, smbd, docker, containerd, and
  tailscaled were active. /srv/storage was mounted read/write from /dev/sda1 as
  ext4. Jellyfin and all four Immich containers were running and healthy.
- The final reboot-required check returned `NO REBOOT REQUIRED`.
- apt reported grub-pc-bin as automatically installed and no longer required;
  `apt autoremove` was NOT run and grub-pc-bin was not removed in this pass.
- Firmware was not attempted during that Ubuntu maintenance pass; the separate
  failed firmware attempt and recovery are recorded below.
- Detailed record: changes/2026-09-14-ubuntu-maintenance-update.md.

### Known Cockpit Software Updates issue

- Cockpit itself is operational, but its Software Updates page currently reports
  `Cannot refresh cache whilst offline` even though the server is online and normal
  apt networking and update operations work.
- This appears to be the known Cockpit/PackageKit/NetworkManager false-offline
  behavior on Ubuntu Server. Do not change working server networking solely to fix
  this cosmetic/update-UI issue.
- apt is the authoritative update method until this low-priority issue is revisited.

## Firmware

- The Lenovo 0.1.52 fwupd/LVFS update attempt FAILED. System Firmware remains
  0.1.47 / BIOS M43KT2FA; 0.1.52 remains available and future updating is pending.
- The attempt caused an extended no-display/no-network boot stall. The server
  recovered after one normal power-button press/restart and is operational,
  based on user-confirmed SSH, Jellyfin, Immich, Samba and disk activity.
- Local console login is not required for SSH or normal server services.
- fwupd retains stale/conflicting reboot/history messages alongside explicit
  failure. These do not establish an active flash or a need for another reboot.
- Do not retry the same fwupd/LVFS capsule path without separate review. Future
  firmware work is a separate deliberate maintenance task, first evaluating
  Lenovo's alternate vendor-supported update/recovery methods. The firmware
  issue remains unresolved.
- Detailed evidence: [failed update and recovery](changes/2026-09-15-failed-lenovo-firmware-update.md).

## Remote Access

- Tailscale hostname: homelab
- Tailscale IPv4: 100.83.35.13
- Normal home-LAN IPv4 remains 10.0.0.6
- Tailscale DNS name: homelab.geep-krait.ts.net; the tailnet DNS suffix was
  renamed by the user on 2026-09-12. Read-only `Self.DNSName` reports
  `homelab.geep-krait.ts.net.`; the machine name remains homelab
- Tailscale remains the private remote-access path for administration and Immich;
  Jellyfin also has intentional public HTTPS access through Tailscale Funnel
- No exit node, subnet router, or Tailscale SSH is enabled
- LAN Jellyfin access: http://10.0.0.6:8096
- Private Tailscale Jellyfin access remains http://100.83.35.13:8096;
  off-site authentication and video playback over this private path are validated
- Public Tailscale Funnel Jellyfin URL: https://homelab.geep-krait.ts.net;
  no :8096 is required. Local proxy target remains http://127.0.0.1:8096
- On 2026-09-12, the user enabled Funnel with `sudo tailscale funnel --bg 8096`
  and approved the Tailscale web flow before the DNS rename. After the rename,
  the user reran the command; the CLI reported the new public hostname and
  successful background operation
- Validation recorded on 2026-09-13 from user-supplied evidence:
  `curl -I https://homelab.geep-krait.ts.net` returned `HTTP/2 302`,
  `location: web/` and `server: Kestrel`. Public DNS resolution, TLS/HTTPS,
  Funnel reachability and Jellyfin response through the new hostname work
- An off-site TV's Jellyfin app successfully connected using the new public
  URL. The TV does not have Tailscale installed. Video playback through this
  new public Funnel path remains unverified
- Funnel status now shows both homelab.geep-krait.ts.net and
  homelab.tail328fad.ts.net as `Funnel on`, proxying to http://127.0.0.1:8096.
  The old hostname is a known stale/legacy entry pending a separate deliberate
  runtime cleanup task; it has not been removed
- Current validation evidence:
  changes/2026-09-13-validate-jellyfin-funnel-after-dns-rename.md.
  The 2026-09-12 rename record preserves the earlier pending state
- Only Jellyfin is exposed through Funnel; Immich, Cockpit, SSH, Samba and other
  services are not exposed through Funnel. Jellyfin accounts should use strong
  unique passwords because the public endpoint exposes the login surface
- Jellyfin port 8096 was not directly exposed with router port forwarding;
  no router configuration was changed
- Off-site Immich access over Tailscale is validated at
  http://100.83.35.13:2283; Tailscale is the intended private remote-access path.
  Immich is not exposed through Funnel or direct router port forwarding, but
  its Docker-published port still needs exposure hardening (see Host Firewall).

## Host Firewall

- UFW is active and enabled on system startup, with default incoming deny and
  outgoing allow. LAN source 10.0.0.0/24 is allowed TCP ports 22 (SSH), 9090
  (Cockpit), 445 (Samba), 8096 (Jellyfin), and 2283 (Immich).
- All inbound traffic on tailscale0 and UDP port 41641 for Tailscale direct
  connections are allowed. Fresh Windows SSH to 10.0.0.6 and LAN access worked;
  Jellyfin and Immich were reachable from a Tailscale-connected device.
- Immich remains Docker-published on 0.0.0.0:2283 and [::]:2283. Docker-published
  ports may bypass normal UFW INPUT filtering; UFW alone does not establish
  protection of port 2283. Immich/Tailscale exposure hardening remains pending.
- SSH hardening is incomplete: PasswordAuthentication was still enabled during
  the audit.
- User-supplied completion evidence: [UFW activation](changes/2026-09-17-enable-ufw-firewall.md).

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

## Samba Recycle Protection

- Media (/srv/storage/media) and Archive (/srv/storage/archive) recycle protection
  is active and tested through Windows SMB deletion, using .recycle/%U within
  each share. A fresh client connection was required for Media after smbd reload.
- Both .recycle roots and their kaian subdirectories were verified mode 700,
  kaian:kaian. Test artifacts were removed; both roots remain present at mode 700,
  kaian:kaian and must be preserved.
- This is same-disk protection on the WD My Book, not backup. It covers SMB
  deletes, not direct Linux or application/container deletes (including Immich),
  disk failure, corruption, disk loss, or sufficiently privileged malicious access.
  Recycled files continue consuming space until deliberately removed; deletion
  inside .recycle is not recursively recycled.
- User-supplied tests and configuration: [Samba recycle](changes/2026-09-17-enable-samba-recycle-bin.md).

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

- Running server/API version verified read-only on 2026-09-13: 10.11.11
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
- SmartLists 12.0.1.0 is installed as an optional third-party Jellyfin plugin,
  manually installed by the user through Jellyfin's plugin UI after adding its
  repository. Codex verified plugin presence and successful startup/load read-only
  on 2026-09-13; metadata reports Active and target ABI 10.11.0
- SmartLists project: https://github.com/jyourstone/jellyfin-smartlists-plugin
- Repository manifest:
  https://raw.githubusercontent.com/jyourstone/jellyfin-plugin-manifest/main/manifest.json
- Purpose: dynamic/rule-based Jellyfin collections and playlists, including
  external-list integration. No particular external provider has been tested
  as part of this validation
- Plugin directory: /srv/jellyfin/config/plugins/SmartLists_12.0.1.0
- No SmartLists were created or configured, and no collections or playlists were
  created by Codex in this documentation task. The observed startup auto-refresh
  cache contained 0 playlists and 0 collections; this is a startup observation,
  not a comprehensive audit of current Jellyfin objects
- Jellyfin health returned Healthy. No SmartLists compatibility/startup errors
  were found in the latest startup log inspected; optional Plugin Pages is absent.
  Startup warnings and validation scope are recorded in
  changes/2026-09-13-install-jellyfin-smartlists.md

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

## PokemonReleaseMonitor

- Application: /home/kaian/apps/PokemonReleaseMonitor, clean main at
  e3df485f8fb77221cb4f4b916646a188e138c5fb; feature/main pushed to verified origin.
- Node v24.21.0 / npm 11.19.0 under ~/.local/opt; node/npm/npx symlinks under
  ~/.local/bin. npm ci, lint, typecheck, 117 fixture tests and build passed.
- Notification-only monitoring of Pokemon TCG: 30th Celebration. 60 stores
  researched, 27 enabled and 33 deferred; full list and reasons in app docs/STORES.md.
  Priority stores Cardcenter, Outland, Pokestore, Collectible and Ringo enabled;
  ARK, Norli and Extra Leker await reliable discovery/online-stock parsing.
- Production snapshot: 123 relevant products; Cardcenter 22 preserved. IndigoTCG
  reports two available products (placeholder prices/unspecified language),
  LittleM six and Kortbakeren seven open preorders. Initial per-store baselines
  are silent; zero product notifications at post-deployment verification.
- Polling targets 90 +/- 15 seconds between starts per store, staggered across
  stores, maximum three concurrent jobs with sequential HTTP inside each job.
  Errors/backoff are isolated per store. No browser or purchasing functionality.
- Runtime: /home/kaian/.local/share/pokemon-release-monitor (700 kaian:kaian),
  SQLite schema 2, per-store last-poll snapshots and logs/monitor.log (600).
  Transactional migration preserved original Cardcenter records/history/baseline;
  integrity and foreign-key checks passed. Fresh pre-migration backup:
  backups/pre-multistore-deploy-20260917T203625Z.sqlite under runtime.
- Environment: /home/kaian/.config/pokemon-release-monitor/env, 600 kaian:kaian;
  both Pushover keys non-empty and outside Git. Product events use priority 1;
  normal test uses 0; emergency priority 2 is never used. Exactly one homelab
  HIGH test accepted HTTP 200 / API status 1 / priority 1 at 20:22:35 UTC.
  iPhone reception/presentation requires the user's own confirmation.
- pokemon-release-monitor.service enabled and active as kaian, restarted for
  deployment at 2026-09-17 22:36:27 CEST. Absolute Node path, built CLI,
  private umask, restart-on-failure and network-online.target unchanged.
  All 27 stores completed at least three successful polls; no errors, 403/429,
  crash loop or duplicate/bootstrap pushes. NRestarts=0. No reboot performed.
- Initial resource observation: about 301 MiB service RAM, 314 MiB peak,
  5.3% of one CPU core average, 8.9 MiB SQLite plus WAL, 475 KiB logs.
- Production per-store status: /home/kaian/.local/bin/pokemon-monitor.
- Latest record, validation and schema-aware rollback:
  changes/2026-09-17-pokemon-multistore-high-priority.md.
  Initial installation: changes/2026-09-17-pokemon-release-monitor-deployment.md.

### PokemonReleaseMonitor store wave in observation (2026-09-21)

- Production switched to 371e7be at 18:10:18 UTC, five new stores imported silently.
- Final reviewed app 9cc913ac8860cd4c0dd6d1451f4cc979a972c354 is pushed to main;
  follow-up exact deployment fixes measured fixed-order scheduler starvation.
- Norli, Extra Leker, Cardstore, MaxGaming Norway, LABOGE passed 142 tests/live
  checks; 32 stores enabled. ARK remains deferred. No notifier/schema change.
- Exact deployment, observation and rollback:
  changes/2026-09-21-pokemon-store-wave2.md; script scripts/pokemon-monitor-deploy-wave2.

# Add Immich Read-Only Archive External Library Mount

Date: 2026-09-10

Status: Applied and verified; administrator UI library creation/first scan pending

## Reason

Allow Immich to visually index the existing human-managed personal archive
without duplicating original media into its managed upload storage. The archive
consolidation is documented separately in
[the archive catch-up record](2026-09-10-complete-personal-media-archive.md).

## Existing deployment

- Compose directory: /home/kaian/nas-admin/compose/immich
- Compose definition: docker-compose.yml; Compose project: immich
- Server service/container: immich-server / immich_server
- Server image, confirmed live: ghcr.io/immich-app/immich-server:v3.1.0
- Machine-learning service/container: immich-machine-learning / immich_machine_learning
- Machine-learning image: ghcr.io/immich-app/immich-machine-learning:v3.1.0
- Database service/container: database / immich_postgres
- PostgreSQL image: ghcr.io/immich-app/postgres:14-vectorchord0.4.3-pgvectors0.2.0,
  pinned to the existing SHA-256 digest in Compose
- Valkey service/container: redis / immich_redis; docker.io/valkey/valkey:9,
  pinned to the existing SHA-256 digest in Compose
- Existing server mounts: /srv/storage/photos/immich -> /data (read/write),
  /etc/localtime -> /etc/localtime (read-only)
- Database bind: /srv/immich/postgres -> /var/lib/postgresql/data
- Machine-learning cache: existing immich_model-cache named volume -> /cache
- Private .env: Git-ignored, untracked, kaian:kaian mode 0600; unchanged
- Existing port: 2283:2283; restart policies remain always

Before editing, non-privileged `docker compose config --quiet` passed. The local
web root returned HTTP 200 and /api/server/version reported 3.1.0. Initial live
Docker inspection was blocked because sudo required interactive authentication
and kaian could not access /var/run/docker.sock. The administrator subsequently
ran the prepared bounded apply-and-verify script with sudo in their authenticated
terminal. Its root-owned sanitized report confirms all four containers healthy
before application, with the Compose paths, images and existing mounts above.
No sudo policy, group membership or Docker socket permissions were changed.

## Configuration and rollback point

The working tree was clean before this task. Pre-change Git revision:
`5b8cfaa09c20a91f7e3af96b845e56be1fc4a629`. Its tracked Compose definition is the
configuration rollback point; no secret environment file was copied into Git.

Exactly one volume line was added under immich-server:

```yaml
      - '/srv/storage/archive/merged/Bilder og Video:/mnt/archive/bilder-og-video:ro'
```

Host source: `/srv/storage/archive/merged/Bilder og Video`.
Container destination: `/mnt/archive/bilder-og-video`.
Mode: **read-only**. The container path avoids spaces; the host path is unchanged.

Only Bilder og Video is exposed through this archive bind. Its siblings hidden,
Duplikater, Other, Explicitly review-blocked and Unreadable - Damaged are outside
the source path. The whole merged root is not mounted. No exclusions need to be
created to obtain this mount boundary, and none were configured in Immich.

## Application and validation

Post-edit Compose validation passed. An in-memory comparison of fully resolved
pre/post Compose configuration confirmed exactly one new bind, with the required
source, destination and `read_only: true`; all other resolved settings matched.
Expanded environment values were neither printed nor saved.

The administrator executed `/tmp/nas-admin-immich-apply-verify.py` using sudo.
The script performed validation and application from the existing Compose
directory, equivalent to:

```sh
cd /home/kaian/nas-admin/compose/immich
sudo docker compose config --quiet
# Only after validation and live prechecks succeeded:
sudo docker compose up -d --pull never
```

Evidence source: `/tmp/nas-admin-immich-live-validation.json`, root:root mode
0644, completed **2026-09-10 09:57:47 UTC**, with `success: true`,
`compose_valid: true` and `applied: true`. The report was read to finalize this
record; deployment was not repeated. The temporary script/report are not durable
recovery dependencies; the important commands and results are preserved here.

The script verified archive filesystem identity, exact resolved Compose scope,
live deployment paths and images, and existing local image IDs before applying.
All four containers were running and healthy before and after:

| Service | Container | Application result |
|---|---|---|
| immich-server | immich_server | Recreated; healthy |
| immich-machine-learning | immich_machine_learning | Same container; healthy |
| database | immich_postgres | Same container; healthy |
| redis (Valkey) | immich_redis | Same container; healthy |

Server container ID changed from `da5606d7f23e` to `f22080029d00`. All image IDs
and existing mounts remained unchanged; dependency container IDs were unchanged.
The local web root returned HTTP 200 before and after; /api/server/version
reported 3.1.0 after application. No image was upgraded or pulled.

Docker inspection confirmed:

```text
Type: bind
Source: /srv/storage/archive/merged/Bilder og Video
Destination: /mnt/archive/bilder-og-video
Mode: ro
RW: false
Propagation: rprivate
```

Inside immich_server, `/proc/self/mountinfo` independently reported the selected
mount at /mnt/archive/bilder-og-video with mount options `ro,relatime`.
The underlying ext4 filesystem remains read/write on the host; its `rw`
superblock flag does not make the container's read-only bind writable.

`test -d`, `test -r` and `test -x` succeeded for the container path, followed by
only `ls -1` of that directory. The 20 top-level year entries were 2004, 2005,
2007, 2008, 2009 and 2011 through 2025. No recursive listing, media-content read,
hashing, archive test-file creation or write attempt was performed.

The mount is ready for administrator UI setup. No External Library was created,
no archive scan/import was started, and original deletion remains disabled.

Final repository verification passed: complete diff review, `git diff --check`,
an exact six-file scope check, and secret-value/pattern checks. The Compose diff
contains only the bind line; .env remains ignored and untracked. No archive
payload, control database, temporary helper/report or generated media is included
in the commit. The local web root was checked again and returned HTTP 200.

## Intended user workflow and staged rollout

The administrator will use Administration -> External Libraries -> Create
Library, select the owner, then Add Folder (Add in the Folders section), entering:

```text
/mnt/archive/bilder-og-video
```

With the server mount verified, the user performs the first Scan / Scan New
Library Files and monitors Administration -> Jobs. This task does not create the
library, start a scan/import, configure exclusions or alter account settings.
The supported setup workflow is described in the
[official External Library guide](https://docs.immich.app/guides/external-library/).

Phase 1 remains read-only while the user validates indexing, timestamps/dates,
thumbnails, photo viewing, video playback, and Canon R6 playback/transcoding.
These are first-scan acceptance checks, not results of this server-side task.

The intended visual layer includes timeline/search, face recognition, maps where
metadata exists, albums, favorites and easy visual review. Albums/favorites and
Immich grouping do not reorganize the physical year/month/event/device hierarchy.
Originals stay at the host source: External Library indexing does not copy them
into Immich-managed upload/library storage. Thumbnails, previews, potentially
encoded/transcoded videos, database/ML records and model cache remain within the
existing application storage architecture; no derived-data paths move here.

The user may enable Account Settings -> Features -> Folders to browse the physical
hierarchy alongside the timeline; see the
[official Folder View documentation](https://docs.immich.app/features/folder-view/).

Phase 2 requires separate user approval and a documented Compose change to this
specific bind before removing `:ro`. With appropriate write permissions/settings,
Immich may write XMP sidecars and delete archive originals when trash is emptied.
No archive write/delete capability is enabled in this phase. The read-only flag's
role is documented in [External Libraries](https://docs.immich.app/features/libraries/).

## Affected files, storage and services

- compose/immich/docker-compose.yml: one server bind added
- CURRENT_STATE.md and ARCHITECTURE.md: archive/Immich relationship and phase status
- runbooks/everyday-commands.txt: UI path, read-only checks and archive pointers
- This change record and the separate archive catch-up record
- Applied runtime change: immich_server recreation, accessing the existing
  WD My Book archive filesystem read-only
- Existing uploads, database storage, machine-learning cache, dependency services,
  port bindings and restart policies retain their configuration

## Safety and rollback

No archive payload was modified, moved, deleted or copied into Immich. No hidden
tree access, archive control changes, manual PostgreSQL operations, Immich reset,
reinstall, upgrade, volume deletion, network/SSH/firewall change, Samba change,
Tailscale change or Jellyfin change was performed. Secrets and .env remain outside
Git. No recursive media scan/hash or real-file write test was performed.

To roll back this mount, remove only the added bind line, preserving later unrelated
changes. From /home/kaian/nas-admin/compose/immich run:

```sh
sudo docker compose config --quiet
# Only if validation succeeds:
sudo docker compose up -d --pull never
sudo docker compose ps
```

Verify health and that the archive bind is absent. No persistent data or volumes
need to be removed. The pre-task Git revision above provides the exact old Compose
line context. If a library has since been created, coordinate its UI handling
separately before removing access; this rollback is not permission to delete media
or application data.

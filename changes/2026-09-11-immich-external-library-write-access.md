# Immich external archive library: intentional write access

Date: 2026-09-11
Status: Applied and server-validated; USER disposable UI deletion test pending.

## Reason and exact change

The user explicitly requested that Immich UI deletion may delete the underlying
external original. The existing indexed library and its path are unchanged.
Compose project immich; file /home/kaian/nas-admin/compose/immich/docker-compose.yml.
Exactly one bind changed, on service immich-server / container immich_server:

```yaml
# Before
- '/srv/storage/archive/merged/Bilder og Video:/mnt/archive/bilder-og-video:ro'
# After
- '/srv/storage/archive/merged/Bilder og Video:/mnt/archive/bilder-og-video:rw'
```

The entire archive/merged roots are not mounted. hidden and all sibling categories
remain excluded. No host permission changes or recursive chmod/chown. No Samba,
Jellyfin, Tailscale, network/SSH/firewall, storage mount or Immich setting changes.
No new sidecar/XMP writing, metadata edit or reorganization feature was enabled.
The mount permits filesystem writes, not just unlink; application settings were
left unchanged. Albums/favorites remain Immich-side state and do not move folders.
AI/Codex no-delete rules remain in force; user-directed Immich capability does not
expand AI authorization. Reconcile later intentional UI deletions without recovery.

## Inspection, backup and bounded application

Direct Docker inspection was initially denied and sudo required interactive
terminal authentication. The administrator ran the reviewed helper:

```sh
sudo python3 -B /home/kaian/nas-admin/scripts/immich-external-library-rw.py --apply
```

It inspected live labels/mounts/processes, filesystem UUID, permissions and the
untouched test image before editing. Both source and test directories were
kaian:kaian (1000:1000), mode 0775. Both Immich processes run with effective
UID 0 / GID 0, mapped to host root. Actual process identity write/search
permission checks passed.
Pre-change Docker RW=false and container ro were confirmed independently.

Timestamped unexpanded Compose backup: `/home/kaian/media-archive-control/_merge-control/server-changes/immich-external-rw/20260911T132304Z/docker-compose.yml.before`.
No .env or expanded secret values were printed, copied into Git or saved in reports.
Rendered pre/post configurations were compared in memory: only read_only changed.
Compose parsing passed before application. Exact apply command:

```sh
cd /home/kaian/nas-admin/compose/immich
sudo docker compose config --quiet
sudo docker compose up -d --no-deps --pull never immich-server
```

No images were pulled/upgraded. Only immich_server changed container ID; the ML,
PostgreSQL and Valkey container IDs, all images, all other mounts and restart
policies were preserved. No volumes/data were removed or reset.

## Validation and disposable test

Root-generated receipt: `/home/kaian/media-archive-control/_merge-control/server-changes/immich-external-rw/20260911T132304Z/result.json`.
Completed: 2026-09-11T13:23:36.075498+00:00. success=true. All four containers healthy;
server restart count zero; local web HTTP 200, version 3.1.0; pg_isready passed.
Docker RW=true and container mountinfo rw confirmed. External library directories
and managed /data accessible; actual process user read/write/search checks passed.
Recent server logs contained no checked startup/mount/permission failure keywords.
No test file was created. No payload was deleted, moved, renamed or content-read.

Actual test path (Linux capitalization):
`/srv/storage/archive/merged/Bilder og Video/Disposeable/Xenomorph.jpg`.
It remains present, with identical inode/size/mtime/ctime/xattrs/ownership/mode.
The user should open it in Immich, delete/trash it, empty trash if needed for
physical deletion, and verify that exact filesystem path disappears. Codex did
not perform the deletion. End-to-end Immich deletion is not yet claimed verified.

Official behavior: [Immich external-library FAQ](https://docs.immich.app/FAQ/)
explains that writable external originals are deleted when trash is emptied;
[the external-library guide](https://docs.immich.app/guides/external-library/)
describes removing :ro. No library scan or deletion API was called by this task.

## Documentation and rollback

CURRENT_STATE.md, ARCHITECTURE.md and runbooks/everyday-commands.txt now reflect
intentional writable access and safe checks. Relevant Archive.Management future/
current documents were updated separately; previous phase evidence is unchanged.
Validation passed: complete diff review, git diff --check, exact six-file scope,
helper Python syntax, current documentation references/ownership receipts, and
secret-value checks. The .env remains ignored and untracked. A fresh HTTP check
returned 200 and the test file still matched its recorded metadata. Archive SQLite
was read-only checked: integrity ok, foreign-key violations zero, unresolved move
attempts zero; it was not modified. No credentials or archive payload enter Git.

To restore read-only, edit only the selected bind suffix from :rw to :ro, keeping
all later unrelated edits. Then run the validate/up commands above, affecting only
immich-server. Confirm Docker RW=false and container ro, health and HTTP 200.
The exact previous Compose bytes are in the timestamped backup above; restore
that whole file only if it contains no later changes that must be preserved.
Rollback does not require deleting volumes, uploads, database or archive media.

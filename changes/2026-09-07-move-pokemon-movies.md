# Move Approved Pokémon Feature Movies

Date: 2026-09-07

Status: Completed

## Reason

Retain Pokémon feature movies while moving them out of the active Jellyfin
Movies directory. A read-only audit identified localized titles from folder and
file names, checked embedded MP4 metadata and runtimes, and consulted movie
references. No NFO files were present and embedded title tags were empty or
absent. The administrator explicitly approved exactly the 14 folders below.
No uncertain/special/OVA candidates were identified in the audited source.

## Configuration

- Source: /srv/storage/media/movies
- Destination: /srv/storage/media/Pokemon/movies (already existed and was empty)
- WD My Book: /dev/sda1, ext4, mounted read/write at /srv/storage
- Source and destination are on the same filesystem.
- Jellyfin Movies library remains /media/movies.
- Destination is outside that library path, within the existing Media Samba
  share and the container's read-only /media mount.

## Changes

Moved only the 14 approved folders, containing 14 files (18,538,057,119 bytes).
Preserved all existing names and contents, permissions, and ownership. Nothing
was copied, overwritten, or deleted. The existing destination required no creation.
Pokémon TV content and all other unselected media were untouched. No Jellyfin
configuration changes, service restarts, or manually triggered scans occurred.

The prepared temporary script was run with:

```text
python3 /tmp/move-approved-pokemon.py inspect
python3 /tmp/move-approved-pokemon.py move
```

It used an explicit approved-name list and Linux renameat2 with
RENAME_NOREPLACE: atomic moves on the same filesystem with no overwrite or copy
fallback. A conflict skips that item; an unexpected error stops further moves.
The temporary script and JSON manifests are execution artifacts, not permanent
repository tooling. The durable approved/moved list is recorded below.

## Validation

- Git working tree was clean before work began.
- Host findmnt confirmed /srv/storage was mounted read/write on /dev/sda1.
- All 14 source folders existed, with no destination conflicts.
- Recursive manifests captured 28 entries: 14 folder roots and 14 files.
- Each source matched its manifest immediately before moving.
- All 14 original source paths were absent after moving.
- Immediate and final recursive destination checks matched relative names,
  device/inode identities, types, sizes, modes, ownership, modification times,
  and link counts. This verified relocation of the same filesystem objects;
  it was not full content hashing or playback verification. Rename-related
  change times were excluded from comparison.
- All 142 unselected source entries retained their paths and checked metadata.
- Source and destination name sets matched the expected result exactly.
- The sibling Pokemon/tvshow directory's checked metadata remained unchanged;
  no operation targeted its contents.
- Active Samba transfers were not independently ruled out; root-only lock
  inspection was unavailable without interactive authentication in this session.

## Outcome

All 14 approved folders moved and verified. No skips, conflicts, move errors,
or verification errors. No uncertain candidates remain pending from this audit.
Jellyfin's displayed library was not refreshed or verified; the administrator
handles that separately.

## Security

No secrets were added. Existing permissions and ownership were preserved;
Samba access configuration was not changed.

## Recovery

To undo this layout change in a later authorized task, move only the listed
folders from /srv/storage/media/Pokemon/movies back to /srv/storage/media/movies.
Confirm the storage mount and source identities first. Refuse any existing
recipient name; do not overwrite, merge, or delete anything. Use the same atomic
no-overwrite move and verify source absence and destination integrity afterward.
Keep Pokémon TV content outside the rollback scope. No rollback was performed.

## Moved Folders

```text
Mewtwo slår tilbake
Den enes kraft
Unowns forbannelse
Pokemon 4ever (2001)
Latios & Latias
Jirachi ønskeskaper
Skjebnens deoxys
Darkrai sin oppstand
Giratina og himmelkrigeren
Arceus og Livets Juvel
Zoroark Illusjonens mester
Pokémon the Movie - Black
Pokémon the Movie - White
Kyurem VS Rettferdighetens sverd
```

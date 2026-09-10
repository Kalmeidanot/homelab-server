# Record Completed Personal Media Archive Consolidation

Date: 2026-09-10

Status: Archive-project documentation catch-up completed

## Reason and scope

Bring the server repository up to date with the separate multi-day personal
media archive consolidation project. The 2026-09-07 Archive-share record describes
the earlier preparation milestone and remains valid historical evidence. This
task did not perform the historical merge, organization, source evacuation or
user deletions.

## Resulting architecture

| Purpose | Host path |
|---|---|
| Human-managed archive / Samba Archive share | /srv/storage/archive |
| Consolidated archive root | /srv/storage/archive/merged |
| Normal organized photos/videos | /srv/storage/archive/merged/Bilder og Video |
| Immich-managed uploads and derived data (separate) | /srv/storage/photos/immich |
| Immich PostgreSQL (internal SSD) | /srv/immich/postgres |
| Durable future-AI entry | /srv/storage/archive/00 - FUTURE AI START HERE.txt |
| Long-term management bundle | /srv/storage/archive/Archive.Management |
| Active detailed archive control plane | /home/kaian/media-archive-control |

The archive uses an intentional year / Norwegian month / meaningful event / device
model. Multi-day event/day hierarchy and original filenames remain meaningful;
device subfolders are used where appropriate, not imposed uniformly. The archive
bundle owns the detailed placement rules and exceptions.

Additional preserved categories beneath merged include Duplikater (additional
exact occurrences), Other (non-media), Explicitly review-blocked (unresolved
semantic placement) and Unreadable - Damaged. These are intentional categories,
not evidence that the source evacuation failed.

`/srv/storage/archive/merged/hidden` is **USER_MANAGED_EXCLUDED**. No automated
enumeration, individual stat, scan, count, hash, classification, source/canonical
use, reorganization, modification or deletion is authorized without a fresh
explicit user instruction naming that tree. It was not accessed in this task.

Former physical source drives were evacuated within the project's intended scope;
routine organization no longer depends on them. Historical drive letters are
provenance, not live paths or permission to recover user-deleted material.

Samba's existing Archive share remains authenticated read/write for kaian at
`\\homelab\Archive` (fallback `\\10.0.0.6\Archive`). No Samba change was made.
Human filesystem management remains separate from Immich-managed uploads.
The companion [Immich mount record](2026-09-10-add-immich-archive-external-mount.md)
tracks preparation of read-only visual indexing of only Bilder og Video.

## Closure and evidence limits

Authoritative evidence read from Archive.Management:

- FUTURE-AI-START-HERE.md
- ARCHIVE-OPERATING-RULES.md
- CURRENT-ARCHIVE-STATE.md
- USER-DECISIONS-AND-EXCLUSIONS.md
- LINUX-PATH-MAPPING.md
- CONTROL-RECOVERY-RUNBOOK.md

Also read the archive-root `00 - FUTURE AI START HERE.txt` pointer.
The H7 checkpoint is dated **2026-09-09 19:35:42 UTC**. It records H4/H5 complete
and H6 COMPLETE_WITH_USER_MANUAL_CLEANUP: automated organization is complete,
with four SEQ-515 files / 33,560,274 bytes still pending optional manual cleanup
at that checkpoint. This task did not recheck those files or perform cleanup.
Intentional user deletions, the retained SEQ-514 hierarchy, and review/fallback
categories must be interpreted using the current decisions rather than stale
merge destinations. Do not recreate intentionally removed Unknown payload or
the former raw directory shells.

Validation for this archive catch-up record was limited to reading the durable
documentation, confirming host `homelab`, checking the actual storage mount, and statting the
specific Bilder og Video root. `findmnt -T` confirmed ext4 /dev/sda1 mounted at
/srv/storage, UUID 0cd558d4-359e-4dab-922c-68bfdd5db432; the selected directory
was kaian:kaian, mode 0775. No recursive archive scan, hashing or control-database
inspection was performed. This is a dated architectural summary, not a fresh
per-file verification of the historical merge.

## Documentation and outcome

Updated CURRENT_STATE.md and ARCHITECTURE.md to replace the obsolete
"consolidation has not begun" current-state description. Reviewed and updated
runbooks/everyday-commands.txt with Archive-share access, the durable management
pointer and the companion Immich operational workflow. The multi-thousand-line
project history, private control database and media payload remain outside Git.

No archive files, archive control state, disks, Samba settings or unrelated
services were changed by this documentation catch-up.

## Recovery and references

The durable control snapshot currently named by the bundle is:

`/srv/storage/archive/Archive.Management/control-snapshots/final-handoff-20260909T193542Z`

It preserves control history after loss of chat, the OS or the internal SSD if
the archive disk survives. It resides on the same disk as the media and is not
an independent backup of that disk. The archive-root AGENTS/_merge-control are
older historical snapshots; do not replace newer active control with them.

For future authorized archive work, start at the durable entry point, read the
latest state and user decisions, and follow CONTROL-RECOVERY-RUNBOOK.md if
control recovery is needed. Validate the identified snapshot before restoring
control to a new local location; never overwrite newer control or infer media
recovery permission from historical references. No recovery was performed here.

Documentation rollback can use the pre-task Git revision
`5b8cfaa09c20a91f7e3af96b845e56be1fc4a629` as a reference. Reverting documentation
does not undo historical consolidation and must not imply the archive is empty.

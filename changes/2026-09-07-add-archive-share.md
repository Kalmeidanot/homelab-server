# Add Archive Samba Share

Date: 2026-09-07

Status: Completed (destination/share preparation only)

## Reason

Create a dedicated, human-managed archive on the WD My Book for a forthcoming
multi-drive personal photo/video consolidation. Keep it separate from Jellyfin
media at /srv/storage/media and Immich-managed storage at
/srv/storage/photos/immich, which must not be manually reorganized.

## Configuration

- Disk: permanently connected WD My Book 12 TB, mounted at /srv/storage
- Archive root: /srv/storage/archive
- Planned final consolidation root: /srv/storage/archive/merged
- Both directories at creation: owner/group kaian:kaian, permissions 0775
- Share: Archive, authenticated read/write access for kaian
- Windows path: `\\homelab\Archive`
- IP-path fallback: `\\10.0.0.6\Archive`

Added to /etc/samba/smb.conf:

```ini
[Archive]
    path = /srv/storage/archive
    read only = no
    valid users = kaian
    create mask = 0664
    directory mask = 0775
```

Immediately before the change, /srv/storage was observed on /dev/sda1 with an
ext4 filesystem mounted read/write: approximately 11 TB reported size, 1.9 TB
used, and 9.1 TB available. These are point-in-time observations, not permanent
expected capacity or free-space values.

## Changes

Created /srv/storage/archive and /srv/storage/archive/merged with the ownership
and permissions above.

Before installing the updated Samba configuration, backed up the previous live
configuration to:

/etc/samba/smb.conf.backup-20260907-122814

Installed the updated /etc/samba/smb.conf with the Archive share and reloaded
smbd successfully. The existing Media share was not intentionally changed.

Affected storage: WD My Book at /srv/storage, specifically the two new archive
directories. Affected configuration/service: /etc/samba/smb.conf and smbd.

## Validation

The following validation was completed during the server change, as reported
by the administrator; it was not repeated during this documentation-only task:

- testparm accepted the live configuration and showed Archive correctly in its
  parsed output.
- smbd reloaded successfully and remained active.
- Windows opened `\\homelab\Archive` and displayed the existing merged directory.
- Windows create/write access succeeded: a test folder was created inside
  merged and a test text file was created.
- Rename and delete succeeded, and the temporary test folder was removed afterward.

## Outcome

The destination and authenticated read/write Archive share are ready for the
upcoming consolidation. The personal photo/video merge has not begun or
completed. No Immich External Library is configured for this archive; possible
future indexing is separate work, as is the future Lightroom-specific proposal.

## Security

Archive access is restricted by Samba to the authenticated user kaian. Directory
permissions 0775 allow local owner/group writes and other local users to read
and traverse; the Samba create and directory masks are 0664 and 0775.
No passwords or other secrets are stored in this record.

## Recovery

Troubleshooting steps (documented only; not performed during this task):

1. Confirm /srv/storage is mounted with `findmnt /srv/storage`.
2. Confirm both archive directories exist and check their ownership/permissions
   with `stat -c '%U:%G %a %n' /srv/storage/archive /srv/storage/archive/merged`.
   Expected owner/group: kaian:kaian; directory mode: 775 (0775).
3. Check smbd with `systemctl status smbd --no-pager`.
4. Run `testparm` to validate the live Samba configuration.
5. If necessary, compare /etc/samba/smb.conf against
   /etc/samba/smb.conf.backup-20260907-122814, accounting for any later changes.

If rollback is needed in a separately authorized server-change task, use the
backup as a reference to remove the Archive share or restore the previous
configuration after reviewing later changes, validate with testparm, and reload
smbd. Preserve the archive directories and their contents; removing share access
does not require deleting data. No recovery or server changes were performed
as part of this documentation task.

## Operational Reference

Reviewed runbooks/everyday-commands.txt. Its existing Media paths remain valid,
but it does not yet list Archive. It was left unchanged because this task permits
Markdown edits only. The Archive access paths and troubleshooting checks are
recorded above; adding them to the .txt runbook remains a documentation follow-up.

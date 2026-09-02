# Configure WD My Book NAS Storage

Date: 2026-09-02

Status: Completed

## Reason

Prepare the 12 TB WD My Book as the primary bulk-storage disk for the homelab.

## Changes

- Replaced the factory exFAT filesystem with ext4.
- Kept the existing GPT partition layout.
- Labeled the filesystem STORAGE.
- Created the permanent mount point /srv/storage.
- Configured automatic mounting by filesystem UUID rather than /dev/sda.
- Created the initial media and data directory structure.

## Destructive Operation

The existing filesystem on /dev/sda1 will be erased.

The user explicitly confirmed that the disk contains no required data and approved formatting.

## Validation

- /srv/storage is mounted read/write.
- Samba remained operational and can access /srv/storage/media.
- The media directory is available to Jellyfin through a read-only container mount.

## Outcome

Successful. The My Book is the server's active bulk-storage disk.

## Affected Files and Services

- External disk filesystem on the WD My Book
- /etc/fstab
- /srv/storage and its initial directory structure
- Samba Media share
- Jellyfin media mount

## Rollback / Recovery

The original exFAT filesystem was intentionally erased and cannot be restored by
reverting repository documentation. If automatic mounting fails, validate the
filesystem UUID and the corresponding /etc/fstab entry before mounting manually.

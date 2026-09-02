# Install Samba File Sharing

Date: 2026-09-02

Status: Completed

## Reason

Allow the main Windows PC to transfer media files to the WD My Book over the local network.

## Configuration

Share name:

Media

Path:

/srv/storage/media

Access:

- authenticated
- user: kaian
- read/write

Windows path:

\\10.0.0.6\Media

## Changes

Installed Samba.

Created a Samba account for the existing Linux user kaian.

Backed up the original Samba configuration to:

/etc/samba/smb.conf.backup-2026-09-02

Configured the Media share in:

/etc/samba/smb.conf

Enabled the Samba service to start automatically.

## Validation

- testparm reported: Loaded services file OK.
- smbd started successfully.
- Windows connected successfully to the Media share.
- Authentication succeeded.
- movies, tv-series and other folders are visible.
- Creating, renaming and deleting a test item from Windows succeeded.

## Outcome

Successful.

Samba file transfer to the WD My Book is operational.

## Security

The Samba password is not stored in this repository.

## Recovery

If the share fails:

1. Verify /srv/storage is mounted.
2. Check smbd status.
3. Run testparm.
4. Compare /etc/samba/smb.conf with the backup.

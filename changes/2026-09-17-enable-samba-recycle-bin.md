# Enable Samba recycle-bin protection for Media and Archive

Date: 2026-09-17
Status: Active and tested on both shares; test artifacts removed, roots retained.

## Evidence, reason and scope

This record uses the user's supplied evidence of completed configuration and
Windows SMB tests. This documentation/Git task ran no sudo or live-server checks,
changed no services or /etc files, and did not access /srv/storage payload or
/srv/storage/archive/merged/hidden.

An accidental Windows Explorer deletion through `\\10.0.0.6\Media\movies`
deleted multiple movie files before the user cancelled. The user chose not to
attempt filesystem recovery. Recycle protection was then enabled as a safety
net for future SMB deletions; it does not recover the earlier deleted movies.

Affected configuration/service: /etc/samba/smb.conf and smbd. Affected shares
and storage: Media at /srv/storage/media and Archive at /srv/storage/archive,
on the same physical WD My Book. No other share received these settings.

## Preparation and installed configuration

The Samba module was confirmed present:
`/usr/lib/x86_64-linux-gnu/samba/vfs/recycle.so`.
A temporary candidate configuration was created and validated before installation.
The pre-installation backup is `/etc/samba/smb.conf.backup-20260917-194704`,
owned by root:root with mode 0644. The live /etc/samba/smb.conf remains
root:root, mode 0644. The backup is a server-local recovery file; its contents
were not copied into this repository.

These settings were added ONLY under both `[Media]` (path = /srv/storage/media)
and `[Archive]` (path = /srv/storage/archive):

```ini
vfs objects = recycle
recycle:repository = .recycle/%U
recycle:keeptree = yes
recycle:versions = yes
recycle:touch = no
recycle:touch_mtime = no
recycle:directory_mode = 0700
recycle:subdir_mode = 0700
recycle:exclude_dir = .recycle
```

No maxsize, minsize, or file exclusion list was configured. Large files such as
movies are therefore eligible for recycle protection too. The repository is
relative to each share and separated by username, with the original tree retained.

Both candidate and installed configurations passed testparm:
`Loaded services file OK.` smbd was **reloaded, not restarted**.
After reload, `systemctl is-active smbd` returned `active`.

## End-to-end tests supplied by the user

### Archive: passed

A harmless file was created at:
`/srv/storage/archive/_RECYCLE_TEST_20260917-195058/archive-test.txt`.
The user deleted it through Windows Explorer over SMB. The original path
disappeared and the file appeared at:
`/srv/storage/archive/.recycle/kaian/_RECYCLE_TEST_20260917-195058/archive-test.txt`.
Its contents remained intact. Archive recycle test PASSED.

### Media: initial old-connection test and successful reconnect test

Shortly after smbd reload, the user deleted a harmless Media test through Windows
Explorer. The original disappeared but no Media .recycle tree was created.
Investigation showed that the Windows PC still had an established Media SMB share
connection from before the reload. No Samba error was found in journal output.

All SMB connections were then closed. The user's `sudo smbstatus` check showed
no sessions and no locked files. A fresh test file was created at:
`/srv/storage/media/_RECYCLE_TEST_MEDIA_20260917-201125/media-test-2.txt`.

The Windows client opened Media with a new SMB connection and deleted the file.
The original disappeared and the recycled file appeared at:
`/srv/storage/media/.recycle/kaian/_RECYCLE_TEST_MEDIA_20260917-201125/media-test-2.txt`.
Its contents were intact:

```text
Samba recycle test - Media round 2
```

Media recycle test PASSED after reconnect. The first test did not recycle the
file, but this was not a Samba recycle configuration failure. An already-established
SMB share connection may continue using its previous share configuration after
an smbd configuration reload. A client reconnect was required for the new recycle
behavior to apply. A successful testparm or active smbd alone does not establish
that an old client connection has adopted new share settings.

## Directory security and completed test cleanup

After successful testing, all four directories were verified as `700 kaian:kaian`:

- /srv/storage/media/.recycle
- /srv/storage/media/.recycle/kaian
- /srv/storage/archive/.recycle
- /srv/storage/archive/.recycle/kaian

All test files and _RECYCLE_TEST* directories were then explicitly removed.
Final verification found both .recycle roots still present, each mode 700 and
owned by kaian:kaian, with no _RECYCLE_TEST* artifacts remaining.
**Do not delete the .recycle roots.** No cleanup was performed by this
documentation task.

## Protection limits

Samba recycle is **not a backup** and **not a general Linux filesystem recycle
bin**. It protects deletions passing through the Samba/SMB shares. It does not
protect against:

- rm or other direct Linux filesystem deletion;
- application/container deletion bypassing Samba, including Immich's writable
  external archive bind;
- disk failure or filesystem corruption;
- loss of the WD My Book;
- sufficiently privileged malicious access.

Recycled content stays on the SAME physical WD My Book. Deleted files continue
consuming disk space until recycle contents are deliberately removed.
`recycle:exclude_dir = .recycle` means deliberate deletion inside the recycle
area is not recursively recycled. There is no independent backup created by
this change.

## Recovery and documentation

For an accidental SMB deletion, inspect the relevant user's recycle tree and
identify the exact file and destination before deliberately restoring it. Check
for an existing destination to avoid overwriting retained data. Do not restore
intentionally deleted archive material from historical records or broaden access
to the excluded hidden tree. No bulk restore or cleanup is authorized here.

If configuration rollback is later necessary, review the server-local backup
above against the then-current configuration, preserving unrelated later changes.
In a separately scoped server-change task, prepare and validate a candidate with
testparm before installation, reload smbd, and reconnect clients before validating
behavior. Removing recycle configuration removes protection for future SMB
deletes; it does not require deleting the recycle roots or their contents.

CURRENT_STATE.md summarizes tested protection; ARCHITECTURE.md describes its
same-disk/SMB boundary. The everyday runbook adds read-only size, file-location,
permission, testparm and connection checks, plus the reconnect lesson and limits.
It contains no broad recycle cleanup/delete commands. README.md remains suitable
unchanged. Reverting this documentation commit changes no Samba configuration
or stored data.

Documentation validation: reviewed the full Git diff and exact five-file scope;
whitespace checks passed. No secrets, /etc backup contents or unrelated files
are included. Docker/Immich and SSH hardening remain explicitly pending; Samba
limits and the initial Media connection/reconnect test sequence are preserved.

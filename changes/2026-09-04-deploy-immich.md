# Initial Immich Deployment

Date: 2026-09-04

Status: Completed

## Reason

Deploy a private photo and video management service with bulk data on the WD My
Book, database storage on the internal SSD, and remote access through Tailscale.

## Configuration

- Immich version: v3.1.0
- Compose directory: ~/nas-admin/compose/immich
- Compose definition: ~/nas-admin/compose/immich/docker-compose.yml
- Deployment basis: official Immich Compose files
- Secret environment file: ~/nas-admin/compose/immich/.env
- LAN URL: http://10.0.0.6:2283
- Tailscale URL: http://100.83.35.13:2283
- Immich-managed upload location: /srv/storage/photos/immich on the WD My Book
- PostgreSQL data: /srv/immich/postgres on the internal SSD
- Time zone: Europe/Oslo

The `.env` file is ignored by Git and remains untracked. Its database password
and other secret contents are not recorded in this repository. PostgreSQL and
Valkey ports were not intentionally exposed as user-facing host services.

The upload location contains Immich-managed photo/video data, thumbnails,
generated or encoded media, backups, and other managed content. It is not a
manually managed Samba photo directory and must not be edited behind Immich's
back.

## Host Prerequisite

Valkey initially warned that Linux memory overcommit was disabled. The setting
was corrected persistently in /etc/sysctl.d/99-immich.conf:

```text
vm.overcommit_memory=1
```

Runtime verification confirmed `vm.overcommit_memory = 1`.

## Containers and Validation

The following containers were confirmed operational and healthy after initial
startup:

- immich_server
- immich_machine_learning
- immich_postgres
- immich_redis

Functional validation confirmed:

- the web interface loaded and the initial/admin account was created
- browser and phone photo uploads worked
- mobile uploads appeared immediately in the browser
- the timeline, thumbnails, and photo viewing worked
- the machine-learning service became healthy
- test photo data was written under /srv/storage/photos/immich
- PostgreSQL data was present under /srv/immich/postgres

During initial testing, the Immich-managed tree used approximately 266 MB and
PostgreSQL used approximately 312 MB. These are point-in-time observations, not
fixed expected values.

## Remote Access Validation

A phone successfully loaded and used Immich away from the direct LAN through
Tailscale at http://100.83.35.13:2283. Tailscale remains the current secure
remote-access method. Immich port 2283 is not intentionally exposed directly to
the public Internet.

## Reboot and Autostart Validation

A full server reboot was performed with `sudo reboot`. Ubuntu and SSH returned
normally, the Immich Docker stack returned automatically, and Immich became
available without a manual stack start. The reboot/autostart test was successful.

## Affected Files and Services

- ~/nas-admin/compose/immich/docker-compose.yml
- ~/nas-admin/compose/immich/.env (secret, Git-ignored, untracked)
- /etc/sysctl.d/99-immich.conf
- /srv/immich/postgres
- /srv/storage/photos/immich
- immich_server
- immich_machine_learning
- immich_postgres
- immich_redis

## Outcome

Immich v3.1.0 is operational on the LAN and through Tailscale. Uploads, viewing,
machine learning, persistent storage, remote access, and automatic return after
reboot were successfully validated.

## Rollback / Recovery

The Compose project can be stopped and its containers removed without deleting
the bind-mounted PostgreSQL or upload-location data. Preserve the `.env` file and
both persistent data paths when recreating or recovering the service. Treat any
deletion of those paths, database reset, or removal of managed media as a separate
destructive operation requiring explicit review and approval.

## Future Work

Evaluate a separate human-managed Adobe Lightroom archive at
/srv/storage/photos/lightroom, potentially shared through a separate Samba Photos
share and indexed by Immich as a read-only External Library. Nothing has been
created or configured for this future architecture, and the Lightroom archive
must remain separate from Immich-managed upload storage.

# Initial Jellyfin Deployment

Date: 2026-09-02

Status: Completed

## Reason

Provide local media playback for movies and TV series stored on the My Book.

## Configuration

- Compose file: ~/nas-admin/compose/jellyfin/compose.yaml
- Official image: jellyfin/jellyfin:latest
- Container name: jellyfin
- Restart policy: unless-stopped
- Network mode: host
- Configuration: /srv/jellyfin/config
- Cache: /srv/jellyfin/cache
- Media: /srv/storage/media mounted read-only as /media
- Intel render device: /dev/dri/renderD128
- Supplemental render group GID: 991
- Browser access: http://10.0.0.6:8096

## Initial Setup

- Completed the Jellyfin setup wizard.
- Configured Movies at /media/movies.
- Configured TV at /media/tv-series.
- Started the initial metadata and library scan; it is still being allowed to finish.

## Validation

- Browser access succeeded.
- Playback succeeded in a browser.
- Playback succeeded on the TV.
- Hardware-accelerated transcoding has not yet been formally validated. The render
  device configuration must not be treated as proof that QSV transcoding works.

## Affected Files and Services

- ~/nas-admin/compose/jellyfin/compose.yaml
- /srv/jellyfin/config
- /srv/jellyfin/cache
- /srv/storage/media (read-only container access)
- jellyfin container

## Outcome

Successful initial deployment and playback validation. Metadata scanning remains
in progress, and formal hardware-transcoding validation remains outstanding.

## Rollback / Recovery

The container can be stopped and removed through its Compose project without
deleting /srv/jellyfin/config, /srv/jellyfin/cache, or the read-only media source.
Preserve those persistent directories when recreating or recovering the service.

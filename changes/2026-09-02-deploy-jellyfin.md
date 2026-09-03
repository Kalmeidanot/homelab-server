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

### Intel hardware acceleration

Follow-up validation completed on 2026-09-03:

- Confirmed the Intel UHD Graphics 770 render device at /dev/dri/renderD128 is
  passed through to the official Jellyfin container.
- Ran `/usr/lib/jellyfin-ffmpeg/vainfo --display drm --device /dev/dri/renderD128`
  inside the container successfully.
- The VA-API test detected the Intel iHD driver and confirmed operational hardware
  decode support for H.264, HEVC, MPEG-2, VC-1, VP9 and AV1, with relevant hardware
  encoding profiles also available.
- Configured Jellyfin to use Intel Quick Sync (QSV).
- Deliberately forced a real playback transcode in the Jellyfin web client by
  lowering the playback bitrate.
- The Jellyfin Dashboard reported active transcoding because the video's bitrate
  exceeded the configured limit, with H.264 video and AAC audio output. The observed
  speed was approximately 823 fps during this particular test.
- The corresponding Jellyfin FFmpeg transcode log included /dev/dri/renderD128,
  Intel iHD VA-API device initialization, `hwaccel vaapi`, QSV device derivation,
  `h264_qsv`, and `encoder: Lavc61.19.101 h264_qsv`.

This formally verifies Intel hardware-accelerated transcoding for the tested real
H.264 QSV transcode. It does not claim validation of every supported codec,
encoding path or tone-mapping scenario.

## Affected Files and Services

- ~/nas-admin/compose/jellyfin/compose.yaml
- /srv/jellyfin/config
- /srv/jellyfin/cache
- /srv/storage/media (read-only container access)
- jellyfin container

## Outcome

Successful deployment and playback validation. Intel hardware-accelerated
transcoding is formally verified for a real H.264 QSV transcode. Metadata scanning
remains in progress; other codec and tone-mapping scenarios have not been
individually validated.

## Rollback / Recovery

The container can be stopped and removed through its Compose project without
deleting /srv/jellyfin/config, /srv/jellyfin/cache, or the read-only media source.
Preserve those persistent directories when recreating or recovering the service.

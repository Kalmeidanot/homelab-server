# Enable public Jellyfin access through Tailscale Funnel

Date: 2026-09-12

Status: CLI configuration succeeded; public HTTPS TV authentication/playback
pending validation.

## Reason

Provide a public HTTPS Jellyfin address for remote clients, including TVs that
cannot run Tailscale, while retaining private Tailscale access for Jellyfin,
administration and Immich. The user confirmed the remote TV has a Jellyfin app
but could not test it yet.

## Pre-change checks

The user supplied these verified observations from 2026-09-12:

- Tailscale version on homelab: 1.102.3.
- `tailscale funnel status` reported `No serve config`.
- Jellyfin at http://127.0.0.1:8096 responded with HTTP 302.
- Tailscale DNS name: homelab.tail328fad.ts.net.
- Existing private Jellyfin address: http://100.83.35.13:8096.
- Existing LAN Jellyfin address remains http://10.0.0.6:8096.

## Change performed by the user

Exact persistent/background command:

```sh
sudo tailscale funnel --bg 8096
```

Tailscale initially reported that Funnel was not enabled for the tailnet and
offered a web approval flow. The user approved Funnel through Tailscale. The
one-time approval URL is intentionally omitted; no credentials are recorded.

After approval, Tailscale reported:

```text
Success.
Available on the internet:

https://homelab.tail328fad.ts.net/

proxy -> http://127.0.0.1:8096

Funnel started and running in the background.
```

The public HTTPS endpoint proxies to Jellyfin locally at 127.0.0.1:8096.
Background mode records the persistent Funnel configuration; no separate
Jellyfin startup command was added. Funnel recovery after reboot has not been
tested as part of this change.

## Scope and affected services

- Tailscale Funnel configuration for homelab and tailnet Funnel approval changed.
- Only Jellyfin is intentionally publicly exposed through Funnel.
- Immich remains private, with remote access through Tailscale only at
  http://100.83.35.13:2283; it is not exposed through Funnel.
- Cockpit, SSH, Samba and other services were not exposed through Funnel.
- Existing LAN and private Tailscale Jellyfin access remain available.

No Jellyfin Docker Compose, media, library, account or configuration changes
were made. No Docker, firewall, router, storage or disk configuration was
changed. Jellyfin port 8096 was not directly exposed with router port forwarding.
The private Tailscale administration path was retained.

This follow-up task only updates repository documentation. It does not execute
Funnel commands or change any server runtime state. Affected documentation:
CURRENT_STATE.md, ARCHITECTURE.md, inventory/network.md,
runbooks/everyday-commands.txt and this change record. Historical change records
remain unchanged.

## Validation and outcome

The Tailscale CLI confirmed successful Funnel configuration and background
operation. The local HTTP 302 observation established that Jellyfin responded
before the change. Earlier private Tailscale authentication/playback validation
remains documented in changes/2026-09-04-install-tailscale.md.

Public HTTPS TV authentication and playback have NOT yet been tested. The CLI
success is configuration evidence, not proof of successful remote TV login or
playback, and does not validate compatibility with arbitrary TVs.

Pending user validation: on the remote TV's Jellyfin app, enter
https://homelab.tail328fad.ts.net/, authenticate and try video playback. Record
the tested device/app and outcome in a follow-up documentation update, without
recording credentials. No public login/playback test was run in this
documentation-only task.

Documentation validation: reviewed the complete diff and searched the repository
for stale Funnel/public-access and TV backlog claims. Current-state conflicts
were updated, including inventory/network.md; the historical Tailscale install
record was preserved. `git diff --check` passed, and the diff contains no
credentials or one-time approval URL.

## Security note

The public endpoint exposes Jellyfin's login surface to the Internet. Jellyfin
accounts should use strong unique passwords. The public address does not require
the client to join the private tailnet; administration and Immich remain private.

## Rollback and recovery

To intentionally disable the public HTTPS Funnel endpoint, use the disable
command reported by Tailscale, with sudo:

```sh
sudo tailscale funnel --https=443 off
```

Disabling Funnel does not disable normal private Tailscale access and does not
require stopping Jellyfin, Docker or tailscaled, or changing router settings.

Safe inspection and verification commands for later troubleshooting:

```sh
tailscale funnel status
tailscale status
curl -I http://127.0.0.1:8096
```

While enabled, verify that Funnel status lists the public HTTPS address and
http://127.0.0.1:8096 proxy target. After rollback, verify that this Funnel
endpoint is absent, check that the public URL no longer serves Jellyfin, and
check Jellyfin on the LAN at http://10.0.0.6:8096 and on a tailnet client at
http://100.83.35.13:8096. The pre-change local response was HTTP 302.

If restoring public access is desired after rollback, deliberately reapply
`sudo tailscale funnel --bg 8096`, complete Tailscale approval if requested,
inspect Funnel status and validate remote authentication/playback. Document
the restored state and results. These rollback/recovery steps are instructions
for future use; they were not executed in this documentation-only task.

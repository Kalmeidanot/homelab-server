# Validate Jellyfin Funnel after the tailnet DNS rename

Date: 2026-09-13

Status: New public HTTPS hostname and off-site TV client connection validated
from user-supplied evidence. Public-path video playback remains unverified;
the old Funnel hostname remains a known cleanup item.

## Reason and previous pending state

Record successful validation after the tailnet DNS suffix changed from
`tail328fad.ts.net` to `geep-krait.ts.net`. The initial Funnel enablement was
recorded in commit `621dc74069ccdead3f6c9426076d2643d3ec9062`; the rename was
recorded in commit `35b03ed7ae80ef7311b861e873c5d723600d7db7`.

Immediately after the rename, Funnel status still listed only
https://homelab.tail328fad.ts.net and the admin console showed `No certificate
found`. New-hostname HTTPS and TV validation were correctly pending then.
The two 2026-09-12 change records remain unchanged as historical evidence.
This follow-up supersedes that pending state for HTTPS and TV client connection.

## Command rerun by the user

The user reran:

```sh
sudo tailscale funnel --bg 8096
```

Tailscale successfully reported:

```text
Available on the internet:

https://homelab.geep-krait.ts.net/
|-- proxy http://127.0.0.1:8096

Funnel started and running in the background.
```

The intended public Jellyfin URL is https://homelab.geep-krait.ts.net.
Do not add :8096. The proxy target remains http://127.0.0.1:8096.

The user then ran `tailscale funnel status`, which showed both hostnames:

```text
https://homelab.geep-krait.ts.net (Funnel on)
|-- / proxy http://127.0.0.1:8096

https://homelab.tail328fad.ts.net (Funnel on)
|-- / proxy http://127.0.0.1:8096
```

## HTTPS and TV validation

The user ran:

```sh
curl -I https://homelab.geep-krait.ts.net
```

Reported successful result:

```text
HTTP/2 302
location: web/
server: Kestrel
```

This confirms public DNS resolves sufficiently for HTTPS access, TLS/HTTPS
works on the new hostname, Funnel reaches Jellyfin, and Jellyfin responds
through the new public hostname. It does not depend on a separate later
admin-console certificate-status inspection.

The user then tested the Jellyfin app on an off-site TV using
https://homelab.geep-krait.ts.net. The TV does NOT have Tailscale installed.
The app successfully connected to Jellyfin through the public HTTPS hostname.
This validates TV client connection without joining the private tailnet.
Video playback through this new public Funnel path has not been established
and is left unverified. Earlier private-path playback evidence does not
establish playback through this public path.

## Scope and security

The command rerun and external tests above were performed by the user before
this documentation task; they were not executed by the documentation agent.
This task changed repository documentation only and made no runtime changes:
no Tailscale, Funnel, Jellyfin, Docker, networking, firewall, router, DNS,
certificate, service or other runtime state was modified.

- LAN Jellyfin remains http://10.0.0.6:8096.
- Private Tailscale Jellyfin remains http://100.83.35.13:8096.
- Immich remains private through Tailscale at http://100.83.35.13:2283.
- Cockpit, SSH, Samba and other services remain outside Funnel.
- No router port forwarding was added; port 8096 was not directly exposed.
- No Jellyfin configuration, accounts, libraries, Docker/Compose configuration,
  media, storage or disk changes were made for this validation.

Only Jellyfin is intentionally public through Funnel. Its login surface is
publicly accessible, so Jellyfin accounts should use strong unique passwords.

## Remaining cleanup and recovery

The old https://homelab.tail328fad.ts.net entry still appears in Funnel status
alongside the new hostname. It is a known stale/legacy entry pending cleanup
in a separate deliberate runtime task. It was not removed or modified here;
its status listing does not establish that the old URL still works.

A future cleanup task should inspect the current configuration, deliberately
remove the legacy entry while preserving the new endpoint, and validate the
result. No cleanup command is executed or prescribed by this documentation task.
The safe read-only inspection command remains `tailscale funnel status`.
Existing LAN and private Tailscale paths remain documented for recovery access.
A documentation correction can be reverted in Git without changing runtime state.

## Documentation review

The working tree was clean on main, in sync with origin/main, before editing.
Updated CURRENT_STATE.md, ARCHITECTURE.md, inventory/network.md and
runbooks/everyday-commands.txt, and added this follow-up record. The historical
September 12 records were preserved unchanged.

Reviewed the full diff and searched documentation for obsolete pending/expected
public-hostname wording and both DNS suffixes. Remaining old-hostname references
are intentional historical evidence (including the rename explanation) or the
known stale Funnel entry awaiting cleanup. Remaining public-path playback and
Funnel reboot-recovery limitations are not superseded by connection validation.
`git diff --check` passed. No secrets or credentials were added.

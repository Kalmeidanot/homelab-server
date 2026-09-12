# Rename the Tailscale tailnet DNS suffix

Date: 2026-09-12

Status: DNS rename confirmed; Funnel status still lists the previous hostname.
New-hostname HTTPS and external Jellyfin/TV authentication/playback validation
remain pending.

## Reason and change performed by the user

Replace the opaque generated `tail328fad.ts.net` tailnet name with the
easier-to-remember Tailscale-provided `geep-krait.ts.net` name. The user made the
rename through the Tailscale admin console after the initial Funnel enablement.

- Old tailnet DNS suffix: `tail328fad.ts.net`.
- New tailnet DNS suffix: `geep-krait.ts.net`.
- Old machine DNS name: `homelab.tail328fad.ts.net`.
- New machine DNS name: `homelab.geep-krait.ts.net`.
- Machine/server name remains `homelab`.
- Expected public Jellyfin URL: https://homelab.geep-krait.ts.net/.

The admin console displayed Domain `homelab.geep-krait.ts.net`. Immediately
after the rename, its TLS certificate status showed `No certificate found`.
This is a dated user-reported observation, not a later certificate inspection.

Funnel had been successfully enabled before the rename. That change was
committed and pushed as `621dc74069ccdead3f6c9426076d2643d3ec9062`
(`docs: record Jellyfin Tailscale Funnel access`). Its historical record,
changes/2026-09-12-enable-jellyfin-tailscale-funnel.md, retains the old hostname.
Public TV login and playback were already unvalidated at that point.

## Read-only runtime checks

Before documentation edits, ran on homelab:

```sh
tailscale status --json | python3 -c 'import sys,json; print(json.load(sys.stdin)["Self"]["DNSName"])'
```

Successful output (including the trailing DNS dot):

```text
homelab.geep-krait.ts.net.
```

Then inspected the existing Funnel configuration without modifying it:

```sh
tailscale funnel status
```

Exact successful output, including its leading and trailing blank lines:

```text

# Funnel on:
#     - https://homelab.tail328fad.ts.net

https://homelab.tail328fad.ts.net (Funnel on)
|-- / proxy http://127.0.0.1:8096

```

Both successful checks exited with status 0. Initial sandboxed attempts could
not access the local Tailscale daemon socket: Funnel inspection reported
`connect: operation not permitted`, and the DNS pipeline had no JSON to parse.
The same read-only commands were rerun with approved access outside the sandbox.
No daemon start/restart or configuration command was executed. The initial
connection failure was not evidence that tailscaled was stopped.

The DNS output confirms that the local Tailscale node reports the new name.
Funnel status still reports the old hostname as `Funnel on`, with the unchanged
local proxy target. This mismatch is recorded as observed; its cause was not
established or repaired. Neither command establishes certificate issuance or
public reachability through the new name.

## Scope and unchanged configuration

The user changed the tailnet DNS suffix in the admin console. This follow-up
task changed repository documentation only. No changes were made to:

- Jellyfin configuration, accounts, libraries or media.
- Docker or Docker Compose.
- Funnel target: http://127.0.0.1:8096.
- Router configuration or port forwarding; port 8096 was not directly exposed.
- Immich exposure: remote access remains private through Tailscale only.
- SSH, Cockpit, Samba or other service exposure: these remain outside Funnel.
- Server/machine hostname: `homelab`.
- Tailscale IPv4: 100.83.35.13.
- LAN Jellyfin URL: http://10.0.0.6:8096.
- Private Tailscale Jellyfin URL: http://100.83.35.13:8096.

No certificate was requested or created by this task. No Tailscale, Funnel,
Jellyfin, Docker, network, firewall, router or service configuration command was
executed. Only Jellyfin is intended to be public through Funnel; strong unique
Jellyfin account passwords remain appropriate for its public login surface.

## Validation and pending external test

Confirmed: the admin-console rename and local Tailscale DNS name. Funnel was
enabled before the rename, and current read-only status still lists the old
hostname with the existing target. New-hostname certificate issuance, public
HTTPS reachability, Jellyfin login and playback are NOT validated.

The remote TV has a Jellyfin app, but the user has not tested the new hostname.
A later external-client/TV test should use https://homelab.geep-krait.ts.net/,
check HTTPS, authenticate and play video, then record the tested client and
outcome without credentials. No public HTTPS request, login or playback test
was performed during this documentation-only task.

## Recovery and troubleshooting

Use the read-only DNS and Funnel status commands above to compare the node's
name with the configured Funnel hostname. Preserve the output if the mismatch
persists. Use the existing LAN or private Tailscale Jellyfin address while
public access is unvalidated. Do not infer that the old public URL still works
from its presence in status output.

Certificate requests, Funnel reconfiguration, service restarts or reversing
the tailnet rename require a separate authorized configuration task. Do not
perform them merely to make documentation validation pass. The existing
documented command to deliberately disable the public endpoint remains:

```sh
sudo tailscale funnel --https=443 off
```

It was not executed. Disabling Funnel does not disable normal private Tailscale
access and does not itself reverse the tailnet DNS rename.

## Documentation review

The working tree was clean on main, in sync with origin/main, before editing.
Current references were updated in CURRENT_STATE.md, ARCHITECTURE.md,
runbooks/everyday-commands.txt and inventory/network.md. The original Funnel
enablement record was preserved unchanged.

Remaining old-suffix references are intentional historical evidence: the
original enablement record, the explicit old-to-new rename history in
ARCHITECTURE.md, and this record's old-name fields and captured Funnel output.
They are not presented as the current operational hostname. Full diff review,
the repeated old-suffix search and `git diff --check` were used to validate the
documentation. No secrets, credentials, approval URLs or private keys were added.

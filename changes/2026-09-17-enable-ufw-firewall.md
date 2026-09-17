# Enable UFW host firewall

Date: 2026-09-17
Status: Completed; Docker/Immich exposure and SSH hardening remain pending.

## Evidence and scope

This records already-completed live-server changes and validation supplied by
the user. This documentation/Git task did not run sudo, inspect or modify live
firewall configuration, restart/reload services, or access storage payload.
Commands in the everyday runbook are reference instructions, not checks executed
in this task.

## Reason and configuration

UFW was previously inactive. It was configured and enabled to establish a host
firewall while retaining home-LAN service access and private Tailscale access.

- Default incoming policy: deny.
- Default outgoing policy: allow.
- Explicit home-LAN source: 10.0.0.0/24.

| Allowed LAN port | Service |
| --- | --- |
| 22/tcp | SSH home LAN |
| 9090/tcp | Cockpit home LAN |
| 445/tcp | Samba home LAN |
| 8096/tcp | Jellyfin home LAN |
| 2283/tcp | Immich home LAN |

Also allowed: all inbound traffic on tailscale0 (Tailscale private network),
and 41641/udp for Tailscale direct connections.

Affected state: persistent UFW host firewall configuration and startup enablement;
network access to SSH, Cockpit, Samba, Jellyfin, Immich and Tailscale. Exact
configuration-file diffs and command transcript were not supplied, so this record
documents the confirmed policies/rules rather than inventing file-level edits.
No disk or storage-path change is part of this firewall change.

## Validation and outcome

After enablement, the user reported:

- UFW active and enabled on system startup.
- A fresh SSH connection from the Windows PC to 10.0.0.6 succeeded.
- LAN access remained functional.
- Jellyfin and Immich were both reachable from a Tailscale-connected device.

The host firewall is enabled with the intended LAN/Tailscale rules. Startup
configuration was confirmed; a subsequent reboot test was not supplied.

## Unresolved security caveats

Immich remains Docker-published on both `0.0.0.0:2283` and `[::]:2283`.
Docker-published ports may bypass normal UFW INPUT filtering. The LAN allow rule
and incoming-deny default do not establish that UFW alone protects port 2283.
Immich exposure is NOT fully hardened. Planned Immich/Tailscale exposure
hardening remains pending; successful Tailscale access does not prove access
from other networks is blocked.

SSH hardening is also incomplete: `PasswordAuthentication` was still enabled
during the audit. Firewall activation does not complete SSH authentication
hardening.

## Recovery and documentation

No rollback was reported necessary. Future firewall changes require explicit
approval under AGENTS.md. Before any such change, inspect the current rules,
preserve a working administration/recovery path, and plan access validation.
No exact prior ruleset backup was supplied; do not treat disabling UFW as a
routine troubleshooting step or assume it would undo every rule change.

CURRENT_STATE.md records the policies and pending hardening. ARCHITECTURE.md
clarifies the host-firewall boundary and intended Immich access. The everyday
runbook now includes read-only UFW status/startup checks and the Docker caveat.
README.md remains appropriate unchanged. Reverting this documentation commit
would not change the live firewall.

Documentation validation: reviewed the full Git diff and exact five-file scope;
whitespace checks passed. No secrets, /etc backup contents or unrelated files
are included. Docker/Immich and SSH hardening remain explicitly pending; Samba
limits and the initial Media connection/reconnect test sequence are preserved.

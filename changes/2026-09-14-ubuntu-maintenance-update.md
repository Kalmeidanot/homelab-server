# Ubuntu Maintenance and Update Pass

Date: 2026-09-14

Status: Completed successfully

## Evidence and Scope

This record documents the completed maintenance sequence and validation confirmed
by the user. This recording task was documentation/Git only: no live-server
changes, sudo commands, package operations, or live health checks were performed
by Codex. Commands below describe the already completed maintenance.

## Reason and Preflight

Apply available Ubuntu and supporting package updates after checking core
services and storage.

- `ssh`, `cockpit.socket`, `smbd`, `docker`, `containerd`, and `tailscaled` were
  active before maintenance.
- `/srv/storage` was mounted read/write as ext4.
- Package information was refreshed with `sudo apt update`.
- `sudo apt -s upgrade` was performed before changes. The simulation showed
  9 packages upgrading, 0 installing, 0 removing, and 0 held back.

## Completed Maintenance

The real package upgrade completed successfully. Updated packages included:

- `containerd.io`
- `dmidecode`
- `docker-buildx-plugin`
- `libaudit-common`
- `libaudit1`
- `libflashrom1`
- `mdadm`
- `sos`
- `tailscale`

The three packages recorded as deferred by phased updates on September 4
(`libaudit-common`, `libaudit1`, and `libflashrom1`) were included in this pass.

apt reported `grub-pc-bin` as automatically installed and no longer required.
`apt autoremove` was NOT run; `grub-pc-bin` was not removed in this pass.

A reboot was required due to `libc6`. This is the reported reboot reason, not
an additional entry in the confirmed nine-package upgrade list. The server was
rebooted with `sudo reboot`.

The separate firmware update remains pending and was NOT performed.

## Post-reboot Validation

- Ubuntu booted successfully and SSH returned.
- Kernel remained `7.0.0-31-generic`.
- LAN IPv4 remained `10.0.0.6`.
- `ssh`, `cockpit.socket`, `smbd`, `docker`, `containerd`, and `tailscaled` were
  active.
- `/srv/storage` was mounted read/write from `/dev/sda1` as ext4.
- `jellyfin` was running and healthy.
- `immich_server` was running and healthy.
- `immich_postgres` was running and healthy.
- `immich_machine_learning` was running and healthy.
- `immich_redis` was running and healthy.
- The final reboot-required check returned `NO REBOOT REQUIRED`.

Outcome: the maintenance pass completed successfully, with the core services,
storage mount, and Docker applications validated after reboot.

## Affected State and Documentation

- Installed Ubuntu/supporting package state, including containerd, Docker Buildx,
  and Tailscale packages.
- Host and service availability across the reboot; `/srv/storage` and Jellyfin
  and Immich container health were checked afterward.
- `CURRENT_STATE.md` now records this completed pass and supersedes the previous
  current-state note about the three deferred packages.
- `runbooks/everyday-commands.txt` was reviewed under the AGENTS.md maintenance
  rule. No update was needed: the confirmed pass did not change operational
  commands, service names, URLs, addresses, storage paths, startup behavior,
  troubleshooting steps, or expected health checks. The supplied checks do not
  establish public Funnel recovery, so its existing validation caveat remains.

## Rollback / Recovery

No rollback was reported as needed; the reboot and post-reboot checks succeeded.
Exact before/after package versions were not supplied, so this record does not
provide a version-specific downgrade procedure. Any future package recovery
requires separate inspection and authorization. Reverting this documentation
commit would only revert the record, not the completed server maintenance.

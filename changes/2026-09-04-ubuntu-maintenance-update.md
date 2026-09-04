# Ubuntu Maintenance and Update Pass

Date: 2026-09-04

Status: Completed

## Reason

Apply available Ubuntu maintenance, kernel, security, Docker, and containerd
updates after confirming that core services and storage were healthy.

## Pre-upgrade Review

- A service and storage health check passed.
- Refreshed package information with `sudo apt update`.
- Previewed the upgrade with `sudo apt -s upgrade` before making changes.
- The dry-run showed 13 packages to upgrade, 7 dependencies/new kernel-related
  packages to install, 0 packages to remove, and 3 packages held back by Ubuntu
  phased updates.

## Changes

- Installed the offered upgrade with `sudo apt upgrade`.
- Updates included Docker/containerd packages and Ubuntu kernel/security packages.
- Rebooted the server with `sudo reboot` when the upgrade reported that a reboot
  was required.
- No firmware update was performed; the separate available firmware update remains
  pending and is not part of this completed maintenance pass.

## Validation

- Ubuntu initially reported 0 immediate updates after the reboot.
- The server successfully booted into `Linux 7.0.0-31-generic`.
- SSH and Cockpit returned successfully.
- `smbd`, `docker`, `containerd`, and `tailscaled` returned active.
- `/srv/storage` automatically remounted read/write as ext4.
- Jellyfin and all Immich containers returned automatically.
- A later `apt update` showed `libaudit-common`, `libaudit1`, and `libflashrom1`
  still upgradable due to phasing. These updates were intentionally not forced and
  should be allowed to roll out normally.

## Known Cockpit Software Updates Issue

Cockpit is operational, but its Software Updates page currently fails with
`Cannot refresh cache whilst offline`. The server is not offline: normal apt
networking and update operations work. This appears to be the known
Cockpit/PackageKit/NetworkManager false-offline behavior on Ubuntu Server.

Do not change the working server networking merely to fix this cosmetic/update-UI
issue. Treat apt as the authoritative update method. Revisit the Cockpit Software
Updates false-offline behavior later as a low-priority backlog item.

## Affected Files and Services

- Ubuntu package state and installed kernel
- Docker and containerd packages
- `smbd`, `docker`, `containerd`, and `tailscaled`
- Cockpit and SSH availability across reboot
- `/srv/storage` automatic mount
- Jellyfin and Immich container autostart

No service, storage, networking, Docker, Jellyfin, Immich, Samba, Tailscale, or
firewall configuration was changed as part of documenting this completed work.

## Outcome

Successful. The server returned normally after the required reboot with its core
services, storage, and application containers operational. The three phased
packages remain intentionally deferred.

## Rollback / Recovery

No rollback was required. If a future kernel update causes a boot problem, use
GRUB to select a previously installed kernel or use Ubuntu recovery media. Package
downgrades should be considered only after identifying the affected package and
reviewing its dependencies. The phased packages require no recovery action.

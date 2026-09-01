# Initial Ubuntu System Updates

Date: 2026-08-31

Status: Completed

## Reason

Apply available Ubuntu updates immediately after the initial operating system installation.

## Actions

- Refreshed Ubuntu package information with `sudo apt update`.
- Reviewed available upgrades with `apt list --upgradable`.
- Installed available standard updates with `sudo apt upgrade`.
- Updated:
  - python-apt-common
  - python3-apt
- Rebooted the server.

## Validation

- Ubuntu rebooted successfully.
- Ethernet returned automatically.
- OpenSSH started automatically.
- Remote SSH login from the main Windows PC succeeded.
- Ubuntu reported 0 immediately available updates after reboot.
- Server was later powered down, physically moved, connected through the new TP-Link TL-SG105E switch, and booted again successfully.
- Remote SSH access still works after the move.

## Outcome

Successful.

The server is verified for unattended boot and headless SSH administration.

## Rollback / Recovery

No rollback was required.

If a future package or kernel update causes a boot problem, recovery may involve selecting an older kernel from GRUB or using Ubuntu recovery media.

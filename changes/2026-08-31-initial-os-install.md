# Initial Ubuntu Server Installation

Date: 2026-08-31

Status: Completed

## Reason

Convert the Lenovo ThinkCentre M70q Gen 3 into the dedicated homelab/NAS server.

## Previous state

The computer was running Windows 11.

## Changes

Installed Ubuntu Server 26.04.1 LTS on the internal SK hynix SSD.

Used a simple non-LVM disk layout.

Configured:

- approximately 1 GB EFI system partition
- remainder of SSD as ext4 root filesystem
- hostname: homelab
- local administrator: kaian
- OpenSSH Server
- password-based SSH authentication during initial setup
- Ethernet networking through DHCP

Ubuntu Pro was skipped.

Optional featured server snaps were not installed.

## Validation

Successful boot from internal SSD.

Successful local login.

Ethernet came online successfully.

Successful SSH connection from main Windows PC to:

kaian@10.0.0.6

## External storage

The WD My Book 12 TB remained disconnected throughout installation.

## Rollback / Recovery

Windows was intentionally erased from the internal SSD.

Returning to Windows would require reinstalling Windows from installation/recovery media.

No user data from the WD My Book was affected.

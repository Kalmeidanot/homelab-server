# Install Cockpit Web Administration

Date: 2026-09-01

Status: Completed

## Reason

Provide a graphical browser-based administration interface for the Ubuntu server.

## Changes

Installed:

- cockpit
- cockpit-files

Enabled Cockpit socket activation with:

sudo systemctl enable --now cockpit.socket

## Access

Cockpit is available on the local network at:

https://10.0.0.6:9090

Authentication uses the Ubuntu user account.

## Validation

- cockpit.socket reports active (listening).
- Browser access from the main Windows PC succeeded.
- Login as user kaian succeeded.
- Cockpit correctly displays:
  - Ubuntu 26.04.1 LTS
  - Lenovo ThinkCentre hardware
  - CPU and memory usage
  - storage
  - networking
  - logs
  - services
  - software updates
  - file browser
  - integrated terminal

## Outcome

Successful.

Cockpit is now the primary graphical administration interface for the Ubuntu host.

SSH remains available for advanced administration and automation.

## Rollback / Recovery

Cockpit can be disabled with:

sudo systemctl disable --now cockpit.socket

Cockpit packages can be removed without removing the underlying Ubuntu server configuration.

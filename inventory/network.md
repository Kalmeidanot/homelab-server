# Network Inventory

Recorded: 2026-08-31

## Ethernet

Linux interface:

eno2

Adapter:

Intel Ethernet Connection I219-LM

Current state:

UP

Current IPv4 address:

10.0.0.6/24

Address assignment:

DHCP

## Wi-Fi

Intel Wi-Fi 6 AX201.

Current Linux interface:

wlo1

Current state:

DOWN

Ethernet is intended to be the normal connection for the server.

## Tailscale

- Hostname: homelab
- IPv4 address: 100.83.35.13
- `tailscaled` is enabled and active
- Installed from Tailscale's official Ubuntu 26.04 Resolute repository
- No exit-node, subnet-router, Tailscale SSH, or Funnel configuration is enabled
- The normal home-LAN IPv4 remains 10.0.0.6

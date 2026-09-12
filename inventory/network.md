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
- No exit-node, subnet-router, or Tailscale SSH configuration is enabled
- Funnel enabled for Jellyfin only on 2026-09-12:
  https://homelab.tail328fad.ts.net/ -> http://127.0.0.1:8096
- CLI configuration/background operation confirmed; public HTTPS TV
  authentication/playback remains pending validation
- Private Tailscale access remains available; Immich and administration services
  are not exposed through Funnel. No router port forwarding was added
- The normal home-LAN IPv4 remains 10.0.0.6

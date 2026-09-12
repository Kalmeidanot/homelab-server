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
- Current Tailscale DNS name: homelab.geep-krait.ts.net; read-only DNS check
  returned `homelab.geep-krait.ts.net.`
- Tailnet DNS suffix renamed on 2026-09-12 to geep-krait.ts.net through the
  Tailscale admin console; machine/server hostname remains homelab
- IPv4 address: 100.83.35.13
- `tailscaled` is enabled and active
- Installed from Tailscale's official Ubuntu 26.04 Resolute repository
- No exit-node, subnet-router, or Tailscale SSH configuration is enabled
- Funnel enabled for Jellyfin only on 2026-09-12, before the DNS rename
- Expected post-rename public URL: https://homelab.geep-krait.ts.net/
- Read-only Funnel status still lists the pre-rename hostname as `Funnel on`;
  local proxy target remains http://127.0.0.1:8096
- Admin console showed `No certificate found` immediately after the rename;
  new-hostname certificate issuance, public HTTPS reachability and external TV
  authentication/playback remain unvalidated
- Exact evidence: changes/2026-09-12-rename-tailscale-tailnet-dns.md
- Private Tailscale access remains available; Immich and administration services
  are not exposed through Funnel. No router port forwarding was added
- The normal home-LAN IPv4 remains 10.0.0.6

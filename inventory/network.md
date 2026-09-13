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
- Public Jellyfin URL: https://homelab.geep-krait.ts.net (no :8096)
- User-supplied validation recorded on 2026-09-13: new DNS/Funnel hostname works;
  `curl -I https://homelab.geep-krait.ts.net` returned `HTTP/2 302`,
  `location: web/` and `server: Kestrel`, confirming public DNS resolution,
  TLS/HTTPS and Jellyfin response through Funnel
- An off-site TV's Jellyfin app successfully connected using this URL; the TV
  does not have Tailscale installed. Video playback through this new public
  Funnel path remains unverified
- After the user reran `sudo tailscale funnel --bg 8096`, Funnel status showed
  both homelab.geep-krait.ts.net and homelab.tail328fad.ts.net as `Funnel on`;
  both use local proxy target http://127.0.0.1:8096. The old hostname remains a
  known stale/legacy entry pending separate deliberate runtime cleanup
- Current evidence: changes/2026-09-13-validate-jellyfin-funnel-after-dns-rename.md;
  the 2026-09-12 rename record preserves the previous pending state
- Private Tailscale access remains available; Immich and administration services
  are not exposed through Funnel. No router port forwarding was added
- The normal home-LAN IPv4 remains 10.0.0.6

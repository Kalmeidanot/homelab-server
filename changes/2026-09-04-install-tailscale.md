# Install Tailscale and Validate Remote Jellyfin Access

Date: 2026-09-04

Status: Completed

## Reason

Provide private off-site access to Jellyfin without intentionally exposing the
service to the public Internet through router port forwarding.

## Changes

- Installed Tailscale from Tailscale's official Ubuntu 26.04 Resolute repository.
- Enabled and started the `tailscaled` service.
- Joined the server to the Tailscale network as `homelab`.
- Assigned Tailscale IPv4 address 100.83.35.13.
- Retained the normal home-LAN IPv4 address 10.0.0.6.

No exit-node, subnet-router, Tailscale SSH, or Funnel/public-exposure
configuration was enabled. Jellyfin port 8096 was not intentionally exposed
through router port forwarding.

## Validation

- A phone joined the same Tailscale network.
- Phone Wi-Fi was disabled so the test used mobile data rather than the home LAN.
- Jellyfin was reached at http://100.83.35.13:8096.
- Jellyfin authentication succeeded.
- Video playback worked correctly.

This formally validates off-site Jellyfin access over Tailscale.

## Affected Files and Services

- Tailscale's Ubuntu 26.04 Resolute APT repository configuration and signing key
- Tailscale package installation
- `tailscaled` service
- Tailscale node registration for `homelab`

Docker, Jellyfin, storage, media, the normal LAN address, and router port
forwarding were not changed as part of the Tailscale configuration.

## Outcome

Successful. Tailscale is the current safe/default remote-access method for
Jellyfin, and remote authentication and playback have been validated over mobile
data.

## Rollback / Recovery

If remote access fails, confirm that the client and `homelab` are connected to the
same Tailscale network, that `tailscaled` is active, and that the server still has
the expected Tailscale address before changing Jellyfin or router configuration.

Removing or disconnecting Tailscale would remove this private remote-access path
but should not affect Jellyfin access through the home LAN at
http://10.0.0.6:8096. Any removal should be treated as a separate server change
and documented before execution.

# Failed Lenovo firmware update and successful server recovery

Recorded: 2026-09-15

Status: Firmware update FAILED; server recovered and is operational. System
Firmware remains 0.1.47 / BIOS M43KT2FA. The firmware issue remains unresolved.

## Evidence and scope

This record uses the incident and recovery evidence supplied by the user. The
record date is the documentation date; exact incident timestamps were not supplied.
The earlier Ubuntu maintenance record preserves its pre-attempt firmware status.
All firmware commands and checks described below are historical observations,
not instructions to execute them now. Codex performed repository/documentation
and Git operations only, with no live-server checks, sudo, reboot, shutdown,
firmware update, firmware-state clearing or other runtime changes.

## Attempt and target release

- Hardware: Lenovo ThinkCentre M70q Gen 3, model 11UD000QMX.
- Tool: fwupd / fwupdmgr; installed fwupd runtime later confirmed as 2.1.1.
- Target: System Firmware, Device ID `758b273ff872574f927cbe4c012d71bd6000ce65`.
- Before attempt: System Firmware 0.1.47; dmidecode BIOS version M43KT2FA.
- Available Lenovo/LVFS release: ThinkCentre M70q-3, ThinkCentre M750q System
  Update; target version 0.1.52, Release ID 148810.
- Reported release characteristics: Lenovo vendor firmware, trusted metadata,
  trusted/signed payload, tested by trusted vendor, and reboot required for
  installation. Security-related fixes included a listed issue CVE-2026-33197;
  reported urgency was Low.

The user intentionally started this available firmware update using the specific
System Firmware Device ID rather than a generic update-all command. The update
was staged and reboot began.

## Failure and recovery sequence

The server did not return normally after staging and reboot:

- No ping response at LAN IPv4 10.0.0.6.
- SSH to 10.0.0.6 and Tailscale IPv4 100.83.35.13 timed out.
- The connected monitor showed no signal.
- The power LED stayed solid white; the Ethernet switch port retained link/activity.
- This state lasted roughly one hour or longer. The user intentionally waited
  instead of immediately forcing power off.

The user eventually pressed the Lenovo power button once. A long press was NOT
required: the machine immediately restarted and subsequently booted normally
into Ubuntu. This records the observed recovery, not a general firmware recovery
procedure or a diagnosis of the stall's cause. No hardware defect is established.

## Recovery validation supplied by the user

- Ubuntu Server 26.04.1 LTS booted successfully.
- Kernel remained Linux 7.0.0-31-generic; LAN IPv4 returned as 10.0.0.6.
- SSH, Jellyfin, Immich and Samba worked again.
- The WD My Book spun up and normal disk activity returned.
- Physical local login was tested once. Later logout/reconnect testing confirmed
  that local console login is NOT required for SSH or normal server services.
- No data-loss symptoms were observed. This is an observation, not a complete
  data-integrity audit.

## Firmware result and conflicting history

Post-recovery `fwupdmgr get-updates` reported for System Firmware:

```text
Current version: 0.1.47
Update State: Failed
Update Error: failed to update to 0: error-unsuccessful
```

The 0.1.52 update remained available. dmidecode still reported `M43KT2FA`.
The update DID NOT install; the machine remained on its previous firmware.

`fwupdmgr get-history` retained stale/conflicting state:

```text
Previous version: 0.1.47
Update State: Needs reboot
Problems: An update is in progress
Target release: 0.1.52
```

`fwupdmgr get-results` for the System Firmware device reported:

```text
Device ... has no results to report
```

`fwupdmgr check-reboot-needed` still claimed an update required a reboot. This
was not trusted as evidence of an active flash: the live firmware state explicitly
showed failure and the machine had already successfully booted. These stale
messages do not establish that another reboot or retry is required.

## Capsule / EFI observations

The user's check found no `/boot/efi/EFI/UpdateCapsule` directory. A broader EFI
search found only `/boot/efi/EFI/ubuntu/fwupdx64.efi`, the normal fwupd UEFI
helper executable. No obvious staged `.cap` firmware payload or UpdateCapsule
directory remained on the EFI System Partition. No firmware state was cleared
as part of this documentation task.

## Current decision and future recovery work

Do NOT retry 0.1.52 through the same fwupd/LVFS capsule path at this time. The
server has recovered, but the firmware update remains pending and its failure
is unresolved. Future firmware work must be a separate deliberate maintenance
task. Before any retry, evaluate Lenovo's alternate vendor-supported BIOS/firmware
update and recovery methods instead of blindly repeating the same capsule update.
No alternate method was evaluated or selected in this task.

The confirmed recovery was one normal power-button press/restart; no firmware
rollback was reported, and firmware remained at 0.1.47 / M43KT2FA. Future recovery
actions require their own inspection and review. Reverting this documentation
in Git changes only the record, not server or firmware state.

## Affected state and documentation review

The incident affected host boot and network/service availability, the System
Firmware update result/history, and availability of the WD My Book during the
stall. Recovery evidence above establishes restored operation within the supplied
checks. This documentation task changed no disks, media, firmware, networking,
storage, Docker, Jellyfin, Immich, Samba, Tailscale, SSH, Cockpit or firewall state.

- Added this detailed incident record.
- Updated CURRENT_STATE.md with concise failed-update and recovery status.
- Updated inventory/hardware.md with the unchanged firmware and deferred retry.
- Reviewed runbooks/everyday-commands.txt under AGENTS.md: added brief notes on
  stale firmware reboot prompts and the confirmed lack of a local-login
  requirement, useful for routine maintenance and startup troubleshooting.
- Reviewed ARCHITECTURE.md and left it unchanged; no architecture change occurred.

Documentation validation: reviewed Git status and the full diff, checked whitespace
with `git diff --check`, and confirmed the record says FAILED and retains firmware
0.1.47 / M43KT2FA. No new reboot/retry requirement is prescribed; future firmware
work remains separate. Only the intended documentation files are included, with
no secrets, credentials, private keys or Codex authentication contents.

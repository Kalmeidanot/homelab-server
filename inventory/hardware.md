# Hardware Inventory

Recorded: 2026-08-31

Firmware status updated: 2026-09-15 (user-supplied recovery evidence).

## Computer

- Manufacturer: Lenovo
- Model: ThinkCentre M70q Gen 3
- Machine type/model: 11UD000QMX
- Motherboard: Lenovo 330B

## Processor

- Intel Core i5-12500T
- 6 cores
- 12 threads

## Graphics

- Intel UHD Graphics 770
- Exposed to the Jellyfin container as /dev/dri/renderD128
- Intel iHD VA-API driver operational inside the official Jellyfin container
- Jellyfin Intel Quick Sync hardware acceleration validated with a real H.264 QSV transcode

## Memory

- 16 GB DDR4-3200 installed
- One 16 GB SO-DIMM currently installed

## Firmware

- BIOS/UEFI: M43KT2FA
- System Firmware: 0.1.47; unchanged after the failed Lenovo 0.1.52 update attempt
- Firmware date: 2025-03-27
- Boot mode: UEFI
- 0.1.52 remains available; retry is deferred pending separate review of
  vendor-supported alternatives to the same fwupd/LVFS capsule path.
- Incident and successful server recovery:
  [failed firmware update](../changes/2026-09-15-failed-lenovo-firmware-update.md).

# Disk Inventory

Recorded: 2026-09-02

## Internal system SSD

Model:

SK hynix HFS256GEJ9X113N

Linux device:

/dev/nvme0n1

Approximate layout:

- /dev/nvme0n1p1 - 1 GB FAT32 - /boot/efi
- /dev/nvme0n1p2 - 237 GB ext4 - /

Root filesystem currently has roughly 214 GB available.

## External storage

WD My Book 12 TB.

Status:

- Initial SMART short and extended tests completed successfully.
- Configured with an ext4 filesystem labeled STORAGE.
- Mounted read/write at /srv/storage.
- Used for bulk storage, including /srv/storage/media and Immich-managed data at
  /srv/storage/photos/immich.

The internal SSD also holds Immich PostgreSQL data at /srv/immich/postgres.

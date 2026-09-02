# Install Docker Engine and Docker Compose

Date: 2026-09-02

Status: Completed

## Reason

Provide the container runtime and Compose tooling for homelab applications.

## Changes

- Installed Docker Engine 29.7.2 from Docker's official Ubuntu repository.
- Installed Docker Compose v5.5.0.
- Enabled the docker and containerd services.
- Kept Docker access restricted to sudo; kaian was not added to the docker group.

## Affected Services

- docker
- containerd
- smbd was checked after installation and remained active

## Validation

- docker service is active.
- containerd service is active.
- The Docker hello-world test completed successfully.
- smbd remained active.
- /srv/storage remained mounted read/write.

## Outcome

Successful. Docker is ready to host Compose applications.

## Rollback / Recovery

Application Compose definitions and persistent application data should be backed
up before Docker packages are removed. Removing Docker packages does not by itself
remove application data under /srv, but package removal and data cleanup should be
treated as separate, explicitly reviewed operations.

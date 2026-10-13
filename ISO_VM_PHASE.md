# Bootable Linux ISO support: implementation checklist

A bootable ISO is not a Python dependency. It needs a virtualization runtime and a host capable of running it.

## Required infrastructure

- Linux server with QEMU/KVM and hardware virtualization enabled (or a supported slower emulation fallback).
- Persistent storage for ISO uploads and virtual disks.
- A provisioning service that creates and destroys VMs.
- An authenticated browser remote-display gateway.
- Resource quotas, monitoring, and a recovery/cleanup process.

## VM lifecycle

1. Authenticate the user and authorize an upload.
2. Enforce maximum upload size, allowed file type, and storage quota.
3. Save the ISO to isolated persistent storage; compute SHA-256.
4. Create a VM with a new virtual disk and strict vCPU/RAM/disk limits.
5. Boot the ISO in QEMU/KVM without host-device passthrough.
6. Publish access only through a short-lived authenticated desktop session.
7. Stop and destroy the VM when the session expires; preserve the virtual disk only if the user has storage quota.
8. Audit the lifecycle and clean up failed/orphaned resources.

## Not safe to implement as a public Flask route

Do not add a route that runs `qemu`, `docker`, `bash`, `subprocess`, or shell commands directly from user-supplied parameters. A web app that accepts arbitrary ISOs or code must delegate provisioning to a tightly restricted worker and validate all inputs. Never expose the hypervisor control socket to clients.

## Free-tier recommendation

Start with the dashboard and repository inspection on a free web host. Keep ISO boot marked **planned** until a compatible virtualization host and secure browser gateway are configured. Do not promise a persistent full desktop from a static site or ordinary free web service.

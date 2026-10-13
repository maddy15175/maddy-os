# MADDY OS Web v2 architecture

## Product goal

Provide a secure browser portal where a user can:
- Sign in and manage workspaces.
- Import a public or authorized private GitHub repository.
- Review README and dependency manifests before building.
- Launch a disposable Linux project workspace with a browser terminal.
- Upload an ISO into a quota-limited VM library.
- Boot a selected ISO in a QEMU/KVM VM with a persistent virtual disk.
- Access a graphical desktop from the browser through a remote-display gateway.

## Recommended split

### 1. Web control plane

- Existing Flask app can evolve into a control API.
- Add authentication before user-specific actions.
- Store metadata in a database (users, workspaces, jobs, ISO metadata, VM state).
- Store uploaded ISOs and VM disks in object/block storage, not in the web service's temporary filesystem.
- Use background jobs for repository inspection, image validation, and provisioning.
- Enforce per-user CPU, RAM, disk, time, and upload quotas.

### 2. Project runner

- Run each imported project in a disposable, unprivileged container or microVM.
- Clone only a validated repository URL; avoid arbitrary URL fetches to prevent SSRF.
- Treat README instructions and requirements.txt as untrusted input.
- Do not automatically run install scripts or arbitrary README commands without an explicit, isolated build step.
- Apply CPU/memory/process/disk/time limits and egress network policy.
- Keep credentials out of the build container.
- Destroy the workspace when requested; persist only explicitly saved files.

### 3. ISO virtualization worker

- Separate Linux host with QEMU/KVM support and hardware virtualization.
- VM per user/session with fixed vCPU, RAM and disk quotas.
- Validate ISO size/type and compute a checksum; do not assume file extension means valid boot media.
- Keep VM images and disks isolated from the host and other users.
- Do not expose QEMU monitor, libvirt, Docker socket, or host SSH directly to the browser.
- Connect through an authenticated gateway (for example, noVNC/SPICE web gateway behind a reverse proxy).
- Require authentication, CSRF protection, secure cookies, rate limits, session expiry and audit logs.

## Deployment phases

1. **Phase 1 — dashboard:** existing Flask app, health checks, UX and documentation. No arbitrary execution.
2. **Phase 2 — repository inspector:** fetch GitHub metadata and README safely; show dependency files and build status. Inspection only.
3. **Phase 3 — isolated project runner:** disposable workspaces on a separate host, only after authentication and isolation are implemented.
4. **Phase 4 — ISO library:** authenticated, size-limited upload to persistent object storage.
5. **Phase 5 — VM service:** QEMU/KVM provisioning, persistent disks, browser desktop gateway, resource quotas and lifecycle controls.
6. **Phase 6 — operations:** monitoring, backup/restore, abuse controls, cleanup jobs and documented incident response.

## Free hosting boundaries

GitHub Pages is static hosting and cannot run a Python backend. A free web service may host the prototype API, but sleep/ephemeral storage and resource limits make it unsuitable for dependable persistent VM hosting. A free tier is reasonable for the control-plane demo; full-time VM execution and ISO storage usually need a separate server or a suitable free compute allocation with explicit limits.

## Acceptance tests before public launch

- User A cannot view or control User B's workspace or files.
- Invalid and private-network repository URLs are rejected.
- Uploads have strict size limits and are not executed on the host.
- Container/VM cannot access host secrets, Docker socket, or other users' storage.
- CPU/RAM/disk/time quotas are enforced server-side.
- Session expiry revokes terminal and desktop access.
- Stopped workspaces and orphaned disks are cleaned up safely.
- Logs never include passwords, access tokens, or session secrets.

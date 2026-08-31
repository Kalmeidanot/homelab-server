# Server Administration Instructions

This repository is the source of truth for this server.

Before making a meaningful server change:

1. Inspect the current state.
2. Understand the reason for the change.
3. Identify affected files, disks and services.
4. Consider rollback or recovery.

After making a meaningful server change:

1. Document what changed.
2. Record important commands or configuration changes.
3. Record affected files and services.
4. Record validation performed.
5. Record the outcome.
6. Record rollback/recovery information where appropriate.
7. Update CURRENT_STATE.md if intended server state changed.
8. Commit relevant documentation and configuration changes to Git.

For destructive operations such as formatting disks, deleting Docker volumes,
changing boot configuration, altering SSH access, changing firewall/network
configuration, or deleting significant data, stop and obtain explicit user
approval before proceeding.

Never commit:

- passwords
- API keys
- access tokens
- SSH private keys
- recovery codes
- encryption keys
- other secrets

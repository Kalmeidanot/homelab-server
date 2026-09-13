# Record the user-installed Jellyfin SmartLists plugin

Date: 2026-09-13

Status: Installed and loaded; verified read-only by Codex. Jellyfin is Healthy.

## Reason

Document the user's completed manual installation of the optional third-party
SmartLists plugin. Its purpose is dynamic/rule-based Jellyfin collections and
playlists, including external-list integration. Intended future uses include
trending/popular collections, curated external lists, and release-related watch
collections such as what to watch before Avengers: Doomsday. These are intentions,
not lists created or providers tested by this task.

- Plugin: SmartLists.
- Project: https://github.com/jyourstone/jellyfin-smartlists-plugin
- Repository manifest:
  https://raw.githubusercontent.com/jyourstone/jellyfin-plugin-manifest/main/manifest.json
- Running Jellyfin server version observed: 10.11.11.
- Installed SmartLists version observed: 12.0.1.0.
- Installed metadata: status Active; target ABI 10.11.0.

The project documents external lists from services including MDBList, IMDb,
Letterboxd, Trakt and TMDb. No particular provider integration was tested here.
Project information describes capabilities; installed state is established by
local runtime evidence below, not by the latest online release.

## A) User action: installation

The user added the third-party repository manifest to Jellyfin and manually
installed SmartLists through Jellyfin's supported plugin-management UI before
this documentation task. Codex did not perform the installation or restart.

## B) Codex action: read-only validation and documentation

Read AGENTS.md, inspected current Jellyfin documentation and recent commits,
and checked Git status before editing. The working tree was clean on main,
in sync with origin/main. Read-only checks:

```sh
curl --fail --silent --show-error http://127.0.0.1:8096/health
curl --fail --silent --show-error http://127.0.0.1:8096/System/Info/Public
```

The health endpoint returned `Healthy`; the public server information endpoint
reported `Version: 10.11.11`. The first sandboxed health attempt could not open
a local socket (`Operation not permitted`); the approved read-only retry outside
the sandbox succeeded. This was a sandbox restriction, not a Jellyfin failure.

Inspected the existing plugin directory and selected non-secret metadata fields:

- Host directory: /srv/jellyfin/config/plugins/SmartLists_12.0.1.0.
- Container directory: /config/plugins/SmartLists_12.0.1.0.
- Binary present: Jellyfin.Plugin.SmartLists.dll.
- meta.json reports SmartLists, version 12.0.1.0, status Active, target ABI 10.11.0.

Inspected /srv/jellyfin/config/log/log_20260913.log, including the latest startup
and subsequent entries through 18:40:04 UTC. Relevant startup evidence:

- 18:31:48.364 UTC: SmartLists assembly version 12.0.1.0 loaded from the plugin
  directory above.
- 18:31:48.479 UTC: `Loaded plugin: "SmartLists" "12.0.1.0"`.
- 18:31:48.797 UTC: storage migration completed successfully; 0 configs and
  0 image folders migrated.
- 18:31:48.825 UTC: SmartLists AutoRefreshService started successfully.
- 18:31:48.860 UTC: auto-refresh cache initialized with 0 playlists and
  0 collections. This startup observation is not an audit of all current objects.
- 18:31:56.365 UTC: Jellyfin reported startup complete.

No SmartLists compatibility or startup errors were found in the inspected
latest-startup log interval. Presence, Active metadata, assembly/plugin load,
and service-start messages confirm installation and successful load; they do
not establish successful rule execution or external-provider operation.

## Relevant messages and limitations

SmartLists logged at informational level that optional Plugin Pages was not
installed, so its user pages are available via direct URL only. No additional
plugin was installed by Codex.

The latest startup also logged ASP.NET warnings about an ephemeral/in-memory
data-protection key repository, no XML encryptor configured, and missing
/wwwroot for static files. These messages were not reported as SmartLists
compatibility failures; their cause and user-visible impact were not established.
Jellyfin completed startup and remained Healthy. No repair was attempted.

No external provider, SmartList rule, collection/playlist generation or plugin
UI workflow was functionally tested. No secrets, raw configuration contents,
credentials or key material are recorded here.

## Scope and affected files

Only CURRENT_STATE.md, ARCHITECTURE.md and this change record were changed.
runbooks/everyday-commands.txt was reviewed and left unchanged: existing health
and log commands remain useful, and no routine command or confirmed UI path
needed adding. Older Jellyfin deployment/change records remain unchanged.

Codex made no runtime/server configuration changes:

- No plugin installation, removal, file modification or configuration changes.
- No Jellyfin restart or Jellyfin/SmartLists configuration changes.
- No SmartList, collection or playlist created or configured by Codex.
- No media files, libraries, metadata, permissions, storage or disks changed.
- Docker and Docker Compose configuration untouched; no image pull or container
  recreation performed.
- Tailscale/Funnel, networking, firewall, router, DNS and certificates untouched.
- Immich and Samba untouched.

The existing Compose definition still declares /srv/storage/media:/media:ro.
SmartLists operates on Jellyfin library/database objects and does not alter the
physical media storage architecture or become a core storage dependency.

## Future rollback/removal

If the user later chooses to remove SmartLists, use Jellyfin's supported
plugin-management UI to remove/uninstall it. Do not manually delete generated
collections/playlists or SmartLists configuration without separate review and
authorization. Media files do not need to be moved, reorganized or deleted merely
because the plugin is removed. No rollback was performed here.

## Documentation QA

Reviewed the full diff and ran `git diff --check`. Only the three intended
Markdown documentation files changed; no runtime/configuration files, plugin
binaries or credentials are included. A final read-only Jellyfin health check
returned `Healthy` before committing. Documentation can be corrected or reverted
in Git without changing server runtime state.

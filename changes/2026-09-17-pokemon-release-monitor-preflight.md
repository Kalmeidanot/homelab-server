# PokemonReleaseMonitor deployment pre-flight

Date: 2026-09-17
Status: BLOCKED before clone; GitHub access restored, but app repository is empty.
Application is not deployed.

## Purpose and intended scope

Run https://github.com/Kalmeidanot/PokemonReleaseMonitor.git (main) as kaian
with Node.js, persistent SQLite/runtime state and a systemd system service.
Only monitor Cardcenter for Pokemon TCG: 30th Celebration under the existing
application rules and send Pushover notifications. No purchasing, checkout,
store login, browser automation or extra infrastructure.

## Inspection and blocker

- Host homelab, user kaian, working directory /home/kaian/nas-admin.
- Kernel: Linux 7.0.0-31-generic, x86_64; Git 2.53.0.
- Node, npm and gh are absent. No OS packages were installed.
- df -h: system filesystem 233G total, 53G used, 169G available (24%).
  /srv/storage: 11T total, 4.2T used, 6.7T available (39%).
- Server-management repository started clean on main, origin
  git@github-homelab:Kalmeidanot/homelab-server.git.
- git ls-remote origin HEAD succeeded. ssh -T identified the existing key as
  the Kalmeidanot/homelab-server deploy key, not an account-wide credential.
- git ls-remote git@github-homelab:Kalmeidanot/PokemonReleaseMonitor.git HEAD
  failed with Repository not found. HTTPS with GIT_TERMINAL_PROMPT=0 also
  failed because authentication was required. Existing access cannot read the app.
- No existing app checkout at the requested location; no existing service unit.
- sudo -n true failed: interactive authentication required.
- package.json could not be read, so Node selection and dependency installation
  are deliberately pending. Ubuntu currently offers Node 22.22.1; user prefers
  compatible Node 24 after inspection.

## Changes actually made

Only new directories on the internal system filesystem:

```sh
install -d -m 755 /home/kaian/apps
install -d -m 700 /home/kaian/.config/pokemon-release-monitor /home/kaian/.local/share/pokemon-release-monitor
```

stat verified owner/group kaian:kaian and modes 755 / 700 / 700 respectively.
Intended checkout: /home/kaian/apps/PokemonReleaseMonitor (not yet created).
Runtime: /home/kaian/.local/share/pokemon-release-monitor (empty, outside Git).
Intended secrets file: /home/kaian/.config/pokemon-release-monitor/env
(not created; no placeholder credentials). No SQLite database exists yet.
No service, autostart, network, firewall, disk, or existing application change.
No secret values were read, printed or committed.

## Resume and remaining validation

User must authorize GitHub access to the app from this server. A supported
interactive option is to install gh via sudo apt install gh, then run
`gh auth login --hostname github.com --git-protocol https --web` as kaian,
signing in as Kalmeidanot, followed by `gh auth setup-git --hostname github.com`.
Use the browser flow; do not paste tokens or passwords into chat. Existing SSH
keys and the server repository SSH remote should remain intact.

After access works, inspect app instructions and package.json, select compatible
Node (prefer 24), clone main, run npm ci / lint / typecheck / test / build.
Prepare a hidden-input Pushover setup command only writing a private env file.
Missing secrets must be entered directly in the terminal, never chat.
Run status and monitor:once with the production runtime; verify baseline and
product count. Run notify:test and verify HTTP 200 / API status 1. Then install
pokemon-release-monitor.service as User=kaian, using verified absolute paths,
EnvironmentFile, network-online.target, Restart=on-failure and RestartSec=15.
System-service installation needs interactive sudo or an authorized execution
path; no sudoers changes are planned. Enable/start only after initial tests.
Observe at least two successful polls and verify persistence and deduplication.

All application QA, Cardcenter discovery, Pushover acceptance, SQLite checks,
systemd active/enabled and stability checks are NOT RUN, not successful.
No application commit or push exists. This record documents preparation only.

## Planned operations and update flow

After deployment, the intended commands are:

```sh
sudo systemctl status pokemon-release-monitor
sudo systemctl stop pokemon-release-monitor
sudo systemctl start pokemon-release-monitor
sudo systemctl restart pokemon-release-monitor
journalctl -u pokemon-release-monitor -n 100 --no-pager
```

They are not yet functional because the unit is absent. App-status environment
loading and final ExecStart must be documented after inspecting the application.
The future update flow is stop the service, verify clean main and correct origin,
git pull --ff-only, npm ci, full QA and build, then start and inspect status/logs.
If QA fails, keep the service stopped until repaired or restore the recorded
previous app commit and rebuild dependencies/output. Never delete runtime state.

## Recovery

Current preparation needs no operational rollback: empty private directories can
remain while deployment waits. No existing data or service was altered.
After eventual systemd installation, deliberate rollback would be:

```sh
sudo systemctl disable --now pokemon-release-monitor.service
sudo rm /etc/systemd/system/pokemon-release-monitor.service
sudo systemctl daemon-reload
```

Do not run this before a unit exists. Preserve runtime data and secrets during
normal rollback; removing a service must not remove its SQLite database.

CURRENT_STATE.md records the pending deployment. The everyday command runbook
records the reserved runtime/config paths and explicitly absent service.

## Follow-up: GitHub access restored, source missing

After the user completed GitHub login on 2026-09-17:

- gh auth status confirmed active account Kalmeidanot and HTTPS Git access.
- gh repo view Kalmeidanot/PokemonReleaseMonitor reported isEmpty=true and
  an empty defaultBranchRef.name; git ls-remote returned no refs.
- git clone --branch main failed with Remote branch main not found in upstream
  origin. No application source is available to inspect or deploy.
- gh is now installed by the user. No Node/npm or additional OS package was
  installed by Codex. sudo -n true still requires interactive authentication.
- User must push the existing Windows application to this repository's main
  branch, excluding secrets and runtime data. Do not create a replacement app
  or an empty main branch merely to pass the clone check.
- QA, Cardcenter, Pushover, SQLite and service/autostart validation remain pending.
  No application code/configuration or existing server service was changed.

The initial access-failure evidence above is historical; the current blocker is
missing source in GitHub. All planned installation and recovery steps remain
pending. Documentation diff/whitespace checks passed for this follow-up.

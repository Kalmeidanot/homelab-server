# PokemonReleaseMonitor homelab deployment

Date: 2026-09-17
Status: Deployed, active and enabled; Pushover accepted and service polls verified.

## Purpose and scope

Monitor Cardcenter continuously for Pokemon TCG: 30th Celebration under the
existing product/language rules and send Pushover notifications. This is only a
release monitor: no purchases, cart, checkout, store login or payment automation.
No browser, Docker, network ports, reverse proxy or database server was added.
Existing homelab services, networking, Tailscale and storage were not changed.

## Application and runtime

- Repository: https://github.com/Kalmeidanot/PokemonReleaseMonitor.git
- Branch: main; deployed source commit e5d1b98af8ae3d65d67c238f45817b8999537d6f.
- Checkout: /home/kaian/apps/PokemonReleaseMonitor, owner kaian.
- Runtime: /home/kaian/.local/share/pokemon-release-monitor, mode 700.
- SQLite: runtime/state.sqlite (WAL), with last-poll.json and logs/monitor.log.
  Files created during baseline are 600, owned by kaian:kaian.
- Production environment: /home/kaian/.config/pokemon-release-monitor/env,
  created only by interactive activation with real keys, mode 600, owner kaian.
- Environment names: PUSHOVER_USER_KEY, PUSHOVER_APP_TOKEN,
  POKEMON_MONITOR_RUNTIME_DIR and NODE_ENV=production. No values of secrets
  belong in this repository. Runtime and config are both outside Git.
- Node.js v24.21.0, npm 11.19.0. package.json requires Node >=24.
- Official Node binary distribution installed at
  /home/kaian/.local/opt/node-v24.21.0-linux-x64 with node/npm/npx symlinks in
  /home/kaian/.local/bin. No version manager or shell-profile change.
- No OS packages installed by Codex. The user installed gh for GitHub access.
  npm ci installed 158 packages; audit reported zero vulnerabilities.

Node installation downloaded the Linux x64 archive and SHASUMS256.txt from
https://nodejs.org/dist/v24.21.0/ and verified the archive with sha256sum -c.
SHA-256: fd8e59d5a511510f6a298afb548f18c7d2b1be404d8b4a27d94fbe49f56cb2d6.
No extra build packages were necessary. npm warned about deprecated
whatwg-encoding and an esbuild install script not covered by allowScripts;
Linux QA and tsx execution succeeded without changing the lockfile or policy.

The earlier access blockers and private-directory creation are recorded in
2026-09-17-pokemon-release-monitor-preflight.md. They are historical: the user
restored GitHub access and pushed the existing Windows source, which cloned
successfully. App worktree remains clean; no app code/config changes or commits.

## QA and first server poll

Passed on Linux: npm ci, npm run lint, npm run typecheck, npm test (56 tests in
2 files), npm run build. No Windows/Linux portability repair was required.

Before permanent startup, used the following production settings with umask 077
and /home/kaian/.local/bin in PATH:

```sh
cd /home/kaian/apps/PokemonReleaseMonitor
export POKEMON_MONITOR_RUNTIME_DIR=/home/kaian/.local/share/pokemon-release-monitor
export NODE_ENV=production
npm run status
npm run monitor:once
```

Initial status was empty. First complete poll succeeded at
2026-09-17T19:25:52.387Z (21:25:52 Europe/Oslo):

- 2,631 sitemap listings discovered; 22 relevant verified products, all sold_out.
- 14 additional candidates blocked by the existing language rules.
- Baseline imported silently; zero notification rows and zero pending notifications.
- No Cardcenter 403, 429, bypass attempt or crash.
- SQLite integrity_check returned ok. Production state/log paths and permissions
  verified. Subsequent status correctly read the persistent baseline.

Pushover keys were absent for this first discovery/baseline pass; the app supports
this explicitly. Real Pushover API acceptance was verified during activation below.

## Systemd configuration and interactive activation

Source unit: systemd/pokemon-release-monitor.service.
Installed target: /etc/systemd/system/pokemon-release-monitor.service.

Runs as User=kaian and Group=kaian, with the app checkout as WorkingDirectory and
the external env file as EnvironmentFile. ExecStart directly executes the built
CLI using the absolute Node binary path; equivalent to npm run monitor, without
requiring an interactive shell or tsx at service startup. Restart=on-failure,
RestartSec=15, UMask=0077, journald output/error. SIGTERM requests graceful stop;
TimeoutStopSec=90 bounds stop time. WantedBy=multi-user.target, with
After/Wants=network-online.target for normal reboot startup.

systemd-analyze verify passed for the unit. It printed unrelated system xfs_scrub
CPUAccounting deprecation warnings; the monitor unit itself had no reported error.
Both helper scripts passed bash -n:

- scripts/pokemon-monitor, installed as /home/kaian/.local/bin/pokemon-monitor:
  defaults to status; supports status, monitor:once and notify:test. Uses Node's
  env-file parser and a fixed PATH, then npm run with production environment.
- scripts/pokemon-monitor-activate: run directly as kaian in a server terminal.
  Uses read -s with tracing disabled, validates non-empty alphanumeric inputs,
  creates env atomically without overwriting an existing file, and enforces 600.
  Only presence/configuration is reported, never secret values.

Single interactive activation command:

```sh
/home/kaian/nas-admin/scripts/pokemon-monitor-activate
```

It runs production status, monitor:once and notify:test before using sudo to
install the unit, daemon-reload, enable and start. The existing application's
notify:test validates both HTTP response and Pushover API status and logs the
accepted HTTP/API statuses. Failure prevents service activation. sudo prompts
in the user's terminal because this Codex session has no noninteractive sudo.
An existing different unit is preserved and requires review before replacement.
An already active service is left alone. No sudoers or SSH-access changes.

Activation and live validation below completed the initially pending checks.
No reboot was performed; enabled state and target dependencies validate the
autostart configuration, not an actual reboot exercise.

## Everyday operations

```sh
sudo systemctl status pokemon-release-monitor --no-pager
sudo systemctl stop pokemon-release-monitor
sudo systemctl start pokemon-release-monitor
sudo systemctl restart pokemon-release-monitor
journalctl -u pokemon-release-monitor -n 100 --no-pager
```

Manual live logs: journalctl -u pokemon-release-monitor -f (Ctrl+C exits logs).
Production app status: /home/kaian/.local/bin/pokemon-monitor
This automatically loads the production environment; no manual secret exporting.
The systemctl commands require completed activation. Never run an extra monitor
alongside the service; the SQLite lock also guards against concurrent monitors.
Built-in logs rotate around 2 MB, retaining one prior file; journald is separate.
If Cardcenter blocks/limits requests, inspect logs and respect app backoff.
Do not bypass access controls or repeatedly force polls.

## Updates

Run as kaian; preserve runtime and env. Check a clean app main/origin before pull.
Record the previous commit for recovery. If any QA step fails, leave the service
stopped until repaired or roll back/rebuild the prior known-good version.

```sh
sudo systemctl stop pokemon-release-monitor
cd /home/kaian/apps/PokemonReleaseMonitor
git status --short --branch
git remote -v
git rev-parse HEAD
# Continue only with clean main and the expected origin.
export PATH=/home/kaian/.local/opt/node-v24.21.0-linux-x64/bin:$PATH
git pull --ff-only && npm ci && npm run lint && npm run typecheck && npm test && npm run build && sudo systemctl start pokemon-release-monitor
sudo systemctl status pokemon-release-monitor --no-pager
/home/kaian/.local/bin/pokemon-monitor
journalctl -u pokemon-release-monitor -n 100 --no-pager
```

Never delete state.sqlite during an update. Review future schema migrations
before upgrading and make a consistent SQLite backup before schema changes.
Node updates are deliberate: verify a new official archive, repeat QA and update
both helper paths and unit ExecStart before reloading/restarting systemd.

## Rollback / recovery

To remove the deployed service deliberately:

```sh
sudo systemctl disable --now pokemon-release-monitor.service
sudo rm /etc/systemd/system/pokemon-release-monitor.service
sudo systemctl daemon-reload
```

Preserve the application checkout, external runtime/SQLite and private environment.
Normal rollback never deletes runtime data. To restore service, reinstall the
tracked unit, daemon-reload and enable/start after validation. Stop the service
before replacing code or restoring a database. A crash can leave a SQLite monitor
lease lasting up to two minutes; wait for expiry instead of deleting state.
For code rollback, use the recorded previous commit in a clean checkout and
reinstall dependencies/build, retaining any local changes and compatible state.
Restoring an older database may affect deduplication; do not reset it casually.

This change affects only files under the application checkout, ~/.local/opt,
~/.local/bin, the dedicated runtime/config directories and (after activation)
the new /etc/systemd/system unit. No other service is restarted.

## Activation evidence

The user ran the activation script in a server terminal. Environment ownership
and mode verified as 600 kaian:kaian; both keys non-empty, production runtime and
NODE_ENV correct (values not printed). A second production monitor:once succeeded
at 2026-09-17T19:30:18.538Z with the same 22 relevant / 14 blocked candidates.
At 2026-09-17T19:30:19.292Z, notify:test logged HTTP 200, API status 1,
accepted=true: a real Pushover test from homelab was accepted. The script then
waited for interactive sudo to install the service. Do not repeat the test merely
to produce another push; API acceptance is established.

## Live service validation

The user's terminal completed sudo installation. The installed unit exactly
matches the tracked unit and is 644 root:root. systemctl reported enabled and
active; User/Group=kaian; Wants/After include network-online.target. First start
was 2026-09-17 21:31:37 CEST. Actual process command uses the pinned absolute Node
binary and dist/cli.js monitor. No shell-profile dependency or root app process.

Two complete consecutive service polls succeeded at 19:32:17.372Z and
19:34:14.745Z, both with 2,631 listings, 22 relevant and 14 blocked candidates.
There were no HTTP errors, 403/429, poll failures, notification failures or
product notifications. NRestarts=0 and process remained active throughout.

The user then exercised stop, start and restart in the terminal because sudo
credentials are not available in the Codex session. Journal confirms a clean
stop at 21:34:18 CEST, start, clean stop/restart at 21:34:19 and a new poll from
PID 745529. Both stops logged Deactivated successfully (no forced kill). The
original baseline_at=2026-09-17T19:25:52.387Z remained intact, while
last_successful_poll advanced; notification rows and pending counts remained zero.

Production app status helper works and loads the correct external runtime/env.
Actual Pushover key values were checked in memory against Git-tracked files in
both repositories: no matches. No key values were printed. Environment mode 600,
config/runtime directories 700, owner kaian:kaian. App remains on its original
clean source commit. No app commit/push or force-push was necessary.

First post-restart poll also succeeded at 19:34:58.434Z with unchanged counts.
Final checks: enabled, active, NRestarts=0, ExecMainStatus=0; SQLite integrity ok;
five successful polls total (two one-shot plus three service polls), zero HTTP /
poll / notification failure events and zero product notification rows. Baseline
remained unchanged across restart. Test push is logged as TEST and is not a
product notification row. Observation covers this deployment window, not future
availability guarantees. Final documentation diff/whitespace review passed.

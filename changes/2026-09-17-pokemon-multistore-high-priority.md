# PokemonReleaseMonitor: multi-store and high-priority alerts

Date: 2026-09-17
Status: deployed and verified in production; all 27 enabled stores completed at least three successful polls.

## Reason and boundaries

Expand direct Norwegian-store coverage for Pokemon TCG: 30th Celebration while
preserving notification-only operation, language filtering, deduplication and
persistent state. No purchasing, cart, checkout, store login or payments. No new
OS packages, browser, Docker, ports, firewall/network or other service changes.

Previous app commit: e5d1b98af8ae3d65d67c238f45817b8999537d6f.
New app commit: e3df485f8fb77221cb4f4b916646a188e138c5fb.
Feature branch: feature/multi-store-monitor, developed in isolated worktree
/home/kaian/apps/PokemonReleaseMonitor-multistore. Feature and main pushed without
force; main fast-forward published while production checkout stayed on the old
commit until the stopped-service deployment. Production checkout:
/home/kaian/apps/PokemonReleaseMonitor. Origin verified as
https://github.com/Kalmeidanot/PokemonReleaseMonitor.git; initially clean.

Runtime remains /home/kaian/.local/share/pokemon-release-monitor (700 kaian).
Environment remains /home/kaian/.config/pokemon-release-monitor/env (600 kaian).
No secrets changed, printed or committed. Node 24.21.0 / npm 11.19.0 unchanged.
Systemd unit/ExecStart/User/network-online dependencies unchanged. Service remains
pokemon-release-monitor.service, built dist/cli.js monitor, kaian, enabled.

## Coverage and architecture

All 44 requested candidates plus 16 extra stores investigated (60 total).
27 enabled, 33 deferred. Full direct evidence, domains, platforms and decisions:
[app STORES.md](https://github.com/Kalmeidanot/PokemonReleaseMonitor/blob/main/docs/STORES.md).

Enabled: Cardcenter, Outland, Pokestore, Collectible, Ringo, Manaheim, Altakube, Game & Trade, Retroworld, Pokelageret, IndigoTCG, LittleM TCG, BoosterKongen, EpiCards, Braspill, Mythic / Cardero, PokeNordic, Maeddiiss / Kortbakeren, Pokebua, Packs of Norway, Cardchimp / Kortjungelen, TCG Norge, Collectors Corner, Pokelink, Kortix, CardSailor, Playlot.

Cardcenter and Shopify specialists use shared sitemap + public product JSON;
Outland uses its own 30th category/product embedded JSON (not local-store stock);
Collectible, Ringo, CardSailor and Playlot use public search + JSON-LD and explicit
online buyability. Real per-store fixtures validate the shared parsers.

High-priority deferred: ARK (no verified complete discovery/stock contract), Norli
(JS shell), Extra Leker (conflicting static stock/button signals). LABOGE's 40k
catalog required 42 requests and is deferred for a narrower discovery surface.
Game Ninja's custom search markup failed closed. Remaining custom-store adapters
need catalog, pagination and online-stock fixtures; all named in app STORES.md.
Verified renames: Maeddiiss→Kortbakeren, Mythic→Cardero, Cardchimp→Kortjungelen.

Polling targets starts every 90 +/- 15 seconds per store, initial starts spread
across 90 seconds (about 3.3 seconds apart for 27 stores). Maximum 3 jobs/HTTP
operations, sequential requests inside each job, >=1 second request spacing.
No per-store overlap. Under load, jobs wait instead of increasing concurrency.
Store failures have independent persistent exponential backoff; Retry-After
respected, no bypass. Structured per-store health/status and snapshots retained.

## Data migration and backup

Consistent SQLite backup taken before work with Python sqlite3.Connection.backup:
/home/kaian/.local/share/pokemon-release-monitor/backups/pre-multistore-20260917T195843Z.sqlite.
Integrity check ok. Research cache: /home/kaian/.cache/pokemon-monitor-research;
validation runtime: /home/kaian/.local/share/pokemon-monitor-validation-20260917,
private and outside Git. These are not used by the production service.

Schema version 0→2 transaction: preserve all Cardcenter products/history/baseline;
prefix IDs with store identity and update notification foreign keys; add
store_id/orderable, store health and scoped metadata. Migration is idempotent,
FK-checked, and refuses to run while an old monitor lease is active. Each new
store's first complete poll establishes its own silent baseline, including open
preorders and existing available products. A newly discovered orderable preorder
after baseline uses one NEW_PRODUCT with explicit preorder-open status; an
already known preorder opening uses PREORDER_OPEN, avoiding two pushes per event.

Deployment script takes another fresh backup after stopping the old service and
writes its exact path/counts/commits to runtime/deploy-multistore.json. It asserts
all old product URL/ID mappings, notification count and Cardcenter baseline are
preserved after migration, then starts systemd. Runtime is never deleted.

## Pushover and QA evidence

All product events use priority=1 and direct product URLs; normal notify:test
remains priority=0. No priority=2, emergency retries or acknowledgements.
Zero/one-NOK prices are unknown; price parsing cannot suppress a stock alarm.
Explicit foreign language markers are blocked; unspecified language is
DEFAULT_OR_UNKNOWN, not verified English.

Passed npm ci, lint, typecheck, 117 fixture-based tests and build on Linux.
All 56 previous tests retained (expected titles updated for requested format).
Tests cover store identity, per-store bootstrap, failed-store isolation, migration
and active-lease guard, all priorities, availability/preorder transitions, price,
language/scope, fixture parsing, staggering/concurrency and backoff.

Isolated live monitor:once with a copy of production state passed all 27 enabled
stores. 27 baselines, zero notification rows, SQLite integrity ok, all 22 relevant
Cardcenter products preserved. No HTTP 403/429 or parser/poll errors. Details:
[app LIVE_VALIDATION.md](https://github.com/Kalmeidanot/PokemonReleaseMonitor/blob/main/docs/LIVE_VALIDATION.md).

Exactly ONE npm run notify:test:high executed at 2026-09-17T20:22:35.554Z from
homelab using the private production credentials and isolated validation log.
Pushover accepted HTTP 200, API status 1, priority 1. No further test push is
needed. Only the user can confirm reception/Time Sensitive presentation on iOS.

## Production switch

Reviewed script (bash -n passed): scripts/pokemon-monitor-deploy-multistore.
The user ran it directly as kaian because this session cannot authenticate sudo:

```sh
/home/kaian/nas-admin/scripts/pokemon-monitor-deploy-multistore
```

It verifies clean main, expected origin and exact old/new commits, fetches,
authenticates sudo, stops only this service, makes the fresh backup, fast-forwards
local main to the reviewed commit, runs npm ci/build, opens status to migrate,
checks preserved records, installs the updated status wrapper, and starts systemd.
No unit change/daemon-reload is needed. Errors keep the monitor stopped and
report recovery instructions; no automatic data deletion/restoration.

## Operations and rollback

Normal systemctl status/stop/start/restart and journalctl commands are unchanged.
`pokemon-monitor` now shows a compact per-store table. The wrapper also accepts
notify:test:high, but the authorized one-off deployment test has already happened.
Future updates: stop service, backup SQLite before schema changes, clean main,
git pull --ff-only, npm ci, full QA/build, start, observe per-store health.
Do not delete the DB or create another production baseline casually.

If deliberately rolling back this release, stop the service first. Version 1
cannot interpret scoped v2 identities, so this specific downgrade DOES need the
pre-migration DB. Archive the current v2 DB before restoring v1; observations
since the backup will not be active under v1 but remain in that recovery archive.
Review clean Git status before changing checkout. No force/reset of local edits.

```sh
sudo systemctl stop pokemon-release-monitor
cd /home/kaian/apps/PokemonReleaseMonitor
git status --short --branch
git switch --detach e5d1b98af8ae3d65d67c238f45817b8999537d6f
export PATH=/home/kaian/.local/opt/node-v24.21.0-linux-x64/bin:$PATH
npm ci && npm run build
```

After confirming the exact backup path from deploy-multistore.json, restore with
SQLite backup API (service stopped), preserving the current v2 state first:

```python
import sqlite3, json, datetime
from pathlib import Path
r = Path('/home/kaian/.local/share/pokemon-release-monitor')
receipt = json.loads((r/'deploy-multistore.json').read_text())
live = sqlite3.connect(r/'state.sqlite')
archive = r/'backups'/('before-rollback-' + datetime.datetime.now(datetime.UTC).strftime('%Y%m%dT%H%M%SZ') + '.sqlite')
assert not archive.exists()
with sqlite3.connect(archive) as saved:
    live.backup(saved)
with sqlite3.connect('file:' + receipt['backup'] + '?mode=ro', uri=True) as old:
    assert old.execute('pragma integrity_check').fetchone()[0] == 'ok'
    old.backup(live)
live.close()
```

Run that restore in a shell with umask 077. Then:

```sh
sudo systemctl start pokemon-release-monitor
sudo systemctl status pokemon-release-monitor --no-pager
/home/kaian/.local/bin/pokemon-monitor
journalctl -u pokemon-release-monitor -n 100 --no-pager
```

Retain both backups, env and runtime. Before returning to main after a rollback,
review the schema/data state and follow a tested upgrade again. Do not restore
an older DB as routine troubleshooting. No rollback has been needed or executed.

## Post-deployment observation

Deployment completed on 2026-09-17; service started at 22:36:27 CEST (20:36:27 UTC).
Production main is the reviewed e3df485 commit. Fresh stopped-service backup:
/home/kaian/.local/share/pokemon-release-monitor/backups/pre-multistore-deploy-20260917T203625Z.sqlite.
Deployment receipt: runtime/deploy-multistore.json (old/new commits, backup,
36 previous product records, zero previous notifications, original baseline).

At 20:42:30 UTC, journald contained 99 successful polls across all 27 stores,
minimum three and maximum four per store. All 26 newly enabled stores logged a
silent baseline; Cardcenter retained 2026-09-17T19:25:52.387Z. No poll errors,
403/429, crashes, restarts, notification attempts or duplicate/bootstrap pushes.
All store health rows are OK without active backoff. Service active/running,
autostart enabled, NRestarts=0. No reboot or additional test push performed.

Production counts match isolated validation: Cardcenter 22, Outland 10,
Pokestore 22, Manaheim 17, Altakube 19, Game & Trade 3, IndigoTCG 2,
LittleM TCG 10, Maeddiiss/Kortbakeren 7, CardSailor 11; the other 17 enabled
stores currently have zero matching products. Total 123 after language filtering.
IndigoTCG reports two available products with placeholder/unknown prices and
unspecified language; six LittleM and seven Kortbakeren preorders are open.
These existing items were silently baselined, not sent as new alerts.

SQLite schema=2, integrity_check=ok, foreign_key_check empty. Every one of the
36 original Cardcenter URL/ID mappings exists after scoping (22 pass language
filter). Original baseline and notification history preserved; notification
rows remain zero. Runtime mode 700, DB/logs/backup/env mode 600, owner kaian.
Runtime and credentials remain outside both repositories.

Resource snapshot after about six minutes: systemd memory about 301 MiB,
peak 314 MiB; 19.1 cumulative CPU seconds, process CPU average about 5.3% of
one core. SQLite main file 8.9 MiB, WAL about 4.8 MiB, application logs 475 KiB.
These are startup/observation measurements, not long-term capacity guarantees.
No infrastructure, dependency, OS package or systemd unit changes were needed.
The unit's old descriptive Cardcenter label remains cosmetic; the process now
runs the 27-store registry. Operations wrapper and status work with production env.

CURRENT_STATE.md and runbooks/everyday-commands.txt updated. App feature/main
and server documentation pushed through verified origins without force. Final
tracked-file secret-value scan passed without displaying any credentials.
Rollback is documented above with the actual fresh backup; not needed/executed.
Recommended next research wave: ARK/Norli/Extra Leker stock/discovery contracts,
then Cardstore/MaxGaming and a narrower LABOGE collection source.

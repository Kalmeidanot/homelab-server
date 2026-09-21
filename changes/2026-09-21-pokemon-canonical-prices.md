# PokemonReleaseMonitor canonical identity and cheapest-price CLI

Date: 2026-09-21. Status: deployed without restart at 19:05:16 UTC; post-checks below.

## Purpose and affected paths

Add conservative canonical IDs and read-only cheapest/complete price views for
same 30th Celebration products, without price alerts, shopping, web dashboard or
changes to the continuously running 32-store monitor.

- Old app / rollback: `9cc913ac8860cd4c0dd6d1451f4cc979a972c354`.
- New reviewed app: `18fd2bf4b87bc926d96d2591d2371a50c233bb0d`.
- Feature branch `feature/canonical-prices`, isolated worktree
  `/home/kaian/apps/PokemonReleaseMonitor-prices`. Feature/main pushed without force.
- App checkout `/home/kaian/apps/PokemonReleaseMonitor`.
- Runtime `/home/kaian/.local/share/pokemon-release-monitor`, existing SQLite schema 2.
- Server wrapper source `scripts/pokemon-monitor`, installed to
  `/home/kaian/.local/bin/pokemon-monitor` (kaian-owned).
- New exact deploy script `scripts/pokemon-monitor-deploy-prices`.

Preflight: clean main at 9cc913a, active/running/enabled, PID 1750225, NRestarts=0.
`npm run status` checked via wrapper. SQLite integrity=ok; 489 products, 344
notifications, 160 metadata rows and 57,532 sightings. PokeNordic had the existing
HTTP 429/backoff; other 31 enabled stores healthy. Consistent private development
snapshot saved to ~/.cache/pokemon-prices/preflight.sqlite. No state reset.

The running dist entrypoint and shared modules were left unchanged during tests.
Two source files were initially written in the primary checkout due to a command
working-directory error, immediately moved to the worktree and restored exactly
from HEAD. No build, running module, service PID or production state was affected.
Subsequent development/QA was in the separate worktree.

## Model and audit

22 maintained canonical products, anchored full-title rules and separate variants
in config/canonical-products.json; existing family/set/language classification
reused unchanged. URLs corroborate but cannot override conflicting or obfuscated
titles. Services, assorted variants, case/display quantities, mixed products and
conflicting copied handles fail closed. IDs are derived on read, no migration.

At 19:01:43 UTC: 489 persisted listings, 144 mapped, 242 unmapped individual-card
rows, 50 review-required, 53 excluded non-English. 20 canonical products occur
at 2+ stores. Counts include retained historical rows, not just current URLs.
All groups, prices, statuses, direct links and unassigned rows are in app
`docs/PRICE_AUDIT_2026-09-21.md`; model/rules in `docs/CANONICAL_PRICES.md`.

NOK product prices >1 only; unknown/invalid/placeholders cannot win. Shipping is
excluded. Observed includes sold_out/coming_soon/closed preorder, but needs fresh
listing evidence. Actionable also requires orderable + available/open preorder and
no store error. Product and store timestamps must match and be <=10 minutes old.
Removed/absent listings cannot retain an eligible stale price. Unknown language
stays DEFAULT_OR_UNKNOWN; explicit English is separately labelled. Null source
prices cannot distinguish historical parser rejection from missing values.

Only 14 targeted public .js reads for price/variant uncertainty, spaced >=1 second.
Twelve returned one default variant; two retained Braspill ex-box URLs returned
404 and remain non-ranking unavailable. No full scrape or transactional endpoint.
SQLite lacks full variant arrays/GTIN/descriptions; hidden options absent from
persisted title/URL remain a documented limitation, not a claim of SKU certainty.

Examples at audit time (NOK, excluding shipping):

| Product | Observed | Actionable |
| --- | --- | --- |
| ETB | MaxGaming 899, sold out | Pokestore 2499, available |
| Binder | MaxGaming 649, sold out | LittleM 1449, open preorder |
| Poster | MaxGaming 349, sold out | LittleM 999, open preorder |
| Booster Bundle | Cardstore 474, coming soon | none with valid fresh price |
| Greninja ex Box | Outland 439, sold out | LittleM 999, open preorder |
| Sylveon ex Box | Outland 439, sold out | Pokestore 999, available |

## QA and deployment method

npm ci, lint, typecheck, **236 tests** and build passed (142 existing + 94 new).
Includes captured production title/URL fixtures; read-only CLI against an active
lock and retained notification; unsupported schema rejected without migration.
No notifier instantiation in the price branch; no environment/secret file loading.
No HTTP from CLI. SQLite opened readOnly/query_only in a consistent transaction.

Safe adaptation of the existing exact-target deployment pattern for side commands:
verify clean main, reviewed origin and ancestry; verify all monitor/shared modules,
config and dependency lock unchanged; build in worktree; byte-compare existing
shared dist modules; online SQLite backup/integrity; fast-forward local main;
atomically install prices.js, cli.js and wrapper; verify unchanged active PID.
No sudo, service restart or production npm ci required (dependencies unchanged).
Deploy script and wrapper passed bash -n. Runtime receipt: deploy-prices.json.

```sh
/home/kaian/nas-admin/scripts/pokemon-monitor-deploy-prices
pokemon-monitor cheapest
pokemon-monitor cheapest etb
pokemon-monitor prices binder
pokemon-monitor prices --json
```

## Rollback without stopping monitor

This release only adds side commands. Preserve runtime, database, WAL and histories.
If rollback is needed, as kaian, first require a clean checkout and inspect the
receipt `~/.local/share/pokemon-release-monitor/deploy-prices.json` for the exact
backup directory. Restore the saved pre-price wrapper and built cli.js by copying
to a temporary file beside each destination, then `mv` atomically into place.
Restore wrapper mode 755. Switch the clean app checkout to detached 9cc913a:

```sh
cd /home/kaian/apps/PokemonReleaseMonitor
git status --short
# Proceed only if clean; retain runtime/state.
price_backup=/home/kaian/.local/share/pokemon-release-monitor/backups/pre-prices-20260921T190516Z
install -m 755 "$price_backup/pokemon-monitor" /home/kaian/.local/bin/pokemon-monitor.rollback
mv /home/kaian/.local/bin/pokemon-monitor.rollback /home/kaian/.local/bin/pokemon-monitor
install -m 644 "$price_backup/cli.js" dist/cli.js.rollback
mv dist/cli.js.rollback dist/cli.js
git switch --detach 9cc913ac8860cd4c0dd6d1451f4cc979a972c354
systemctl is-active pokemon-release-monitor.service
```

The extra unused dist/prices.js may remain; the old CLI cannot invoke it. Do not
restore the database backup for this code-only rollback. Do not run npm ci/build
in production while the monitor is active; shared modules are already byte-identical.
A later change to monitor dependencies/schema needs the normal stopped deployment.
No rollback was executed.

## Deployment and post-check outcome

Deployed **2026-09-21 19:05:16 UTC**, receipt status installed_without_restart.
Backup directory: `/home/kaian/.local/share/pokemon-release-monitor/backups/pre-prices-20260921T190516Z`
(mode 700, SQLite mode 600). Receipt mode 600. Main is clean at 18fd2bf, matching
origin/main. Shared modules compared byte-identically before atomic installation.
No package reinstall, service/unit/OS change, sudo, restart or migration in production.

Verified **2026-09-21T19:07:17.924755+00:00**:

- Service active and autostart enabled; PID **1750225** and start time unchanged
  (18:20:18 UTC from previous phase). **NRestarts=0**.
- All **31 previously healthy enabled stores completed a successful poll after
  deployment**. PokeNordic retains its pre-existing HTTP 429/backoff; no new store
  errors, parser errors or notification failures during post-deploy observation.
- SQLite integrity_check=ok, foreign_key_check empty, schema=2. All **489 existing
  product IDs/URLs/first-seen timestamps**, **344 notification rows** and **32 store
  baseline timestamps** compared with backup and preserved. Product count remains
  489. All notification rows are also byte-for-value identical to the phase's
  earlier preflight snapshot: no new rows, status changes or retry attempts.
- `pokemon-monitor cheapest`, `cheapest etb`, `prices binder` and `prices --json`
  ran successfully against production. Results reproduce the 22/144/242/50/53
  audit counts and 20 products at 2+ stores. Existing status path unchanged.
- No push/test alert/price notification was sent. No scraping occurs in the
  installed commands; checks used the existing monitor observations.

Useful working evidence (outside Git): ~/.cache/pokemon-prices/postcheck.json,
deployed-cheapest.txt, deployed-binder.txt, deployed-audit.json. Full public product
and mapping evidence is committed in the app audit; no secrets are in either repo.

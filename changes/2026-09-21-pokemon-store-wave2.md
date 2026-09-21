# PokemonReleaseMonitor: second production store wave

Date: 2026-09-21.
Status: first switch completed at 18:10 UTC; follow-up scheduler fairness fix
prepared after production observation exposed delayed polls. Final three-cycle
observation remains pending the exact-target follow-up deployment.

## Purpose and commits

Enable only robust candidates from ARK, Norli, Extra Leker, Cardstore, MaxGaming
Norway and LABOGE for Pokémon TCG: 30th Celebration. No purchasing, cart/checkout
requests, login, payment, browser, anti-bot bypass, price comparison or social monitoring.

- Old app / rollback: `e3df485f8fb77221cb4f4b916646a188e138c5fb`.
- First deployed app: `371e7be04c642c734c0e524b540b10b3b3f69aba`.
- Final reviewed app: `9cc913ac8860cd4c0dd6d1451f4cc979a972c354`.
- Branch `feature/store-wave2`, separate worktree
  `/home/kaian/apps/PokemonReleaseMonitor-wave2`.
- Feature branch pushed, remote main advanced by verified fast-forward without
  force. Production checkout remains old main until the service is stopped by
  the exact-target deployment script.
- App remote verified: https://github.com/Kalmeidanot/PokemonReleaseMonitor.git.
- Server-management remote verified: Kalmeidanot/homelab-server (existing SSH alias).

Affected: app checkout/config/dist, existing persistent runtime, this dated record,
CURRENT_STATE.md, runbooks/everyday-commands.txt, scripts/pokemon-monitor-deploy-wave2.
No systemd unit, secrets, OS dependencies, ports, other services or schema changes.

## Before state

Clean main at old commit; service active since 2026-09-17, enabled, NRestarts=0.
SQLite schema=2, integrity_check=ok, foreign keys intact; no database reset.
At initial status, 26 stores healthy and **PokeNordic already in HTTP 429 backoff**.
Existing backoff is retained. Do not attribute that store's later errors to this wave.

Disk: 167 GiB available / 25% used. Initial service RAM ~404 MiB (then ~405 MiB),
pre-deploy sampled CPU 3.54% of one core over 154 seconds. SQLite main 9,580,544 B
(~9.14 MiB), WAL 5,294,232 B, SHM 32,768 B. Application log 957,409 B plus rotated
2,000,131 B at sampling. Earlier rollout reference was 301 MiB / 5.3% one core;
use today's before/after values as well as that historical reference.

Runtime: `/home/kaian/.local/share/pokemon-release-monitor`.
Research/live cache: `/home/kaian/.cache/pokemon-wave2` (private, outside Git).
No notifier credentials loaded into research/validation; production env untouched.

## Decisions and methods

New enabled: **Norli, Extra Leker, Cardstore, MaxGaming Norge, LABOGE**.
Resulting config: 32 enabled / 28 deferred out of the existing 60-store registry.
ARK remains **DEFERRED**.

| Store | Relevant allowed | Discovery and online contract |
| --- | ---: | --- |
| ARK | Unknown (0 observed on partial surface) | Samlekort 35/35, Pokémon brand 48/78. Next server actions load additional pages; GET page=2 still page 1. 35 product-sitemap shards are unsuitable for this polling budget. Online/store split verified, complete economical discovery and target fixtures not verified. |
| Norli | 5 | Public unauthenticated GET GraphQL category 5191 (68 products/1 request), complete totals/pagination. is_salable + positive online netshop message and stock; IN_STOCK alone insufficient. |
| Extra Leker | 0 | Pokémon brand category, 265 listings/8 pages. Explicit product online stock + matching SKU control/validation initializer. Physical stock never used. |
| Cardstore | 20 | Verified www.cardstore.no, Shopify-backed custom SSR; 2 product sitemaps, direct HTML, JSON-LD plus availableForSale selected variant and enabled control. 23 requests. |
| MaxGaming Norge | 7 | www.maxgaming.no/no paths, NOK offers; index + one sitemap filtered to set URLs + 10 products (12 requests). sid_1/På lager/InStock agreement; sid_8 active control/Forhåndsbestille opens preorder; sid_10 watch-only is sold_out. |
| LABOGE | 10 | title:30th search excluding Singles product type, total checked (14 listings), 10 product .js details/11 requests; global matching/language and Shopify parser unchanged. |

ARK control World Cup booster: 39.90 NOK, JSON-LD InStoreOnly, online unavailable,
local store inStock, isPurchasable=true. No IN_STOCK should be inferred. Its public
DiscoveryView bundle and embedded state confirm build-specific server actions for
paging. Robots-disallowed search/elastic endpoints were not queried. No ARK baseline.

Extra Leker: available Abyss Eye 79.90 NOK has 14 physical stores, static disabled
button and analytics data-quantity-max=0. Public validate-product initialization
removes disabled; quantity analytics are not the online inventory. Negative Pitch
Black 69.90 NOK is explicitly Utsolgt på nett with **3 physical stores**, no purchase
control. Both fresh post-test controls and fixtures passed. Product `.stock` online
indicators must agree. No transaction was attempted to test purchaseability.

Norli: four 30th products have IN_STOCK but is_salable=false; no false stock alert.
One 30th Tech Sticker is coming_soon. Cardstore future-stock labels are coming_soon,
not preorder-open. LABOGE Binder is a closed preorder with placeholder/unknown price.
No allowed target product was available or open preorder during live validation.
MaxGaming has 3 blocked foreign-language target products, including 2 open Japanese
preorders, which never enter the notification stream. Counts after language filtering
sum to 42. Full direct product URLs/prices/statuses in app docs/WAVE2_VALIDATION.md.

## QA and isolated live validation

npm ci, lint, typecheck, **142 tests**, build passed. Original 117 tests retained.
Fixtures include actual public-data parsing per store, complete discovery, prices,
available/sold-out/preorder/unknown, wrong set, language blocks, and independent silent
baselines. Extra physical-online discrepancy and Norli GraphQL contract are explicit.
55 captured discovery-response excerpts; no live network in test suite.

Each new adapter ran a complete isolated live discovery after parser fixtures.
New separate SQLite baselines: integrity ok, zero notification rows; applying the
same result again also generated zero rows. No production DB write during validation.
Fresh positive/negative controls verified separately. No candidate HTTP 403/429 storm.
MaxGaming initially failed closed on unrelated SCART URL substring and missing
optional metadata; both fixed and retested before activation. No partial baseline.

Global matching/language, notifier, state, existing adapters, dependencies and
Pushover config are unchanged. Scheduler fairness was changed only after measured
production starvation; see the observation below. All product events remain priority=1. No test push.
90 +/- 15 seconds per store, max three jobs, >=1 second sequential request spacing,
stagger over 90 seconds (~2.8 seconds/store). Existing failure isolation/backoff reused.
The five stores add 55 requests per observed full round; no startup burst introduced.

## Exact deployment

Reviewed script: `scripts/pokemon-monitor-deploy-wave2` (`bash -n` passed).
Run as kaian in a terminal:

```sh
/home/kaian/nas-admin/scripts/pokemon-monitor-deploy-wave2
```

`sudo -n -l` confirmed interactive authentication is required. The script obtains
sudo in the user's terminal; no password is requested by Codex. It verifies clean
main, origin, exact old/new commit and fast-forward ancestry before stopping only
pokemon-release-monitor.service. Then consistent SQLite backup + integrity/FK checks,
merge --ff-only, npm ci/build, persistence checks and start. Failure leaves the
service stopped with explicit rollback directions. A completed target is not rerun.

Fresh backup path/counts/timestamps go to runtime/deploy-wave2.json. No schema
migration. No restoring/deleting data during normal deployment or rollback.

## Rollback (same schema, retain current runtime)

If required, as kaian in a terminal:

```sh
sudo systemctl stop pokemon-release-monitor.service
cd /home/kaian/apps/PokemonReleaseMonitor
git status --short
# Continue only with a clean checkout.
git switch --detach e3df485f8fb77221cb4f4b916646a188e138c5fb
PATH=/home/kaian/.local/opt/node-v24.21.0-linux-x64/bin:$PATH npm ci
PATH=/home/kaian/.local/opt/node-v24.21.0-linux-x64/bin:$PATH npm run build
sudo systemctl start pokemon-release-monitor.service
/home/kaian/.local/bin/pokemon-monitor
```

Keep runtime/state.sqlite, its WAL, logs, env and backups. Both versions use schema 2;
old code ignores the five additions and preserves all data. Do not use the old
single-store schema rollback/restore procedure for this wave. Returning to main must
also stop service before switching/building; review the intended commit first.
Rollback has not been executed.

## Post-deployment observation

Follow-up deployment pending. Required: >=3 successful polls per addition, service
active/enabled, NRestarts, all old-store health, zero new-store bootstrap/duplicate
notifications, no new 403/429/parser storm, SQLite integrity/FK and resource snapshot.
Record actual receipt/backup/service start and results below before calling deployed.

### First switch and scheduler correction

User ran the initial script; service started 2026-09-21 18:10:18 UTC on 371e7be.
Backup: runtime/backups/pre-wave2-20260921T181016Z.sqlite; 442 original product
records and 340 notification records preserved, no schema migration. All five new
stores imported exactly one silent baseline. No new-store notifications or errors.

Production observation exposed fixed-array-order scheduler starvation under load:
Norli's first poll started 127 seconds after service start; Cardstore's first poll
started 214 seconds after start. Norli/Extra then waited over three minutes while
earlier stores repeatedly got free slots. This is the concrete reason a scheduler
change became necessary. Final scheduler selects **oldest due time** before starting
one job per second; concurrency=3, stagger, jitter, backoff and no-overlap unchanged.
A saturation regression test exercises continuous scheduling, not only once mode.
All 142 tests/lint/typecheck/build passed before publishing the fix. App feature and
main updated by fast-forward. No changes experimented on the running checkout.

Updated exact-target script accepts e3df485 or the intermediate 371e7be, archives
the first deployment receipt, takes another consistent backup and deploys 9cc913a.
Final observation must restart its three-cycle count after this service restart.
Both restarts are planned deploys; NRestarts counts automatic failure restarts.

# PokemonReleaseMonitor: second production store wave

Date: 2026-09-21.
Status: deployed and verified at 2026-09-21T18:27:10.972195+00:00. All five additions completed
at least three successful polls after the final scheduler-fairness restart.

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
  force. Both production updates used the stopped-service exact-target script;
  final checkout is clean main at 9cc913a.
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

Final verified observation follows the first-switch history below.

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
Final observation restarted its three-cycle count after this service restart.
Both restarts are planned deploys; NRestarts counts automatic failure restarts.

### Final deployment and verified outcome

Final app **9cc913ac8860cd4c0dd6d1451f4cc979a972c354**, clean main, matching origin.
User ran the updated script; service start **2026-09-21 18:20:18 UTC**. New backup:
`/home/kaian/.local/share/pokemon-release-monitor/backups/pre-wave2-20260921T182016Z.sqlite`.
Second receipt records 487 products / 340 notifications / schema 2 before restart.
First receipt is archived as runtime/deploy-wave2-371e7be.json; current receipt is
runtime/deploy-wave2.json. Both backups/receipts retained, mode 600 under private runtime.

Verified at 2026-09-21T18:27:10.972195+00:00: service active, autostart enabled, **NRestarts=0**.
Two planned deploy restarts occurred (adapters, then measured fairness correction);
there were no automatic crash restarts.

| Added store | Successful polls after final restart | Observed start intervals (seconds) |
| --- | ---: | --- |
| norli | 3 | 99.1, 115.1, 103.1 |
| extra-leker | 3 | 100.1, 102.1, 88.1 |
| cardstore | 3 | 108.1, 102.1 |
| maxgaming | 3 | 105.1, 96.1, 102.1 |
| laboge | 3 | 109.1, 95.1, 100.1 |

Completed-poll counts were captured at 18:26:09 UTC; start intervals include
additional starts through the final 18:27:10 UTC integrity verification.

Exactly five silent baselines were imported in the first deployment, including
Extra Leker's verified empty target set. The final restart imported none again;
all original and new baseline timestamps are preserved. New-store notification
rows remain **zero**, and the full notification history remains **340**, so there
were no baseline pushes or duplicate notifications during either observation.
All 442 pre-wave product IDs/URLs/first-seen values and all 340 prior notification
rows were compared with the initial SQLite backup and remain intact. Current
products total 487: 42 allowed additions and 3 language-blocked MaxGaming entries.
Schema remains 2, integrity_check=ok, foreign_key_check empty. No migration/reset.

All 26 previously healthy stores also completed successful polls after the final
restart. PokeNordic remains the pre-existing HTTP 429/backoff exception (last good
poll 17:35 UTC); it was not retried during this observation because its persistent
backoff extends to 18:29 UTC. No newly failed store, parser mismatch, 403/429 storm,
timeout or notification failure was logged during final observation.

Target remains 90 +/- 15 seconds, concurrency three, stagger and request spacing
unchanged. Actual intervals above include waiting for capacity, so they can exceed
105 seconds. Oldest-due scheduling eliminated fixed-order starvation: initial
Cardstore start fell from 214 seconds to 97 seconds, MaxGaming to 101 seconds.
No claim is made that the target interval is a hard deadline under workload.

Resource snapshot: service RAM **363.78 MiB**; sampled CPU
**5.67% of one core** during final observation. Compare initial
rollout 301 MiB / 5.3% and this phase's before state ~404 MiB / 3.54%. No dramatic
CPU/RAM increase was observed; this is a short observation, not a long-run bound.

| Runtime file | Bytes | MiB |
| --- | ---: | ---: |
| state.sqlite-wal | 4680352 | 4.46 |
| state.sqlite-shm | 32768 | 0.03 |
| state.sqlite | 12886016 | 12.29 |
| monitor.log | 1061254 | 1.01 |
| monitor.log.1 | 2000131 | 1.91 |

SQLite grew from 9.14 MiB to about 12.29 MiB, principally retained sightings from
MaxGaming's Norwegian sitemap; application logs remain under the existing rotation
limit. Current CPU/RAM and data integrity need no OS/service configuration changes.

QA: npm ci, lint, typecheck, 142 tests and build passed; actual isolated/public
validation and final production observation both passed. Pushover priority=1 and
credentials unchanged; no test alert. Runtime permissions and backup mode checked.
Rollback target remains **e3df485f8fb77221cb4f4b916646a188e138c5fb**, preserving the
current schema-2 database. No rollback was required or performed.

App evidence: [store decisions](https://github.com/Kalmeidanot/PokemonReleaseMonitor/blob/9cc913ac8860cd4c0dd6d1451f4cc979a972c354/docs/STORES.md)
and [methods, product URLs/prices/statuses](https://github.com/Kalmeidanot/PokemonReleaseMonitor/blob/9cc913ac8860cd4c0dd6d1451f4cc979a972c354/docs/WAVE2_VALIDATION.md).

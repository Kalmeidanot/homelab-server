# PokemonReleaseMonitor: global opening-service exclusion

Date: 2026-09-21. Status: implemented, tested and published; awaiting the user's
interactive deployment command. Production has not yet been restarted or changed.

## Purpose and exact commits

The user never wants Rip & Ship/live-opening/break services. Exclude them globally
from relevance, online availability, preorder, all three existing notification
types and canonical price views. Preserve real sealed choices on mixed pages.

- Production app / rollback: **18fd2bf4b87bc926d96d2591d2371a50c233bb0d**.
- Reviewed new app: **e54abfca13e27b03cc470cd7e517b76a3441856a**.
- Branch: feature/opening-exclusion, worktree
  /home/kaian/apps/PokemonReleaseMonitor-opening.
- Feature/main published through non-force fast-forward. Production checkout
  remains clean main at 18fd2bf until the stopped-service script advances it.
- App: /home/kaian/apps/PokemonReleaseMonitor.
- Runtime: /home/kaian/.local/share/pokemon-release-monitor.
- Service: pokemon-release-monitor.service. No unit, OS, scheduler, store enablement,
  Pushover configuration, credential or dependency changes.

## Preflight and evidence

Clean main; active/running and enabled, PID 1750225, NRestarts=0.
Status checked via npm wrapper; SQLite schema 2, integrity/FK OK. Snapshot:
490 product rows, 346 notification rows, 160 metadata entries, 32 store baselines.
PokeNordic already had HTTP 429/backoff; remaining 31 enabled stores healthy.
Private consistent preflight copy: ~/.cache/pokemon-opening/preflight.sqlite.
All development/test work was in the separate worktree while production ran.

State audit: **16 explicit services**, across Collectible (3), Braspill (4),
Kortbakeren/Maeddiiss (4), Cardero/Mythic (2), LABOGE (2), Kortjungelen/Cardchimp (1).
Fifteen RIP_AND_SHIP/live listings and one Japanese Box Break (already language
blocked). Historical Pokebua Evolving Skies fixture also confirms BOX BREAK usage;
it is outside the target set and does not add a current 30th service listing.

37 bounded, sequential public checks including fresh post-test controls:
22 successful responses, 13 removed URLs (404), two Cardero 403s. No auth, browser,
transactional endpoint, bypass or retry after the Cardero controls. No new catalog
scrape. No Pushover keys loaded or audit notifications sent. Exact public titles,
URLs, outcomes and limitations are in app docs/OPENING_AUDIT_2026-09-21.md.

No mixed sealed/opening variant array confirmed in the checked responses. Actual
normal Kortbakeren character-option products contain optional opening marketing;
that wording must not block the normal product. Fresh checks verified LABOGE ETB
(Live) blocked, ordinary ETB retained and Kortbakeren Tech Sticker preorder retained.
Unfetched/failed pages are not claimed fully variant-audited.

## Shared policy and persistence

src/purchase-mode.ts normalizes case, accents, whitespace, URL escapes, nested
HTML ampersands, punctuation and rip/and/n/ship spellings. Strong opening/service
and contextual box-break/live-break/break-spot wording block; bare live/break,
TCG Live code cards and optional marketing do not. Variant evidence outranks title;
URL path is considered, never hostname/query or storefront footer text.

SEALED / RIP_AND_SHIP / BREAK_SERVICE / UNKNOWN / REVIEW_REQUIRED plus evidence.
Shopify mixed variants use only explicit sealed choices for stock/orderability/price;
sold-out sealed + available opening stays sold_out. Unknown sealed choice requires
review; aggregate available/minimum price cannot override filtered variants.
HTML option labels without a complete per-option stock/price matrix fail closed.
Multiple eligible sealed variants remain ambiguous for canonical price matching.

The price-only regex was removed; all paths share the same purchase policy.
Product parser, state apply/read and monitor result boundaries enforce exclusion.
Notifier code/config unchanged. Services never enqueue NEW_PRODUCT, IN_STOCK or
PREORDER_OPEN, and old pending service events are cancelled. Normal price output
hides services; prices --json retains non-orderable, null-price excluded audit rows.

No schema change: purchase_mode:<product-id> JSON uses existing metadata.
Idempotent startup reclassification marks old service rows irrelevant, unknown
availability, non-orderable, no comparable price. Product rows/first-seen/URLs,
all sent history and store baselines remain. Re-eligibility of an existing policy-
blocked row is silent; subsequent genuine sealed transitions notify normally.

Known pure-service details with unchanged catalog titles are rechecked daily,
not every 90 seconds. Catalog discovery remains normal. Mixed/review listings
continue normal polling. New sealed options under unchanged service titles may
therefore be delayed up to 24 hours. Missing public variant data is held for review.

## QA and isolated state validation

npm ci, lint, typecheck, **319 tests**, build passed (236 existing retained,
83 additional; old expected results updated only for intentional exclusion).
Captured pure services/normal/optional marketing; controlled mixed variants;
all spelling variants, break context, price/notification boundaries, old pending
cancellation, sent history preservation, restart metadata, daily discovery cache.

Against a copy of production SQLite: two reclassification passes returned 16;
490 products / 346 full notification records / 32 baselines preserved. Integrity
and FK checks passed. Built cheapest/prices also ran read-only against production;
none of the 16 service URLs appeared in normal output. No production writes by audit.

## Exact deployment

Prepared executable: scripts/pokemon-monitor-deploy-opening-filter.
Shell syntax and embedded Python AST checked. The script verifies clean main,
origin, old/new commits and ancestry. It obtains sudo in the user's terminal,
stops only the monitor, takes a consistent SQLite backup, fast-forwards, runs
npm ci/build, reclassifies twice without notifier/network, checks history/schema/
integrity/baselines, then starts the service. Failure leaves explicit rollback
instructions. Already-target checkout is not blindly deployed again.

Required terminal command, as kaian:

```sh
/home/kaian/nas-admin/scripts/pokemon-monitor-deploy-opening-filter
```

Reason for user action: `sudo -n -l` returns “interactive authentication is required”.
No password is requested by or passed through Codex. The restart is necessary
because the running monitor must load the changed parsers/state/policy modules.

Receipt: runtime/deploy-opening-filter.json. Backup:
runtime/backups/pre-opening-filter-<UTC timestamp>.sqlite. Schema remains 2.
After the user confirms completion: inspect receipt, observe 2–3 poll cycles,
check active/enabled/NRestarts, healthy stores, no new parser failures or service
pushes, normal sealed products, CLI views, integrity/FK and preserved history.

## Rollback

No schema downgrade or state reset. As kaian, in the server terminal:

```sh
sudo systemctl stop pokemon-release-monitor.service
cd /home/kaian/apps/PokemonReleaseMonitor
git status --short
# Continue only if clean.
git switch --detach 18fd2bf4b87bc926d96d2591d2371a50c233bb0d
PATH=/home/kaian/.local/opt/node-v24.21.0-linux-x64/bin:$PATH npm ci
PATH=/home/kaian/.local/opt/node-v24.21.0-linux-x64/bin:$PATH npm run build
sudo systemctl start pokemon-release-monitor.service
/home/kaian/.local/bin/pokemon-monitor status
```

Retain SQLite/WAL/runtime/environment/logs/backups. Old code ignores the added
metadata; future old-code polls can restore opening-service eligibility, so this
rollback also restores the old filtering limitation. Prefer a forward correction
if continued global exclusion is required. Historical sent notifications and
existing product/store identities are never rolled back to an older DB snapshot.

## Post-deploy outcome

Pending user-run deployment. Do not describe the production monitor as hardened
until the new commit is running and post-deploy observation is completed.

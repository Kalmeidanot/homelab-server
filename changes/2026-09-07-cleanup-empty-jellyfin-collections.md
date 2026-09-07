# Remove Empty Jellyfin Collections

Date: 2026-09-07

Status: Completed

## Reason

The administrator finished moving media out of the active Jellyfin libraries
and confirmed a fresh library scan had completed. Remove only the resulting
empty collection containers, preserving media, populated collections, and playlists.
The administrator reviewed the complete 59-collection audit and explicitly
approved the 36 zero-member BoxSet IDs recorded below.

## Configuration and API

- Jellyfin server and live OpenAPI version: 10.11.11
- Deployment: compose/jellyfin/compose.yaml, host networking, jellyfin container
- Local API: http://127.0.0.1:8096
- Live definition: GET /api-docs/openapi.json
- Version: GET /System/Info/Public
- Health: GET /health
- Collection enumeration: GET /Items with includeItemTypes=BoxSet and recursive=true
- Item type recheck: GET /Items with ids=<approved ID>
- Membership: GET /Items with parentId=<approved ID>, recursive=true,
  collapseBoxSetItems=false, enableTotalRecordCount=true, and pagination
- Deletion: DELETE /Items/{itemId}, one approved empty BoxSet at a time

The API key was read privately from the administrator-supplied file outside this
repository and used in an Authorization header. No key value was displayed,
logged, documented, or committed. No configuration or database credential search
was performed.

The live OpenAPI definition and matching 10.11.11 implementation were reviewed.
The generic item deletion endpoint can delete filesystem content; it was used
only for approved, freshly confirmed empty BoxSets whose API paths were under
/config/data/collections/. Paths were an additional scope guard, not evidence
of emptiness. Jellyfin itself performed the metadata cleanup through its API;
no collection directory or database was manually edited or deleted.

Implementation references:

- [LibraryController, 10.11.11](https://github.com/jellyfin/jellyfin/blob/v10.11.11/Jellyfin.Api/Controllers/LibraryController.cs)
- [BoxSet, 10.11.11](https://github.com/jellyfin/jellyfin/blob/v10.11.11/MediaBrowser.Controller/Entities/Movies/BoxSet.cs)
- [LibraryManager, 10.11.11](https://github.com/jellyfin/jellyfin/blob/v10.11.11/Emby.Server.Implementations/Library/LibraryManager.cs)

## Changes and Safeguards

- A read-only audit found 59 BoxSets: 36 empty and 23 populated.
- Non-recursive parent queries returned zero even for populated collections.
  Recursive queries returned their actual Movie members and were used for all
  emptiness decisions, with a second audit pass confirming the results.
- The deletion script accepted only the 36 explicitly approved IDs.
- Immediately before each deletion, the API reconfirmed BoxSet type and exactly
  zero recursively returned members, without a user-specific visibility filter.
- A nonempty, missing, changed-type, or unexpected-path item would be skipped;
  a request or verification error would stop further deletion.
- All 36 DELETE requests returned HTTP 204 and the IDs were checked absent.
- No playlist mutation, media modification, restart, or manual scan was requested.

The temporary execution helper was run as:

```text
python3 /tmp/jellyfin-empty-cleanup.py prepare
python3 /tmp/jellyfin-empty-cleanup.py delete
```

The helper and sanitized before/after JSON reports in /tmp are execution
artifacts, not durable repository tooling. The definitive deleted IDs are below.

## Validation and Outcome

- Collections: 59 before, 23 after; zero empty collections remain.
- All 23 previously populated collections remain, with exactly the same member IDs.
- All 36 approved IDs are absent. No approved item was skipped.
- The explicitly typed API inventory contained 1,886 items before and 1,850 after;
  the removed IDs were exactly the 36 approved BoxSets.
- All 1,747 media IDs remained: 141 Movies, 1,305 Episodes, 300 Videos, and 1 Trailer.
  The inventory also included 68 Seasons and 12 Series, all preserved.
  Audio, AudioBook, Book, MusicVideo, Photo, Recording, Playlist, MusicAlbum, and
  PhotoAlbum types were included in the query and had no returned items.
- A recursive read-only filesystem inventory of /srv/storage/media matched all
  2,749 entries before and after: paths, device/inode identities, types, sizes,
  permissions, owner/group IDs, modification times, and symlink targets where
  applicable. This was metadata comparison, not full content hashing; no media
  contents were written by the cleanup.
- GET /health reported Healthy before and after; no restart was needed.
- No deletion or final-verification errors occurred.
- Repository diff/whitespace review passed; only relevant documentation changed.

Read-only API issues encountered and resolved: the user-oriented item route
returned HTTP 400 with API-key-only authentication, so item lookup used the
supported /Items ids query. An unfiltered recursive /Items inventory returned
HTTP 500; an explicit media/container-type query succeeded with complete
pagination. Neither failed read request performed any deletion.

## Security and Affected State

Affected state is limited to the 36 empty Jellyfin collection containers and
their Jellyfin-managed metadata. Media files, subtitles, artwork and NFOs under
the media root, populated collections, and application configuration were
preserved. No direct SQLite/database access was used. The API key remains
outside Git; revocation of the temporary key is a separate administrator action.

## Recovery

The deleted empty containers had no media memberships to restore. If a container
is wanted again, recreate it through Jellyfin's UI or the supported Collections
API using its recorded name. Recreated IDs and artwork/metadata may differ.
No full collection-metadata backup was made, so exact metadata restoration is
not promised. Do not restore a whole database or manipulate collection files
manually as part of this cleanup; media recovery is unnecessary.

## Deleted Collections

Every row had zero members immediately before deletion.

| Collection | Jellyfin item ID |
|---|---|
| 101 Dalmatians (Animated) Collection | `d66772ff1a6598fc019203f01ee63346` |
| A Goofy Movie Collection | `59af051d6d27615c7ddaf7290b4b8c3b` |
| Aladdin Collection | `87ab895dae2d16a4b66c0a2d09febf2a` |
| Askepott Collection | `e34ffb41bea9d02e6bf4dc2e7e72fae8` |
| Atlantis Collection | `9feafb159ff7312fe6b05bfe8886ec3f` |
| Bambi Collection | `5e90a6cb95290ecdb788ef1cc5010187` |
| Beauty and the Beast Collection | `8fbfb80e9311f0497e436fa5aadfe34e` |
| Caballeros Collection | `1958b62249ff23857d9b137611ff1eb4` |
| Cinderella Collection | `48a7b6375acf09c8ba8380ef8a251d28` |
| Fantasia Collection | `d1ab45f950a147a6b070e702cd42cdd3` |
| Kim Possible Collection | `dfddb6018b4acdd432ceb25837d9225c` |
| Lady and the Tramp Collection | `31e25d8cd9e9198f18d1075835a19a45` |
| Lilo & Stitch (Animated) Collection | `35d6895b2b58b29d624346b5a6829e9a` |
| Mickey's… Upon a Christmas Collection | `ea518a0ea8a72e7f47eb107573f9a7ef` |
| Min Bror Bjørnen | `5da428f072efdf4b202793a814f0e542` |
| Min Bror Bjørnen | `998ef8825075626e5f055ea1cf1c6bbc` |
| Mulan Collection | `0c95a1a10adb48793dd2498c065ba8aa` |
| Peter Pan Collection | `c079f8e40eb17c0096081792c422717d` |
| Pocahontas Collection | `361fa99ed24df7dc2ddcce10ea647077` |
| Tarzan (Animation) Collection | `d52380f4f295284c7be8124502fcdb64` |
| The Emperor's New Groove Collection | `f6ff9d304562ba9164b706c52430e177` |
| The Fox and the Hound Collection | `458fe3daa96ae86aeb305ad75cb4b3a5` |
| The Hunchback of Notre Dame Collection | `d22a9bea24132a9cffa47e66089b52ef` |
| The Jungle Book Collection | `f2d0ae72cf34c7dc9ac3a3c7eee408b4` |
| The Lion King Collection | `679d015990e70e6c6fbedbfe9f084d98` |
| The Little Mermaid Collection | `700d9fb2806190ca9cc534b26759c17c` |
| The Rescuers Collection | `ce7b24bf437243897b24149c19e3f898` |
| Toy Story Collection | `d2191a91bbb69e161956a97af387811b` |
| ポケットモンスター アドバンスジェネレーション シリーズ | `10b1f93bda53969c931df8689a63d60d` |
| ポケットモンスター アドバンスジェネレーション シリーズ | `ddc07abd89811f7a40eac6bb44a54714` |
| ポケットモンスター シリーズ | `920d5a58d7dfb94e59b3452b824196d4` |
| ポケットモンスター ダイヤモンド&パール シリーズ | `0c14c7371168a9e0f4d1201813d407b7` |
| ポケットモンスター ダイヤモンド&パール シリーズ | `6932489d4e28f8bbdbad9259ce59d555` |
| ポケットモンスター ベストウイッシュ シリーズ | `e41985cf860e977cd1a813418602c862` |
| ポケットモンスター ベストウイッシュ シリーズ | `f0a13012216b57608bf696626d84ce23` |
| ポケモン不思議のダンジョン シリーズ | `51fcce68b7de1ca6237d07f943022e17` |

## Preserved Populated Collections

| Collection | Jellyfin item ID | Members before and after |
|---|---|---:|
| Ace Ventura Collection | `e0b04e86496d5116c7c870ca9fdd4918` | 2 |
| Avatar Collection | `e0ef9c2ef48794cf90330e5a8e671998` | 2 |
| Captain America Collection | `228810e48238da768b49ffa79c83c522` | 2 |
| Child's Play Collection | `a7822bb859d56c7aa9b1ead56ba15b87` | 5 |
| Doctor Strange Collection | `027fd827f4df77c3d29c0492bc7315af` | 2 |
| Guardians of the Galaxy Collection | `3c8dfb827a9dbd9adc37d9a569104cac` | 2 |
| Harry Potter Collection | `4ca22b93013a86aca66741235b7cbd37` | 8 |
| Herbie Collection | `63bb61e5b89a93ece2ec4f7db1eaf5d2` | 2 |
| Iron Man Collection | `43d4dc455f7aba5ae10021d6ce8d1c72` | 3 |
| James Bond Collection | `60b37f81616dc8f26fd807d91ee23d42` | 25 |
| Jaws Collection | `4610c63133b8ba52eaded62bdb3c5255` | 4 |
| Jurassic Park Collection | `7b6daebf10a51ef4e817434eaba16b46` | 7 |
| Rocky Collection | `ec27102247d801d6d9835e9f0f7b4df3` | 6 |
| Rush Hour Collection | `96208e6aa6cb1ef82142d81ff1fcd2f3` | 3 |
| Scary Movie Collection | `66f163abfd9b0f6eb8d1a4d8ea05b443` | 6 |
| Scream Collection | `9f15866ba532c565855d6b34d42f242d` | 3 |
| Spider-Man (MCU) Collection | `289b7f1f8ed5461f03837af0110ecf06` | 3 |
| The Avengers Collection | `34ab6fd1f51c41bb014981f2e334f465` | 4 |
| The Dark Knight Collection | `a94f86b422e7452e94f2402c75dcc563` | 3 |
| The Lord of the Rings Collection | `ef9334d74f41ff40e9cd98f45ceaa7f6` | 3 |
| The Matrix Collection | `7ba7b56b7bc2671aabd7d8f137797a71` | 4 |
| The Terminator Collection | `bca1f27ba958eca61067d09eb130abf4` | 6 |
| Undisputed Collection | `592298160fab3640d35e4e64048fea16` | 3 |

# Naruto playlists without pure filler

Date: 2026-09-18

Status: Both playlists created through the Jellyfin API and verified.

## Goal and policy

Provide the complete ordinary Naruto and Naruto: Shippuden episode sequences
with only pure filler excluded. Classification sources, checked on this date:
[Naruto](https://www.animefillerlist.com/shows/naruto) and
[Naruto Shippuden](https://www.animefillerlist.com/shows/naruto-shippuden) on
Anime Filler List. Manga Canon, Mixed Canon/Filler and Anime Canon are retained;
only Filler is excluded. Movies, OVAs, specials and Season 0 are excluded.

| Playlist | Ordinary total | Filler excluded | Included | PlaylistId |
| --- | ---: | ---: | ---: | --- |
| Naruto – Uten fillers | 220 | 90 | 130 | `f4cd555473f3e678c7b5cf95eb455f3b` |
| Naruto: Shippuden – Uten fillers | 500 | 203 | 297 | `7f29faf1cf2e5316a0f5166fc1d7c597` |

Both playlists are private to Kaian, UserId
`5c02e89163964acbb9d7e22ee8f4f699`. User-specific API queries confirmed both
visible to Kaian and neither visible to the other four accounts.

The exact excluded sets matched both the user's specification and the source:

- Naruto: 26, 97, 101–106, 136–140, 143–219.
- Shippuden: 57–71, 91–112, 144–151, 170–171, 176–196, 223–242,
  257–260, 271, 279–281, 284–295, 303–320, 347–361, 376–377, 388–390,
  394–413, 416–417, 422–423, 427–450, 464–468, 480–483.

## Inspection and episode mapping

Local health and public server information reported Healthy and Jellyfin
10.11.11. The live `GET /api-docs/openapi.json` also reported 10.11.11;
its playlist contract and the matching upstream implementation were reviewed.
Docker inspection required interactive sudo, so the user supplied fresh inspect
output: `/jellyfin`, `jellyfin/jellyfin:latest`, running/healthy, and
`/srv/storage/media -> /media` with `Mode=ro`, `RW=false`. Compose matched.

- Naruto (2002–2007): SeriesId `ec9290555dfd64c5b2b989edc7292da4`,
  TVDB 78857, TMDB 46260, IMDb tt0409591;
  `/media/tv-series/Naruto (2002)`, four seasons.
- Naruto Shippūden (2007–2017): SeriesId `52b4b562a4b21d388858d411156a570b`,
  TVDB 79824, TMDB 31910, IMDb tt0988824;
  `/media/tv-series/Naruto Shippuden (2007)`, twenty seasons.

All Series items were enumerated; there was one candidate for each series.
Paginated Episode queries returned exactly 220 and 500 ordinary episodes.
Every ItemId, file path and episode TVDB ID was unique within its series.
Each episode had one existing regular media file and one media source.

The filenames use `SxxEyy` with **continuing absolute episode numbers across
seasons**, rather than resetting E to 1. Parsed filename season/episode values
matched API ParentIndexNumber/IndexNumber for all 720 episodes. Sorting by
season/episode produced exactly 1–220 and 1–500, without gaps, duplicates,
combined episodes, extras or Season 0. Naruto season ranges were 1–52, 53–104,
105–158 and 159–220; Shippuden continued from S01E01 through S20E500.
Premiere dates were nondecreasing throughout both sequences.

All 720 numbered source rows were cross-checked: each episode matched its source
number by normalized title or exact premiere date, in addition to the filename
and complete sequence evidence. There were 7/67 title wording differences and
8/2 date differences for Naruto/Shippuden, respectively; no episode differed in
both checks. These source/provider differences did not make mapping ambiguous,
and no metadata was corrected.

## API changes and verification

Read-only checks used `GET /Users`, paginated `GET /Items` for series, seasons,
episodes and playlists, plus health/version/OpenAPI reads. Playlist queries
across all five users found no existing playlists. In-memory manifests included
absolute number, ItemId, season, episode, title, path, classification and action.
All write-gate checks passed before the first write, including fresh episode
identity/visibility checks and exact filler-set equality.

Exactly two `POST /Playlists` requests created the playlists, each with its full
ordered Ids array, the above UserId, MediaType Video, no additional Users and
IsPublic false. Authentication used the supplied temporary environment variable
in an HTTP header; no secret was printed or saved to a file.

`GET /Items` and paginated `GET /Playlists/{playlistId}/Items` verified names,
counts, exact ordered ItemId membership, Episode type, correct SeriesId, paths,
absence of specials and duplicates, and an empty filler intersection for both.
First/last absolute episodes are 1/220 and 1/500. Naruto 220 was retained.
Retained classifications: Naruto 74 Manga Canon + 56 Mixed Canon/Filler;
Shippuden 232 Manga Canon + 64 Mixed Canon/Filler + 1 Anime Canon (episode 28).
Both playlists passed a second complete readback. Episode API metadata remained
unchanged, and final health was Healthy.

## Affected state and media safety

Only the two new playlist objects and their Jellyfin-managed metadata under
`/srv/jellyfin/config/data/playlists/` changed. No direct database access,
episode-metadata edits, scans, configuration changes or restarts were performed.
No media files were copied, moved, renamed, deleted or modified; no hardlinks,
symlinks or media directories were created. All 3,844 filesystem entries under
`/srv/storage/media` matched before/after by path, device/inode, type/mode,
owner/group, size, modification/change timestamps, link count and symlink target.
This was filesystem metadata comparison, not full content hashing.

This record is the only repository change. CURRENT_STATE.md remains a server
state reference, not a playlist catalog. runbooks/everyday-commands.txt was
reviewed; no operational command, address, service or troubleshooting step changed.

## Rollback

If later requested, sign in as Kaian and delete only the two newly created
playlists through Jellyfin's playlist UI, confirming their names and PlaylistIds
above. Delete the playlist objects, not their referenced episodes. Leave all
other playlists and media intact. No rollback was performed.

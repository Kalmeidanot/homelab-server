# Move Approved Disney/Family Movies out of the Active Movies Directory

Date: 2026-09-07

Status: Completed

## Reason

Retain Disney/Pixar animated family movies while moving them out of the active
Jellyfin Movies library directory. The administrator approved the complete
105-folder proposed list and explicitly added all 12 borderline candidates.
This selection does not include all Disney-owned or distributed films.

## Configuration and Scope

- Source: /srv/storage/media/movies
- Destination: /srv/storage/media/disney (already existed and was empty)
- Storage: WD My Book, /dev/sda1, ext4 mounted read/write at /srv/storage
- Both directories are on the same filesystem.
- Jellyfin Movies library remains /media/movies.
- The destination remains inside the existing Media Samba share and the
  container's read-only /media mount, but outside /media/movies.

## Changes

Moved 117 approved folders, containing 118 regular files (90,436,003,237 bytes),
with their existing names and contents preserved. No media was copied, rewritten,
deleted, or overwritten. No ownership or permission changes were made.

The prepared temporary script was run as:

```text
python3 /tmp/move-approved-disney.py inspect
python3 /tmp/move-approved-disney.py move
```

The script used an explicit approved-name list and Linux renameat2 with
RENAME_NOREPLACE for each complete directory. This performs an atomic move on
the same filesystem and refuses any existing destination, with no copy fallback.
The temporary script and JSON manifests are execution artifacts, not durable
repository tooling; the complete moved-folder list is recorded below.

Jellyfin configuration was not changed, no service was reloaded or restarted,
and no Jellyfin scan was manually triggered. The administrator handles Jellyfin
separately. Immich-managed storage and the general-purpose archive were untouched.

## Validation

- Repository was clean before work began.
- Host-level findmnt confirmed /srv/storage on /dev/sda1, ext4, read/write.
  The sandbox-only mount view was read-only; the approved move ran outside it.
- All 117 approved sources existed and no destination conflicts were present.
- A recursive manifest captured all 235 entries (117 roots and 118 files).
- Each source was compared with its manifest immediately before its move.
- Each moved source path was confirmed absent and its destination present.
- Recursive destination manifests matched original relative names, device/inode
  identities, file types, modes, owner/group IDs, sizes, modification times,
  link counts, and symlink targets where applicable, both immediately and in
  a final pass. The same inodes were relocated; no media-content rewrite occurred.
- This was inode/metadata verification of same-filesystem moves, not a full
  content-hash or playback validation. Rename-related change times were not compared.
- All 156 unselected source entries retained their original paths and checked
  metadata, including Victory Through Air Power (1943).
- Final source/destination name sets matched the expected result exactly.
- Samba open-file lock inspection could not be completed: smbstatus requires
  root, and sudo required interactive authentication. No claim is made that
  active Samba transfers were ruled out.

## Outcome

- Moved and verified: 117 folders, 118 files.
- Approved items skipped: none.
- Conflicts or move/verification errors: none.
- The 12 initially uncertain/borderline candidates were moved by explicit user
  approval; their inclusion does not establish an otherwise uncertain identity
  (in particular, the Aladdin (1994) folder was not renamed or reclassified).
- All other titles remained in place, including Victory Through Air Power (1943),
  Marvel titles, Pokemon titles, and the other excluded movies.
- Jellyfin's displayed library state was not verified or refreshed.

## Security

No secrets were added to the repository. Existing file permissions and ownership
were preserved, and no Samba access configuration was changed. The moved movies
remain accessible through the existing Media share under its disney directory.

## Recovery

If the administrator later wants to restore the previous directory layout, move
only the folders listed below from /srv/storage/media/disney back to
/srv/storage/media/movies using the same no-overwrite, same-filesystem approach.
First confirm the storage mount, source identities, and absence of conflicting
names. Stop for any conflict; do not merge directories or delete either copy.
Verify source absence and destination integrity afterward. Any Jellyfin refresh
is a separate administrator action. No rollback was performed.

## Moved Folders

Exact names, including the 12 explicitly approved additions:

```text
101 Dalmatians (1961)
101 Dalmatians 2 - Patch's London Adventure (2003)
A Bug's Life (1998)
A Goofy Movie (1995)
Aladdin -The Return of Jafar (1994)
Aladdin and the King of Thieves (1996)
Alice in Wonderland (1951)
An Extremely Goofy Movie (2000)
Atlantis 2 Milo's Return (2003)
Atlantis The Lost Empire (2001)
Bambi (1942)
Bambi II (2006)
Beauty and the Beast (1991)
Beauty and the Beast - The Enchanted Christmas (1997)
Belle's Magical World (1998)
Bolt (2008)
Brother Bear (2003)
Brother Bear 2 (2006)
Buzz Lightyear Of Star Command, The Adventure Begins (2000)
Cars (2006)
Chicken Little (2005)
Cinderella (1950)
Cinderella II - Dreams Come True (2002)
Cinderella III - A Twist in Time (2007)
Dinosaur (2000)
Disney Princess Enchanted Tales - Follow Your Dreams (2007)
Ducktales The Movie - Treasure of the Lost Lamp (1990)
Dumbo (1941)
Fantasia (1940)
Fantasia 2000 (2000)
Finding Nemo (2003)
Fun and Fancy Free (1947)
Hercules (1997)
Home On The Range (2004)
Kim Possible - A Stitch In Time (2003)
Kim Possible - So The Drama (2005)
Kim Possible - The Secret Files - Attack Of The Killer Bebes, Downhill, & Partners (2002)
Kim Possible - The Villain Files (2004)
Kronk's New Groove (2005)
Lady and the Tramp (1955)
Lady And The Tramp II - Scamp's Adventure (2001)
Leroy & Stitch (2006)
Lilo And Stitch (2002)
Lilo and Stitch 2 - Stitch has a Glitch (2005)
Make Mine Music (1946)
Meet The Robinsons (2007)
Melody Time (1948)
Mickey Donald Goofy-The Three Musketeers (2004)
Mickey's House of Mouse - The Villains (2002)
Mickey's Magical Christmas-Snowed In at the House of Mouse (2001)
Mickey's Once Upon A Christmas (1999)
Mickeys Twice Upon a Christmas (2004)
Monsters, Inc (2001)
Mulan (1998)
Mulan II (2004)
Oliver & Company (1988)
Peter Pan (1953)
Piglet's Big Movie (2003)
Pinocchio (1940)
Pocahontas (1995)
Pocahontas II - Journey to a New World (1998)
Pooh's Heffalump Movie (2005)
Ratatouille (2007)
Return to Never Land (2002)
Robin Hood (1973)
Saludos Amigos (1942)
Sleeping Beauty (1959)
Snow White and the Seven Dwarves (1937)
Stitch! The Movie (2003)
Tarzan & Jane (2002)
Tarzan (1999)
Tarzan II (2005)
The Adventures Of Ichabod and Mr. Toad (1949)
The Aristocats (1970)
The Black Cauldron (1985)
The Emperor's New Groove (2000)
The Fox and the Hound (1981)
The Fox and the Hound 2 (2006)
The Great Mouse Detective (1986)
The Hunchback of Notre Dame (1996)
The Hunchback of Notre Dame II (2002)
The Incredibles (2004)
The Jungle Book (1967)
The Jungle Book 2 (2003)
The Lion King (1994)
The Lion King 1-1.5 - Hakuna Matata (2004)
The Lion King 2 - Simba's Pride (1998)
The Little Mermaid (1989)
The Little Mermaid - Ariel's Beginning (2008)
The Little Mermaid 2-Return to the Sea (2000)
The Many Adventures of Winnie the Pooh (1977)
The Rescuers (1977)
The Rescuers Down Under (1990)
The Sword in the Stone (1963)
The Three Caballeros (1945)
The Tigger Movie (2000)
Tinker Bell (2008)
Toy Story (1995)
Toy Story 2 (1999)
Treasure Planet (2002)
Wall-E (2008)
Winnie the Pooh - Springtime With Roo (2004)
Winnie The Pooh's Most Grand Adventure (1997)
Winnie the Pooh-A Very Merry Pooh Year (2002)
Winnie The Pooh-Seasons of Giving (1999)
Aladdin (1994)
A Disney Christmas Gift (1982)
Disney's Christmas Favourites (2005)
Bedknobs and Broomsticks (1971)
Enchanted (2007)
James and the Giant Peach (1996)
Mary Poppins (1964)
Pete's Dragon (1977)
Song of the South (1946)
The Nightmare Before Christmas (1993)
The Reluctant Dragon (1941)
Who Framed Roger Rabbit (1988)
```

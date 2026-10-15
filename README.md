# Tunes Off the Chain — website

Static site for the Tunes Off the Chain brass method, served by GitHub Pages
at tunesoffthechain.au. The domain is set in the repo's Settings → Pages; `CNAME`
only records it. The site publishes only its own pages and
media (see "Deploying"), but the repo itself is public on GitHub, so keep
everything here, this README included, free of anything private.

## Editions
This is the live site, for the published edition. The next edition is built up
on its own branch, `edition-<year>` (now `edition-2027`); its README explains
publishing it. Fixes made here should be merged into that branch
(`git switch edition-2027 && git merge main`), and when `rights.json` changes in
the book's repo, copy it to both branches.

## Layout
- `manifest-2026.yaml` — source of truth: numbered tunes, unnumbered extras, song books.
- `rights.json` — copyright and licensing, **copied from the book's repo**
  (`make rights` there); never edit it here. Only the .mp3 tags use it on this branch.
- `generate.py` — builds the site from the manifest.
- `index.html`, `tunes/`, `books/`, `assets/css/style.css` — **generated**; don't hand-edit,
  change `generate.py` (or the manifest) and regenerate instead.
- `assets/fonts/decaf-please.woff2` — self-hosted title font.
- `assets/icons/`, `favicon.ico` — favicon, home-screen icon and the link-preview image
  (og-image.png). Static files, not generated; `favicon.svg` is the master.
- `media/audio/` — backing tracks (.mp3). `totc-all-tunes.zip` is built there too,
  but not committed (.gitignore).
- `media/books/` — trumpet and trombone PDFs.
- `.github/workflows/pages.yml` — builds and deploys the site (see "Deploying").

## Regenerating
Edit manifest-2026.yaml (or generate.py), then from the repo root:

    python3 generate.py

(needs pyyaml and mutagen: `pip install pyyaml mutagen --break-system-packages`,
or Debian's `python3-yaml` and `python3-mutagen`)

This rewrites the CSS, the home page, the books page, tunes/index.html and every
tunes/<id>.html page. It builds the all-tunes zip for previewing, only when the set
of .mp3 files in media/audio/ or their contents have changed; the zip isn't
committed.

It also warns about any tune marked `available` whose .mp3 is missing, and deletes
tune pages that are no longer in the manifest. It stops, before writing anything,
if a published track has no entry in `rights.json` (a track of your own with no
source in the book's repo needs `rights: own` in the manifest) or isn't allowed
to be a free download.

`python3 generate.py --tag-tracks` also tags the .mp3 files from `rights.json`
and the manifest: title, track number, artist, album, composer, copyright,
licence and the tune's page. The deploy workflow does that; don't commit the
result, so the .mp3s in git stay as they are.

## Adding or updating audio
1. Convert the original recording (.m4a) to a 192 kbps .mp3 in media/audio/. The
   filename must exactly match the `file:` path in the manifest (e.g. HandsUp.mp3):

       ffmpeg -i 01-HandsUp.m4a -map 0:a -map_metadata -1 -c:a libmp3lame -b:a 192k media/audio/HandsUp.mp3

   Convert from the original, never from another .mp3. Keep the .m4a somewhere
   outside the repo; git ignores .m4a files anyway.
2. For a tune that was `coming_soon`, set its `status` to `available` and fill in
   `file`.
3. Run generate.py and commit the .mp3 with the pages.

## Deploying
Pages is set to deploy from GitHub Actions, not from a branch. On every push,
`.github/workflows/pages.yml` checks out the branch, runs
`python3 generate.py --tag-tracks` (which tags the .mp3s and builds the zip) and
publishes the site's own files: `index.html`, `favicon.ico`, `assets/`, `books/`,
`media/` and `tunes/` (and `licence.html` and `credits.html`, once they exist). The
README, `generate.py`, the manifest and `rights.json` stay off the site. A new
top-level file the site needs must be added to that list in the workflow.

Only `main` is deployed. On any other branch the run stops there, and its
`github-pages` artifact (on the run's page) is the site that branch would
publish, for checking an edition before it goes live.

So the zip and the tags never go into git: a new track means one small commit,
not a fresh 80 MB zip.

## Updating the song books
Put the new PDFs in media/books/ and update the `books:` entries in the manifest.

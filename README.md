# Tunes Off the Chain — website

Static site for the Tunes Off the Chain brass method, served by GitHub Pages
at tunesoffthechain.au (see CNAME). The whole repo is published as-is (see
"Deploying"), so this README is publicly reachable at /README.md — keep it free
of anything private.

## Layout
- `manifest-2026.yaml` — source of truth: numbered tunes, unnumbered extras, song books.
- `generate.py` — builds the site from the manifest.
- `index.html`, `tunes/`, `books/`, `assets/css/style.css` — **generated**; don't hand-edit,
  change `generate.py` (or the manifest) and regenerate instead.
- `assets/fonts/decaf-please.woff2` — self-hosted title font.
- `assets/icons/`, `favicon.ico` — favicon, home-screen icon and the link-preview image
  (og-image.png). Static files, not generated; `favicon.svg` is the master.
- `media/audio/` — backing tracks (.mp3). `totc-all-tunes.zip` is built there too,
  but not committed (.gitignore).
- `.github/workflows/pages.yml` — builds and deploys the site (see "Deploying").
- `media/books/` — trumpet and trombone PDFs.

## Regenerating
Edit manifest-2026.yaml (or generate.py), then from the repo root:

    python3 generate.py

(needs pyyaml: `pip install pyyaml --break-system-packages`)

This rewrites the CSS, the home page, the books page, tunes/index.html and every
tunes/<id>.html page. It builds the all-tunes zip for previewing, only when the set
of .mp3 files in media/audio/ or their contents have changed; the zip isn't
committed.

It also warns about any tune marked `available` whose .mp3 is missing, and deletes
tune pages that are no longer in the manifest.

## Adding or updating audio
1. Copy the .mp3 into media/audio/ — the filename must exactly match the `file:`
   path in the manifest (e.g. HandsUp.mp3).
2. For a tune that was `coming_soon`, set its `status` to `available` and fill in
   `file`.
3. Run generate.py and commit the .mp3 with the pages.

## Deploying
Pages is set to deploy from GitHub Actions, not from a branch. On every push,
`.github/workflows/pages.yml` checks out the branch, runs `python3 generate.py`
(which builds the zip) and packages the repo as it then stands (minus `.git` and
`.github`) as the site. Only `main` is deployed. On any other branch the run stops
there, and its `github-pages` artifact (on the run's page) is the site that branch
would publish.

So the zip never goes into git: a new track means one small commit, not a fresh
80 MB zip.

## Updating the song books
Put the new PDFs in media/books/ and update the `books:` entries in the manifest.

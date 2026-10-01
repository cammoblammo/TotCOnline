# Tunes Off the Chain — website

Static site for the Tunes Off the Chain brass method, served by GitHub Pages
at tunesoffthechain.au (see CNAME). `.nojekyll` makes Pages serve files as-is,
so this README is publicly reachable at /README.md — keep it free of anything
private.

## Layout
- `manifest-2026.yaml` — source of truth: numbered tunes, unnumbered extras, song books.
- `generate.py` — builds the site from the manifest.
- `index.html`, `tunes/`, `books/`, `assets/css/style.css` — **generated**; don't hand-edit,
  change `generate.py` (or the manifest) and regenerate instead.
- `assets/fonts/decaf-please.woff2` — self-hosted title font.
- `assets/icons/`, `favicon.ico` — favicon, home-screen icon and the link-preview image
  (og-image.png). Static files, not generated; `favicon.svg` is the master.
- `media/audio/` — backing tracks (.mp3) plus `totc-all-tunes.zip`.
- `media/books/` — trumpet and trombone PDFs.

## Regenerating
Edit manifest-2026.yaml (or generate.py), then from the repo root:

    python3 generate.py

(needs pyyaml: `pip install pyyaml --break-system-packages`)

This rewrites the CSS, the home page, the books page, tunes/index.html and every
tunes/<id>.html page. The all-tunes zip is only rebuilt when the set of .mp3 files
in media/audio/ or their contents have changed, so routine regeneration won't add
a new copy of it to git history.

It also warns about any tune marked `available` whose .mp3 is missing, and deletes
tune pages that are no longer in the manifest.

## Adding or updating audio
1. Copy the .mp3 into media/audio/ — the filename must exactly match the `file:`
   path in the manifest (e.g. HandsUp.mp3).
2. For a tune that was `coming_soon`, set its `status` to `available` and fill in
   `file`. Still outstanding: WhereverYouMayBe (10) and HotCrossBuns (30).
3. Run generate.py — the zip will be rebuilt automatically.

## Updating the song books
Put the new PDFs in media/books/ and update the `books:` entries in the manifest.

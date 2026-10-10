# Tunes Off the Chain — website

Static site for the Tunes Off the Chain brass method, served by GitHub Pages
at tunesoffthechain.au (see CNAME). `.nojekyll` makes Pages serve files as-is,
so this README is publicly reachable at /README.md — keep it free of anything
private.

## Layout
- `manifest-2026.yaml` — source of truth: numbered tunes, unnumbered extras, song books.
- `rights.json` — copyright and licensing, **copied from the book's repo** (see
  "Rights and licensing" below); never edit it here.
- `generate.py` — builds the site from the manifest and `rights.json`.
- `index.html`, `tunes/`, `books/`, `licence.html`, `credits.html`, `assets/css/style.css`,
  `media/audio/LICENSE.txt` — **generated**; don't hand-edit, change `generate.py` (or the
  manifest) and regenerate instead.
- `assets/fonts/decaf-please.woff2` — self-hosted title font.
- `assets/icons/`, `favicon.ico` — favicon, home-screen icon and the link-preview image
  (og-image.png). Static files, not generated; `favicon.svg` is the master.
- `media/audio/` — backing tracks (.mp3) plus `totc-all-tunes.zip`.
- `media/books/` — trumpet and trombone PDFs.

## Regenerating
Edit manifest-2026.yaml (or generate.py), then from the repo root:

    python3 generate.py

(needs pyyaml and mutagen: `pip install pyyaml mutagen --break-system-packages`,
or Debian's `python3-yaml` and `python3-mutagen`)

This rewrites the CSS, the home page, the books page, tunes/index.html and every
tunes/<id>.html page. The all-tunes zip is only rebuilt when the set of .mp3 files
in media/audio/ or their contents have changed, so routine regeneration won't add
a new copy of it to git history.

It also warns about any tune marked `available` whose .mp3 is missing, and deletes
tune pages that are no longer in the manifest. It retags the .mp3 files from
`rights.json` (only those whose tags differ) and stops, before writing anything, if
a published track has no rights or isn't allowed to be a free download.

## Adding or updating audio
1. Copy the .mp3 into media/audio/ — the filename must exactly match the `file:`
   path in the manifest (e.g. HandsUp.mp3).
2. For a tune that was `coming_soon`, set its `status` to `available` and fill in
   `file`. Still outstanding: WhereverYouMayBe (10) and HotCrossBuns (30).
3. Run generate.py — the zip will be rebuilt automatically.

## Rights and licensing

The book and the backing tracks are licensed CC BY-NC 4.0, except the
third-party tunes. Every copyright and licence text is written once, in the
book's repo (`TunesOffTheChain2026`, `config/rights.yaml`; its authoring guide's
"Copyright and licensing" section explains it), and reaches this site as
`rights.json`:

1. In the book's repo: `make rights` (writes `build/rights/rights.json`).
2. Copy that file here as `rights.json`.
3. `python3 generate.py`, then commit.

Do it whenever `rights.yaml` changes there (a permission, the wording, a new
tune's rights). From `rights.json`, generate.py makes:

- `licence.html` ("Using these tunes") and `credits.html` (the third-party tunes
  among this site's tunes, in the book's wording), linked from every page's footer
  and the home page;
- the download notice under the download buttons. A third-party-restricted tune's
  page gets the variant saying the tune itself isn't covered, and shows the tune's
  copyright line under its title;
- `media/audio/LICENSE.txt`, also put in the all-tunes zip;
- every published .mp3's tags:

  | Frame | Content |
  |---|---|
  | `TIT2` title, `TRCK` track | this manifest's `title` and `number` (the site's numbering; extras have no track number) |
  | `TPE1` artist, `TALB` album | the author, "Tunes Off the Chain" |
  | `TCOM` composer | the tune's: the author, "Traditional", the composer or the holder |
  | `TCOP` copyright | `track_copyright`, "2026 Cameron Horsburgh" (ID3 wants a year first) |
  | `COMM` comment | the tune's full copyright text (`track_comment`) |
  | `WCOP`, `WOAS` | the licence's URL, the tune's page here |

  Every other frame is removed, except `TXXX:iTunSMPB` (gapless playback). A file
  is rewritten only when its tags differ, so the first run after a wording change
  rewrites every .mp3 (and the zip): about 230 MB of changed files for git. The
  audio itself never changes.

**Tunes are matched by `id`**, the tune's stem in the book's repo and the .mp3's
name. A track whose tune has no source in the book's repo (FunkyRooster) needs
`rights: own` in its manifest entry; generate.py stops on a track that has neither.

**Restricted tunes.** A tune whose holder allowed it in the book but not as a free
download (`download_allowed: false` in `rights.json`) can't be published:
generate.py stops and names it. Mark it `coming_soon` until the permission is
widened in the book's `rights.yaml`.

## Updating the song books
Put the new PDFs in media/books/ and update the `books:` entries in the manifest.

# Tunes Off the Chain — site skeleton

Generated from manifest-2026.yaml. NOT served by GitHub Pages (that's what .nojekyll and the README-exclusion convention is for) — just housekeeping notes for you.

## Before pushing
1. Copy your converted .mp3 files into media/audio/ (filenames must exactly match the `file:` paths in the manifest, e.g. HandsUp.mp3).
2. Copy the book PDFs and the all-tunes zip into media/books/, and update the placeholder links in books/index.html to the real filenames.
3. Decide the two @font-face declarations aren't wired in yet — assets/css/style.css currently references 'Decaf Please' and falls back to 'Baloo 2' (Google Fonts) if the real font file isn't present. Add the real @font-face rule once you have a web licence + .woff2 file.
4. When WhereverYouMayBe (10) and HotCrossBuns (30) get real audio: update their `status` to `available` and `file` path in manifest-2026.yaml, then re-run generate.py.

## Regenerating
Edit manifest-2026.yaml, then:
    python3 generate.py
(needs pyyaml: pip install pyyaml --break-system-packages)

This regenerates tunes/index.html and every tunes/<id>.html page. It does NOT touch media/ or books/ — those are untouched by regeneration since they're not generated content.

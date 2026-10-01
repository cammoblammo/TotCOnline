import yaml, os, html

# Run this from the repo root — it reads manifest-2026.yaml and writes
# generated files into the current directory.
MANIFEST = "manifest-2026.yaml"
OUT = "."

with open(MANIFEST) as f:
    data = yaml.safe_load(f)

tunes = data["tunes"]
extras = data.get("extras", [])

os.makedirs(OUT, exist_ok=True)
os.makedirs(f"{OUT}/tunes", exist_ok=True)
os.makedirs(f"{OUT}/books", exist_ok=True)
os.makedirs(f"{OUT}/assets/css", exist_ok=True)
os.makedirs(f"{OUT}/assets/fonts", exist_ok=True)
os.makedirs(f"{OUT}/media/audio", exist_ok=True)
os.makedirs(f"{OUT}/media/books", exist_ok=True)

# .nojekyll
open(f"{OUT}/.nojekyll", "w").close()

# ---------- shared stylesheet ----------
css = """@font-face {
  font-family: 'Decaf Please';
  src: url('../fonts/decaf-please.woff2') format('woff2');
  font-weight: normal;
  font-display: swap;
}

:root {
  --color-bg: #FFFDF7;
  --color-text: #2B2A28;
  --color-muted: #6B6862;
  --color-border: #EFE9DD;
  --color-accent: #DD8047;
  --color-accent-text: #A85A2E;
  --font-title: 'Decaf Please', 'Baloo 2', sans-serif;
  --font-body: 'Atkinson Hyperlegible', sans-serif;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-body);
}
a { color: inherit; text-decoration: none; }
.container { max-width: 720px; margin: 0 auto; padding: 24px 20px 40px; }
.site-title {
  font-family: var(--font-title);
  font-weight: normal;
  font-size: 34px;
  margin: 0 0 4px;
}
.subtitle { font-size: 14px; color: var(--color-muted); margin: 0 0 16px; }

.button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px;
  background: var(--color-accent);
  border-radius: 16px;
  min-height: 44px;
  font-family: var(--font-title);
  font-weight: normal;
  letter-spacing: 0.02em;
  font-size: 19px;
  color: var(--color-text);
  border: none;
  cursor: pointer;
  width: 100%;
}
.button svg { flex-shrink: 0; }

.jumpstrip {
  display: flex;
  gap: 8px;
  padding: 4px 0 14px;
  overflow-x: auto;
}
.jumpstrip a {
  flex-shrink: 0;
  padding: 8px 14px;
  border-radius: 999px;
  background: var(--color-border);
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
}

.tunes-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
@media (min-width: 640px) {
  .tunes-list { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
}
@media (min-width: 980px) {
  .tunes-list { grid-template-columns: repeat(3, 1fr); }
}

.tune-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: #ffffff;
  border: 2px solid var(--color-border);
  border-radius: 12px;
  min-height: 44px;
}
.tune-row .num {
  width: 30px;
  flex-shrink: 0;
  font-family: var(--font-title);
  font-weight: normal;
  font-size: 16px;
  color: var(--color-accent-text);
  text-align: center;
}
.tune-row .name {
  flex: 1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.tune-row.coming-soon {
  opacity: 0.6;
  font-style: italic;
}
.tune-row.coming-soon .name { color: var(--color-muted); }

.extras-heading {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-muted);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 28px 0 8px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 4px;
  min-height: 44px;
  color: var(--color-accent-text);
  font-weight: 700;
  font-size: 16px;
}

.tune-header {
  text-align: center;
  margin: 24px 0 8px;
}
.tune-number {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-accent-text);
  letter-spacing: 0.02em;
}
.tune-title {
  font-family: var(--font-title);
  font-weight: normal;
  font-size: 40px;
  margin: 2px 0 0;
}

audio { width: 100%; margin: 20px 0; }

.hub-links {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}
.hub-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  background: #ffffff;
  border: 2px solid var(--color-border);
  border-radius: 16px;
  min-height: 44px;
}
.hub-card .hub-card-title { font-weight: 700; font-size: 16px; }
.hub-card .hub-card-desc { font-size: 13px; color: var(--color-muted); }
"""
open(f"{OUT}/assets/css/style.css", "w").write(css)

DOWNLOAD_ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M5 21h14"/></svg>'
BACK_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>'

def page(title, body, css_rel="assets/css/style.css"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_rel}">
</head>
<body>
{body}
</body>
</html>
"""

# ---------- tunes/index.html ----------
groups = []
for start in range(1, len(tunes) + 1, 10):
    chunk = tunes[start-1:start+9]
    groups.append((f"{start}", chunk))

jumpstrip = "".join(
    f'<a href="#g{g[0]}">{g[1][0]["number"]}\u2013{g[1][-1]["number"]}</a>'
    for g in groups
)

rows = ""
for label, chunk in groups:
    for t in chunk:
        num = t["number"]
        title = html.escape(t["title"])
        anchor = f' id="g{chunk[0]["number"]}"' if t is chunk[0] else ""
        if t["status"] == "coming_soon":
            rows += f'<div class="tune-row coming-soon"{anchor}><div class="num">{num}</div><div class="name">{title} \u2014 coming soon</div></div>\n'
        else:
            rows += f'<a class="tune-row"{anchor} href="{t["id"]}.html"><div class="num">{num}</div><div class="name">{title}</div></a>\n'

extra_rows = ""
if extras:
    extra_rows += '<div class="extras-heading">Also available (not numbered)</div>\n<div class="tunes-list">\n'
    for t in extras:
        extra_rows += f'<a class="tune-row" href="{t["id"]}.html"><div class="name">{html.escape(t["title"])}</div></a>\n'
    extra_rows += "</div>\n"

import glob, zipfile, zlib

# Build the "download everything" zip from whatever .mp3 files are currently
# in media/audio/. It's only rebuilt when the set of mp3s or their contents
# differ from what's already in the zip, so regenerating the site doesn't
# create a new 75 MB blob in git every time.
ZIP_REL_PATH = "media/audio/totc-all-tunes.zip"
audio_dir = f"{OUT}/media/audio"
mp3_files = sorted(glob.glob(f"{audio_dir}/*.mp3"))

def file_crc(path):
    crc = 0
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            crc = zlib.crc32(chunk, crc)
    return crc

def zip_is_current(zip_path, mp3_files):
    # Compare by filename and CRC32 rather than mtime — git checkouts reset
    # mtimes, so timestamps can't be trusted here.
    if not os.path.exists(zip_path):
        return False
    try:
        with zipfile.ZipFile(zip_path) as zf:
            existing = {i.filename: i.CRC for i in zf.infolist()}
    except zipfile.BadZipFile:
        return False
    wanted = {os.path.basename(p): file_crc(p) for p in mp3_files}
    return existing == wanted

all_zip_button = ""
if mp3_files:
    zip_path = f"{OUT}/{ZIP_REL_PATH}"
    if zip_is_current(zip_path, mp3_files):
        print("Audio unchanged — keeping existing zip.")
    else:
        print("Audio changed — rebuilding zip.")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for fpath in mp3_files:
                zf.write(fpath, arcname=os.path.basename(fpath))
    all_zip_button = f'<a class="button" href="../{ZIP_REL_PATH}">{DOWNLOAD_ICON} Download All Backing Tracks (zip)</a>'
else:
    print("No .mp3 files found in media/audio/ yet — skipping zip build.")

tunes_index_body = f"""<div class="container">
  <a class="back-link" href="../index.html">{BACK_ICON} Home</a>
  <div class="site-title">Tunes Off the Chain</div>
  <div class="subtitle">{len(tunes)} tunes — tap a number range to jump</div>
  <div class="jumpstrip">{jumpstrip}</div>
  <div class="tunes-list">
    {rows}
  </div>
  {extra_rows}
  <div style="margin-top: 28px; display: flex; flex-direction: column; gap: 12px">
    {all_zip_button}
    <a class="button" href="../books/index.html">{DOWNLOAD_ICON} Get the Song Books</a>
  </div>
</div>
"""
open(f"{OUT}/tunes/index.html", "w").write(page("Tunes Off the Chain — Tunes", tunes_index_body, css_rel="../assets/css/style.css"))

# ---------- individual tune pages ----------
def tune_page(t, is_extra=False):
    num_html = f'<div class="tune-number">TUNE {t["number"]}</div>' if not is_extra else ""
    body = f"""<div class="container">
  <a class="back-link" href="index.html">{BACK_ICON} All tunes</a>
  <div class="tune-header">
    {num_html}
    <div class="tune-title">{html.escape(t["title"])}</div>
  </div>
  <audio controls preload="none" src="../{t['file']}"></audio>
  <a class="button" href="../{t['file']}" download>{DOWNLOAD_ICON} Download this tune</a>
</div>
"""
    return page(f"Tunes Off the Chain — {t['title']}", body, css_rel="../assets/css/style.css")

for t in tunes:
    if t["status"] == "available":
        open(f"{OUT}/tunes/{t['id']}.html", "w").write(tune_page(t))

for t in extras:
    open(f"{OUT}/tunes/{t['id']}.html", "w").write(tune_page(t, is_extra=True))

# ---------- books/index.html ----------
BOOK_ICON = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--color-accent-text)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>'
ZIP_ICON = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--color-accent-text)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7" width="18" height="14" rx="2"/><path d="M3 7l3-4h12l3 4"/><path d="M12 12v4"/></svg>'

books_list = data.get("books", [])
book_cards = ""
for b in books_list:
    icon = ZIP_ICON if b["file"].endswith(".zip") else BOOK_ICON
    desc = b.get("description", "")
    book_cards += f'''<a class="hub-card" href="../{b["file"]}">
      <div style="flex-shrink:0">{icon}</div>
      <div>
        <div class="hub-card-title">{html.escape(b["title"])}</div>
        <div class="hub-card-desc">{html.escape(desc)}</div>
      </div>
    </a>
'''

books_body = f"""<div class="container">
  <a class="back-link" href="../index.html">{BACK_ICON} Home</a>
  <div class="site-title">Song Books</div>
  <div class="subtitle">Download the current edition</div>
  <div class="hub-links">
    {book_cards}
  </div>
</div>
"""
open(f"{OUT}/books/index.html", "w").write(page("Tunes Off the Chain — Song Books", books_body, css_rel="../assets/css/style.css"))

# ---------- root index.html (Hub) ----------
hub_body = """<div class="container">
  <div class="site-title">Tunes Off the Chain</div>
  <div class="subtitle">A progressive brass method project</div>
  <div class="hub-links">
    <a class="hub-card" href="tunes/index.html">
      <div>
        <div class="hub-card-title">Tunes</div>
        <div class="hub-card-desc">Listen to and download backing tracks</div>
      </div>
    </a>
    <a class="hub-card" href="books/index.html">
      <div>
        <div class="hub-card-title">Song Books</div>
        <div class="hub-card-desc">Download the trumpet and trombone books</div>
      </div>
    </a>
  </div>
</div>
"""
open(f"{OUT}/index.html", "w").write(page("Tunes Off the Chain", hub_body))

print("Generated:", sum(len(files) for _, _, files in os.walk(OUT)), "files")

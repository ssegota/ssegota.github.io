#!/usr/bin/env python3
"""Build files/CV_Sandi_Baressi_Segota.pdf from the site's own data files.

Sources: _data/cv.yml, _data/cv_summaries.yml, _data/scholar.json,
_teaching/*.md and _talks/*.md - the same content the /cv/ page renders, so the
download never drifts from the web version.

    python3 scripts/build_cv_pdf.py

Rendering goes through headless Chrome (--print-to-pdf), which is already
present on most desktops. Pass --html to stop at the intermediate HTML if you
want to inspect or restyle it.
"""

import argparse
import datetime as dt
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PDF = os.path.join(ROOT, "files", "CV_Sandi_Baressi_Segota.pdf")

CHROME_CANDIDATES = [
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

# Palette lifted from _sass/_gundam.scss so the document matches the site.
CSS = """
@page { size: A4; margin: 16mm 15mm 15mm; }
* { box-sizing: border-box; }
body {
  font-family: "Source Sans Pro", "Helvetica Neue", Arial, sans-serif;
  font-size: 10pt; line-height: 1.42; color: #15181f; margin: 0;
}
a { color: #24408e; text-decoration: none; }
.hazard {
  height: 5px; margin-bottom: 14px;
  background: repeating-linear-gradient(-45deg, #f0b929 0 7px, #1a2f6b 7px 14px);
}
header { margin-bottom: 14px; }
h1 { font-size: 20pt; margin: 0 0 2px; letter-spacing: 0.01em; }
.subtitle { color: #24408e; font-weight: 600; font-size: 10.5pt; margin: 0 0 6px; }
.contact { font-size: 8.5pt; color: #545a66; }
.contact a { color: #545a66; }
h2 {
  font-size: 8.5pt; letter-spacing: 0.22em; text-transform: uppercase;
  color: #24408e; border-bottom: 2px solid #b0b3ac;
  padding-bottom: 3px; margin: 16px 0 8px;
}
ul { margin: 0; padding-left: 15px; }
li { margin-bottom: 4px; }
li ul { margin-top: 3px; }
.entry-role { font-weight: 700; }
.entry-meta { color: #545a66; }
.summary p { margin: 0 0 7px; text-align: justify; }
.pub { margin-bottom: 5px; }
.pub .venue { color: #545a66; font-style: italic; }
.pub .cites { color: #c0272d; font-weight: 600; }
.stats { font-size: 8.5pt; color: #545a66; margin: -3px 0 8px; }
footer {
  margin-top: 18px; padding-top: 6px; border-top: 1px solid #b0b3ac;
  font-size: 8pt; color: #545a66;
}
h2, li { break-inside: avoid; }
"""


def esc(text):
    return html.escape(str(text or ""), quote=False)


def md_links_to_html(text):
    """[label](url) -> <a>, *emphasis* -> <em>, blank lines -> paragraphs."""
    text = esc(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return "\n".join(f"<p>{p}</p>" for p in paragraphs)


def read_yaml(name):
    with open(os.path.join(ROOT, "_data", name), encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_front_matter(path):
    with open(path, encoding="utf-8") as handle:
        body = handle.read()
    match = re.match(r"^---\n(.*?)\n---", body, re.S)
    return yaml.safe_load(match.group(1)) if match else {}


def collection(folder):
    entries = [read_front_matter(p) for p in glob.glob(os.path.join(ROOT, folder, "*.md"))]
    return sorted(entries, key=lambda e: str(e.get("date", "")), reverse=True)


def org_html(entry):
    name = esc(entry.get("org", ""))
    return f'<a href="{esc(entry["url"])}">{name}</a>' if entry.get("url") else name


def build_html(config):
    cv = read_yaml("cv.yml")
    summaries = read_yaml("cv_summaries.yml")
    full = next((s for s in summaries if s["id"] == "full"), summaries[0])

    scholar_path = os.path.join(ROOT, "_data", "scholar.json")
    scholar = {}
    if os.path.exists(scholar_path):
        with open(scholar_path, encoding="utf-8") as handle:
            scholar = json.load(handle)

    author = config.get("author", {})
    parts = ["<div class='hazard'></div>", "<header>",
             f"<h1>{esc(author.get('name', 'Curriculum Vitae'))}</h1>",
             "<p class='subtitle'>dr. sc., univ. mag. ing. comp. &mdash; "
             "Assistant Professor, Faculty of Informatics, "
             "Juraj Dobrila University of Pula</p>"]

    contact = []
    if author.get("email"):
        contact.append(f'<a href="mailto:{esc(author["email"])}">{esc(author["email"])}</a>')
    if config.get("url"):
        contact.append(f'<a href="{esc(config["url"])}">{esc(config["url"])}</a>')
    for key in ("orcid", "googlescholar"):
        if author.get(key):
            label = "ORCID" if key == "orcid" else "Google Scholar"
            contact.append(f'<a href="{esc(author[key])}">{label}</a>')
    parts.append("<p class='contact'>" + " &nbsp;|&nbsp; ".join(contact) + "</p>")
    parts.append("</header>")

    parts.append("<h2>Profile</h2>")
    parts.append(f"<div class='summary'>{md_links_to_html(full['text'])}</div>")

    parts.append("<h2>Education</h2><ul>")
    for entry in cv.get("education", []):
        parts.append(f"<li><span class='entry-role'>{esc(entry['degree'])}</span>, "
                     f"{esc(entry['year'])}<br><span class='entry-meta'>{org_html(entry)}"
                     "</span></li>")
    parts.append("</ul>")

    parts.append("<h2>Experience</h2><ul>")
    for entry in cv.get("experience", []):
        note = f" &mdash; {esc(entry['note'])}" if entry.get("note") else ""
        parts.append(f"<li><span class='entry-role'>{esc(entry['role'])}</span>, "
                     f"{esc(entry['period'])}<br><span class='entry-meta'>{org_html(entry)}"
                     f"{note}</span></li>")
    parts.append("</ul>")

    parts.append("<h2>Skills</h2><ul>")
    for group in cv.get("skills", []):
        items = "".join(f"<li>{esc(i)}</li>" for i in group.get("items", []))
        parts.append(f"<li><span class='entry-role'>{esc(group['group'])}</span>"
                     f"<ul>{items}</ul></li>")
    parts.append("</ul>")

    if cv.get("awards"):
        parts.append("<h2>Awards</h2><ul>")
        for award in cv["awards"]:
            parts.append(f"<li><span class='entry-role'>{esc(award['year'])}</span> &mdash; "
                         f"{esc(award['text'])}</li>")
        parts.append("</ul>")

    if scholar.get("cited"):
        stats = scholar.get("stats", {})
        parts.append("<h2>Most cited publications</h2>")
        parts.append(f"<p class='stats'>{stats.get('citations_all', '?')} citations &middot; "
                     f"h-index {stats.get('h_index_all', '?')} &middot; "
                     f"i10-index {stats.get('i10_all', '?')} "
                     f"(Google Scholar, {esc(scholar.get('fetched', ''))})</p>")
        for paper in scholar["cited"]:
            cites = (f" <span class='cites'>{paper['citations']} citations</span>"
                     if paper.get("citations") else "")
            parts.append(f"<div class='pub'>{esc(paper['authors'])} ({esc(paper['year'])}). "
                         f"<a href=\"{esc(paper['url'])}\">{esc(paper['title'])}</a>. "
                         f"<span class='venue'>{esc(paper['venue'])}</span>{cites}</div>")

    teaching = collection("_teaching")
    if teaching:
        parts.append("<h2>Teaching</h2><ul>")
        for entry in teaching:
            parts.append(f"<li><span class='entry-role'>{esc(entry.get('title'))}</span> "
                         f"&mdash; <span class='entry-meta'>{esc(entry.get('type'))}, "
                         f"{esc(entry.get('venue'))}</span></li>")
        parts.append("</ul>")

    talks = collection("_talks")
    if talks:
        parts.append("<h2>Selected talks</h2><ul>")
        for entry in talks[:12]:
            date = entry.get("date")
            year = getattr(date, "year", str(date)[:4] if date else "")
            parts.append(f"<li><span class='entry-role'>{esc(entry.get('title'))}</span><br>"
                         f"<span class='entry-meta'>{esc(entry.get('type'))}, "
                         f"{esc(entry.get('venue'))}, {esc(entry.get('location'))}, "
                         f"{esc(year)}</span></li>")
        parts.append("</ul>")

    if cv.get("service"):
        parts.append("<h2>Service and leadership</h2><ul>")
        for item in cv["service"]:
            parts.append(f"<li>{esc(item)}</li>")
        parts.append("</ul>")

    today = dt.date.today().isoformat()
    parts.append(f"<footer>Generated from {esc(config.get('url', ''))} on {today}. "
                 "Built by scripts/build_cv_pdf.py.</footer>")

    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<title>CV - {esc(author.get('name', ''))}</title>"
            f"<style>{CSS}</style></head><body>{''.join(parts)}</body></html>")


def find_chrome():
    for candidate in CHROME_CANDIDATES:
        path = shutil.which(candidate) or (candidate if os.path.exists(candidate) else None)
        if path:
            return path
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", action="store_true",
                        help="write the intermediate HTML next to the PDF and stop")
    parser.add_argument("--out", default=OUT_PDF, help="output path")
    args = parser.parse_args()

    with open(os.path.join(ROOT, "_config.yml"), encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    document = build_html(config)

    if args.html:
        target = os.path.splitext(args.out)[0] + ".html"
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(document)
        print(f"cv: wrote {target}")
        return 0

    chrome = find_chrome()
    if not chrome:
        sys.exit("Chrome or Chromium is required to render the PDF "
                 f"(looked for: {', '.join(CHROME_CANDIDATES[:4])})")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with tempfile.TemporaryDirectory() as workdir:
        source = os.path.join(workdir, "cv.html")
        with open(source, "w", encoding="utf-8") as handle:
            handle.write(document)

        subprocess.run([
            chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
            f"--user-data-dir={os.path.join(workdir, 'profile')}",
            "--no-pdf-header-footer", "--virtual-time-budget=8000",
            f"--print-to-pdf={args.out}", f"file://{source}",
        ], check=True, capture_output=True)

    size = os.path.getsize(args.out)
    print(f"cv: wrote {args.out} ({size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

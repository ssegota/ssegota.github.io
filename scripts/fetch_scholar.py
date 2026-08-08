#!/usr/bin/env python3
"""Refresh _data/scholar.json from a Google Scholar profile.

Writes the ten most recent and the ten most cited publications, plus the
profile-level citation statistics, so the publications page can render both
lists without any client-side requests to Google.

    python3 scripts/fetch_scholar.py                # refresh in place
    python3 scripts/fetch_scholar.py --dry-run      # print, do not write

Google Scholar has no API and blocks datacentre traffic aggressively, so this
will fail from most CI runners. That is expected and handled: the script exits
non-zero without touching the existing file, and the last good snapshot stays
committed until someone runs it from a normal connection.
"""

import argparse
import datetime as dt
import html
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request

SCHOLAR_ID = "lhMwhucAAAAJ"
PROFILE = "https://scholar.google.com/citations?user={uid}&hl=en&cstart=0&pagesize=100&sortby={sortby}"
OUTPUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "_data", "scholar.json")
TOP_N = 10

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")


class ScholarBlocked(RuntimeError):
    pass


def fetch(url, attempts=3):
    """GET with a browser UA. Raises ScholarBlocked on a challenge page."""
    last = None
    for attempt in range(attempts):
        request = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        })
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                body = response.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code in (429, 403):
                raise ScholarBlocked(
                    f"Google Scholar returned HTTP {exc.code} (rate limited or blocked)")
            time.sleep(2 + attempt * 3)
            continue
        except Exception as exc:  # network hiccup - worth a retry
            last = exc
            time.sleep(2 + attempt * 3)
            continue

        if "gs_captcha" in body or "unusual traffic" in body or "not a robot" in body:
            raise ScholarBlocked("Google Scholar served a CAPTCHA challenge")
        if 'class="gsc_a_tr"' not in body:
            last = RuntimeError("no publication rows in response")
            time.sleep(2 + attempt * 3)
            continue
        return body

    raise ScholarBlocked(f"could not fetch {url}: {last}")


def text_of(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment or "")).strip()


def parse_rows(body):
    rows = []
    for chunk in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', body, re.S):
        # href precedes class in Scholar's markup, so match on the anchor as a whole.
        title = re.search(r'<a[^>]*href="([^"]*)"[^>]*class="gsc_a_at"[^>]*>(.*?)</a>',
                          chunk, re.S)
        grays = re.findall(r'class="gs_gray">(.*?)</div>', chunk, re.S)
        cites = re.search(r'class="gsc_a_ac[^"]*"[^>]*>(.*?)</a>', chunk, re.S)
        year = re.search(r'class="gsc_a_h[^"]*"[^>]*>(.*?)</span>', chunk, re.S)
        if not title:
            continue

        href = html.unescape(title.group(1))
        if href.startswith("/"):
            href = "https://scholar.google.com" + href

        count = text_of(cites.group(1)) if cites else ""
        rows.append({
            "title": text_of(title.group(2)),
            "authors": text_of(grays[0]) if grays else "",
            "venue": text_of(grays[1]) if len(grays) > 1 else "",
            "year": text_of(year.group(1)) if year else "",
            "citations": int(count) if count.isdigit() else 0,
            "url": href,
        })
    return rows


def parse_stats(body):
    numbers = re.findall(r'class="gsc_rsb_std">(\d+)</td>', body)
    keys = ["citations_all", "citations_5y", "h_index_all", "h_index_5y",
            "i10_all", "i10_5y"]
    return {key: int(value) for key, value in zip(keys, numbers)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default=SCHOLAR_ID, help="Scholar profile id")
    parser.add_argument("--top", type=int, default=TOP_N, help="entries per list")
    parser.add_argument("--dry-run", action="store_true", help="print instead of writing")
    args = parser.parse_args()

    try:
        by_date = fetch(PROFILE.format(uid=args.user, sortby="pubdate"))
        time.sleep(random.uniform(1.5, 3.5))  # do not hammer
        by_cites = fetch(PROFILE.format(uid=args.user, sortby=""))
    except ScholarBlocked as exc:
        print(f"scholar: {exc}", file=sys.stderr)
        print("scholar: leaving the existing _data/scholar.json untouched", file=sys.stderr)
        return 1

    recent = parse_rows(by_date)
    cited = parse_rows(by_cites)
    if not recent or not cited:
        print("scholar: parsed zero publications - the page layout may have changed",
              file=sys.stderr)
        return 1

    name = re.search(r'id="gsc_prf_in">(.*?)</div>', by_cites, re.S)

    payload = {
        "profile_name": text_of(name.group(1)) if name else "",
        "profile_url": f"https://scholar.google.com/citations?user={args.user}&hl=en",
        "fetched": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
        "total_publications": len(cited),
        "stats": parse_stats(by_cites),
        "recent": recent[:args.top],
        "cited": sorted(cited, key=lambda row: row["citations"], reverse=True)[:args.top],
    }

    if args.dry_run:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"scholar: wrote {OUTPUT} "
          f"({len(payload['recent'])} recent, {len(payload['cited'])} cited, "
          f"{payload['stats'].get('citations_all', '?')} citations)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

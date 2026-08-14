#!/usr/bin/env python3
"""Build _data/skilltree.json from the curated taxonomy plus real evidence.

The taxonomy in _data/skills.yml says which skills exist and what words signal
them. This script does the counting: it reads publication titles out of
_data/scholar.json and repository names, descriptions and languages from the
GitHub API, matches both against the taxonomy, and turns the number of matches
into a proficiency level.

    python3 scripts/build_skilltree.py               # refresh in place
    python3 scripts/build_skilltree.py --dry-run     # print, do not write
    python3 scripts/build_skilltree.py --offline     # skip GitHub, use cache

Scoring, so the levels on the page mean something specific:

    score = 3*papers + 2*repos + min(citations/40, 6) + boost
    level = 1 at score 1, 2 at 7, 3 at 15, 4 at 30, 5 at 55

A skill with no evidence at all is dropped from the chart rather than drawn
dim, because an empty node is a claim too. Terms that appear often in the
corpus but match nothing in the taxonomy are written to
_data/skill-suggestions.md for you to review - that file is the feedback loop
that keeps the taxonomy growing without letting a keyword extractor invent
categories on your behalf.
"""

import argparse
import collections
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request

import yaml

GITHUB_USER = "ssegota"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAXONOMY = os.path.join(ROOT, "_data", "skills.yml")
SCHOLAR = os.path.join(ROOT, "_data", "scholar.json")
OUTPUT = os.path.join(ROOT, "_data", "skilltree.json")
SUGGESTIONS = os.path.join(ROOT, "_data", "skill-suggestions.md")
REPO_CACHE = os.path.join(ROOT, "_data", ".repos-cache.json")

MAX_EVIDENCE = 8          # evidence items kept per skill in the JSON
LEVEL_STEPS = [1, 7, 15, 30, 55]

# Repositories that say nothing about skills. Add to taste.
SKIP_REPOS = {"ssegota", "ssegota.github.io", "config-files"}

STOPWORDS = set("""
a an and are as at be based by for from in into is its of on or that the their
this to using use used with within without via toward towards under over about
new novel approach approaches method methods methodology model models modelling
modeling analysis application applications applied study studies research
results result performance evaluation comparison case system systems technique
techniques problem problems data set sets simple various different multiple
implementation implementations solution solutions repository code project
projects example examples test tests tool tools library first second three two
one paper review determination determining utilization improvement estimation
""".split())


def load_taxonomy(path):
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)["constellations"]


def compile_patterns(patterns):
    """Whole-word, case-insensitive matchers. Multiword patterns are fine."""
    compiled = []
    for raw in patterns or []:
        # collapse the newlines PyYAML leaves inside folded list entries
        cleaned = re.sub(r"\s+", " ", str(raw)).strip().lower()
        if not cleaned:
            continue
        body = r"[\s\-]+".join(re.escape(part) for part in cleaned.split(" "))
        compiled.append((cleaned, re.compile(rf"(?<!\w){body}(?!\w)", re.I)))
    return compiled


def load_papers(path):
    """Prefer the full corpus; fall back to the two display lists."""
    if not os.path.exists(path):
        print(f"skilltree: {path} not found, continuing without papers", file=sys.stderr)
        return [], {}
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)

    rows = data.get("corpus") or (data.get("recent", []) + data.get("cited", []))
    unique = {}
    for row in rows:
        title = (row.get("title") or "").strip()
        if title:
            unique.setdefault(title.lower(), row)
    return list(unique.values()), data.get("stats", {})


def fetch_repos(user, offline=False):
    if offline:
        if os.path.exists(REPO_CACHE):
            with open(REPO_CACHE, encoding="utf-8") as handle:
                return json.load(handle)
        print("skilltree: --offline but no repo cache; continuing without repos",
              file=sys.stderr)
        return []

    url = f"https://api.github.com/users/{user}/repos?per_page=100&type=owner"
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "skilltree-builder"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repos = []
    page = 1
    while True:
        request = urllib.request.Request(f"{url}&page={page}", headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                batch = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as exc:
            print(f"skilltree: GitHub fetch failed ({exc}); falling back to cache",
                  file=sys.stderr)
            return fetch_repos(user, offline=True)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    keep = [{
        "name": r["name"],
        "url": r["html_url"],
        "description": r.get("description") or "",
        "language": r.get("language") or "",
        "topics": r.get("topics") or [],
        "stars": r.get("stargazers_count", 0),
        "fork": r.get("fork", False),
    } for r in repos if not r.get("fork") and r["name"] not in SKIP_REPOS]

    with open(REPO_CACHE, "w", encoding="utf-8") as handle:
        json.dump(keep, handle, ensure_ascii=False, indent=1)
    return keep


def repo_text(repo):
    """Repo names carry the meaning; split them into words first."""
    words = re.sub(r"[-_.]+", " ", repo["name"])
    return " ".join([words, repo["description"], " ".join(repo["topics"])]).lower()


def level_for(score):
    level = 0
    for index, step in enumerate(LEVEL_STEPS, start=1):
        if score >= step:
            level = index
    return level


def build(taxonomy, papers, repos):
    constellations = []
    matched_spans = []          # every pattern hit, for the suggestions pass

    for group in taxonomy:
        skills = []
        for spec in group.get("skills", []):
            patterns = compile_patterns(spec.get("match"))
            langs = {lang.lower() for lang in spec.get("langs", [])}

            hit_papers, hit_repos, terms = [], [], collections.Counter()

            for paper in papers:
                title = paper.get("title", "")
                found = [name for name, rx in patterns if rx.search(title)]
                if found:
                    terms.update(found)
                    matched_spans.extend(found)
                    hit_papers.append(paper)

            for repo in repos:
                text = repo_text(repo)
                found = [name for name, rx in patterns if rx.search(text)]
                if repo["language"].lower() in langs:
                    found.append(repo["language"].lower())
                if found:
                    terms.update(found)
                    matched_spans.extend(found)
                    hit_repos.append(repo)

            citations = sum(int(p.get("citations") or 0) for p in hit_papers)
            boost = float(spec.get("boost", 0))
            score = (3 * len(hit_papers) + 2 * len(hit_repos)
                     + min(citations / 40.0, 6.0) + boost)
            level = max(level_for(score), int(spec.get("floor", 0)) if score else 0)

            if not level:
                continue

            hit_papers.sort(key=lambda p: int(p.get("citations") or 0), reverse=True)
            hit_repos.sort(key=lambda r: r["stars"], reverse=True)

            skills.append({
                "id": spec["id"],
                "name": spec["name"],
                "note": spec.get("note", ""),
                "level": level,
                "score": round(score, 1),
                "papers": len(hit_papers),
                "repos": len(hit_repos),
                "citations": citations,
                "signals": [term for term, _ in terms.most_common(6)],
                "evidence": {
                    "papers": [{
                        "title": p["title"],
                        "year": p.get("year", ""),
                        "citations": int(p.get("citations") or 0),
                        "url": p.get("url", ""),
                    } for p in hit_papers[:MAX_EVIDENCE]],
                    "repos": [{
                        "name": r["name"],
                        "url": r["url"],
                        "language": r["language"],
                        "description": r["description"][:110],
                    } for r in hit_repos[:MAX_EVIDENCE]],
                },
            })

        if not skills:
            continue

        skills.sort(key=lambda s: (-s["level"], -s["score"]))
        constellations.append({
            "id": group["id"],
            "name": group["name"],
            "spectral": group.get("spectral", "A"),
            "blurb": group.get("blurb", ""),
            "papers": len({p["title"] for s in skills
                           for p in s["evidence"]["papers"]}),
            "peak": max(s["level"] for s in skills),
            "skills": skills,
        })

    return constellations, matched_spans


def suggest(papers, repos, matched_spans, limit=40):
    """Frequent terms the taxonomy does not cover yet."""
    covered = " | ".join(matched_spans).lower()
    corpus = [p.get("title", "") for p in papers] + [repo_text(r) for r in repos]

    counts = collections.Counter()
    for text in corpus:
        words = [w for w in re.findall(r"[a-z][a-z\-]{2,}", text.lower())
                 if w not in STOPWORDS]
        counts.update(words)
        counts.update(f"{a} {b}" for a, b in zip(words, words[1:]))

    rows = [(term, n) for term, n in counts.items()
            if n >= 2 and term not in covered]
    rows.sort(key=lambda row: (-row[1], row[0]))
    return rows[:limit]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default=GITHUB_USER)
    parser.add_argument("--offline", action="store_true",
                        help="use the cached repo list instead of calling GitHub")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    taxonomy = load_taxonomy(TAXONOMY)
    papers, stats = load_papers(SCHOLAR)
    repos = fetch_repos(args.user, offline=args.offline)

    constellations, matched = build(taxonomy, papers, repos)
    tips = suggest(papers, repos, matched)

    payload = {
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
        "sources": {
            "papers": len(papers),
            "repos": len(repos),
            "citations": stats.get("citations_all", 0),
            "h_index": stats.get("h_index_all", 0),
        },
        "levels": ["Familiar", "Working", "Practised", "Fluent", "Signature"],
        "constellations": constellations,
    }

    total = sum(len(c["skills"]) for c in constellations)
    print(f"skilltree: {total} skills across {len(constellations)} constellations "
          f"from {len(papers)} papers and {len(repos)} repos")

    if args.dry_run:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    with open(OUTPUT, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=1)
        handle.write("\n")

    with open(SUGGESTIONS, "w", encoding="utf-8") as handle:
        handle.write("# Terms not yet in the taxonomy\n\n")
        handle.write(f"Generated {payload['generated']} from {len(papers)} paper "
                     f"titles and {len(repos)} repositories. Anything here worth "
                     "keeping should be added to `_data/skills.yml` by hand.\n\n")
        for term, count in tips:
            handle.write(f"- `{term}` &mdash; {count}\n")

    print(f"skilltree: wrote {OUTPUT} and {SUGGESTIONS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

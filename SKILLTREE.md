# Skill chart

A `/skills/` page for `ssegota.github.io` that draws your skills as a star
chart: ten constellations, one per research area, with each star's brightness
derived from how much published work and public code sits behind it.

## What goes where

| File | What it is |
|---|---|
| `_data/skills.yml` | The taxonomy. **The only file you edit by hand.** |
| `scripts/build_skilltree.py` | Reads evidence, scores it, writes the JSON. |
| `_data/skilltree.json` | Generated. Do not edit. |
| `_data/skill-suggestions.md` | Generated. Terms the taxonomy is missing. |
| `_includes/skilltree.html` | The chart: SVG, CSS and JS in one include. |
| `_pages/skills.md` | The page that includes it. |
| `.github/workflows/update-skilltree.yml` | Weekly rebuild. |
| `INSTRUCTIONS.md` | How to install it into the repo. |
| `scripts/fetch_scholar.py` | Your existing script, plus a `corpus` key. |

## Install

Step-by-step integration lives in `INSTRUCTIONS.md`. The short version: copy the
files in, add a `/skills/` entry to `_data/navigation.yml`, patch
`scripts/fetch_scholar.py` to keep the full title corpus, then

```bash
pip install pyyaml
python3 scripts/fetch_scholar.py
python3 scripts/build_skilltree.py
```

`_data/skilltree.json` is committed, so the site builds on GitHub Pages without
running Python.

## How scoring works

```
score = 3×papers + 2×repositories + min(citations ÷ 40, 6) + boost
level:   1 at score 1 · 2 at 7 · 3 at 15 · 4 at 30 · 5 at 55
```

Citations are capped so one 279-citation paper cannot carry a whole
constellation. `boost` in the taxonomy covers work that leaves no public trace
— teaching, supervision, the dAIgnostics and LiberiqAI work. Keep those honest;
they are the one place the chart can lie.

Thresholds live at the top of `build_skilltree.py` as `LEVEL_STEPS`.

## Keeping the taxonomy alive

Each rebuild writes `_data/skill-suggestions.md`: terms appearing twice or more
across your titles and repo descriptions that no pattern currently catches.
Skim it after a publishing run and promote anything real into `skills.yml`.

This is deliberate. Pure keyword extraction on titles gives you `using`,
`based`, `approach` and a flat bag of terms with no hierarchy — nothing you can
draw a tree from. So the structure stays curated and only the *weighting* is
automated. The suggestions file is how the curation stays cheap.

### Adding a skill

```yaml
      - id: rl
        name: Reinforcement Learning
        match: [reinforcement learning, q-learning, policy gradient, reward]
        langs: [Python]
        note: "One line shown in the detail panel."
```

Patterns match whole words, case-insensitively, and tolerate hyphens: `path
planning` matches "Path-Planning". Short patterns are the risky ones — `ga`
matched fine here, but check `skill-suggestions.md` and the printed signal list
after a rebuild.

### Removing a constellation

Delete its block. Ten is already near the top of what reads well; the layout
handles fewer gracefully and reflows to 5, 3, 2 or 1 columns by width.

## Design notes

Star magnitude is the load-bearing idea: astronomers rank stars by brightness,
so "how much evidence" maps onto the visual language without inventing a
convention. Constellation colours are stellar spectral classes (O through M)
plus three nebula hues where nine hues were needed. Stars at level 4 and up get
diffraction spikes, which is what a real chart does for the brightest objects.

The panel always shows the underlying papers and repositories. That is the
point — a skills page that cannot show its evidence is just a claim with
better typography.

## Known limits

- Google Scholar blocks CI, so the corpus refresh stays manual. ORCID
  (`https://pub.orcid.org/v3.0/0000-0002-3015-1024/works`) has a real JSON API
  and no blocking, and would be a better long-term source — swap it into
  `load_papers()` if you want the whole thing hands-off.
- None of your repos have GitHub topics set. Adding topics to the ten or so
  repos that matter would sharpen matching more than any change to the script.
- Level 5 is currently unreachable. That is intentional until the full corpus
  is in; check the top scores afterwards and adjust `LEVEL_STEPS` if nothing
  earns it.

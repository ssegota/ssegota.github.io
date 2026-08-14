# INSTRUCTIONS

Integrating the skill chart into `ssegota.github.io`. Full reference is in
`SKILLTREE.md`; this is just the install.

## 1. Copy the files

From the repo root, with this folder unpacked alongside it:

```bash
git checkout -b skill-chart
SRC=../skilltree

cp $SRC/_data/skills.yml              _data/
cp $SRC/_data/skilltree.json          _data/
cp $SRC/_data/skill-suggestions.md    _data/
cp $SRC/_data/.repos-cache.json       _data/
cp $SRC/_includes/skilltree.html      _includes/
cp $SRC/_pages/skills.md              _pages/
cp $SRC/scripts/build_skilltree.py    scripts/
cp $SRC/.github/workflows/update-skilltree.yml .github/workflows/
cp $SRC/SKILLTREE.md $SRC/INSTRUCTIONS.md .
```

Nothing collides with an existing file. Jekyll skips dotfiles and `.md` inside
`_data/`, so the cache and the suggestions list are inert at build time.

## 2. Patch `scripts/fetch_scholar.py`

Do this by hand rather than copying the file, in case you have edited it since.
In `main()`, add a `corpus` key straight after the `"cited":` line of `payload`:

```python
        "cited": sorted(cited, key=lambda row: row["citations"], reverse=True)[:args.top],
        # Every title Scholar returned, trimmed to what the skill chart needs.
        "corpus": [{"title": row["title"], "year": row["year"],
                    "citations": row["citations"], "url": row["url"]}
                   for row in cited],
```

`cited` already holds all ~100 rows before truncation, so the fetch itself does
not change.

## 3. Add the nav entry

In `_data/navigation.yml`, after the Publications block:

```yaml
  - title: "Skills"
    url: /skills/
```

## 4. Build

```bash
pip install pyyaml
python3 scripts/fetch_scholar.py      # run before the first build, see below
python3 scripts/build_skilltree.py
bundle exec jekyll serve              # http://localhost:4000/skills/
```

Run `fetch_scholar.py` from your own connection first. Google blocks CI, and
until the corpus is cached the chart scores against 20 papers instead of ~100 —
which is why Python currently outranks epidemiological modelling.

## 5. Commit

```bash
git add _data/skills.yml _data/skilltree.json _data/skill-suggestions.md \
        _data/.repos-cache.json _data/scholar.json _data/navigation.yml \
        _includes/skilltree.html _pages/skills.md \
        scripts/build_skilltree.py scripts/fetch_scholar.py \
        .github/workflows/update-skilltree.yml SKILLTREE.md INSTRUCTIONS.md
git commit -m "Add generated skill chart at /skills/"
git push -u origin skill-chart
```

`_data/skilltree.json` must be committed: the classic GitHub Pages build will
not run Python. The Action commits refreshes back to the repo instead.

## 6. Check the Action

After merging, run *Rebuild skill chart* once from the Actions tab. It should
finish in under a minute. It also fires whenever *Refresh Google Scholar data*
completes, so the two stay in step.

## Optional: full-width chart

Minimal Mistakes caps `.page__content` near 900px, so the chart settles on
three columns. It reflows by design, but for the full five-wide field add this
under the front matter of `_pages/skills.md`:

```html
<style>
.page__content .sky { width: 100vw; max-width: 1400px;
  margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw); }
@media (min-width: 1400px) { .page__content .sky {
  margin-left: calc(700px - 50%); margin-right: calc(700px - 50%); } }
</style>
```

## If the page is blank

Almost always a missing or malformed `_data/skilltree.json`. `skills.md` has an
`{% if %}` guard that prints a plain-text fallback instead, so a blank page with
no fallback text means Jekyll failed to load the include — check the build log
for `_includes/skilltree.html`.

## Routine maintenance

```bash
python3 scripts/fetch_scholar.py && python3 scripts/build_skilltree.py
```

Then skim `_data/skill-suggestions.md` and promote anything real into
`_data/skills.yml`. That file is the only one you edit by hand.

# ssegota.github.io

Personal academic website of Sandi Baressi Šegota,
[Faculty of Informatics, Juraj Dobrila University of Pula](https://fipu.unipu.hr) — live at
**[ssegota.github.io](https://ssegota.github.io)**.

Jekyll on the [Academic Pages](https://github.com/academicpages/academicpages.github.io) template,
served by GitHub Pages, which rebuilds on every push to `master`.

## The files you will actually edit

| To change… | Edit | Appears at |
| --- | --- | --- |
| Your biography on the front page | [`_pages/about.md`](_pages/about.md) | [/](https://ssegota.github.io/) |
| The five CV summaries (full → 250 chars) | [`_data/cv_summaries.yml`](_data/cv_summaries.yml) | [/cv/](https://ssegota.github.io/cv/) |
| Education, jobs, skills, awards, service | [`_data/cv.yml`](_data/cv.yml) | [/cv/](https://ssegota.github.io/cv/) and the PDF |
| Thesis topics for students | [`_pages/thesis-topics.md`](_pages/thesis-topics.md) | [/thesis-topics/](https://ssegota.github.io/thesis-topics/) |
| Special issues you edit | [`_data/editorial.yml`](_data/editorial.yml) | [/editorial/](https://ssegota.github.io/editorial/) |
| Courses you teach | [`_teaching/`](_teaching/) — one file per course | [/teaching/](https://ssegota.github.io/teaching/) |
| Talks you have given | [`_talks/`](_talks/) — one file per talk | [/talks/](https://ssegota.github.io/talks/) |
| The menu bar | [`_data/navigation.yml`](_data/navigation.yml) | every page |
| Profile links, e-mail, site title | [`_config.yml`](_config.yml) | sidebar, every page |
| Colours and dark mode | [`_sass/_gundam.scss`](_sass/_gundam.scss) | every page |
| Privacy / terms wording | [`_pages/terms.md`](_pages/terms.md) | [/terms/](https://ssegota.github.io/terms/) |

`_data/cv.yml` and `_data/cv_summaries.yml` feed both the web page and the PDF, so editing them
once updates both.

## The two scripts

```bash
python3 scripts/fetch_scholar.py     # refresh _data/scholar.json from Google Scholar
python3 scripts/build_cv_pdf.py      # rebuild files/CV_Sandi_Baressi_Segota.pdf
```

[`scripts/fetch_scholar.py`](scripts/fetch_scholar.py) rewrites
[`_data/scholar.json`](_data/scholar.json) with your ten most recent and ten most cited papers plus
the citation counts, which is what [/publications/](https://ssegota.github.io/publications/)
renders — it is now the only source for the publications page. A monthly GitHub Action
([`.github/workflows/update-scholar.yml`](.github/workflows/update-scholar.yml)) tries the same
thing, but Google blocks datacentre traffic often enough that it will frequently fail — when it
does, nothing is committed and the last good snapshot keeps serving. Running it yourself from a
normal connection always works; commit the changed JSON afterwards.

[`scripts/build_cv_pdf.py`](scripts/build_cv_pdf.py) regenerates the downloadable CV from
`_data/cv.yml`, `_data/cv_summaries.yml`, `_data/scholar.json`, `_teaching/` and `_talks/`, using
headless Chrome to print it. **Re-run it after editing any of those**, otherwise the PDF and the
web page drift apart.

## Adding an entry

Copy a neighbouring file in the same folder and edit its front matter. A course that should link
straight to an external course site uses `link` plus `redirect_to`:

```yaml
---
title: "Robotics"
collection: teaching
type: "Lectures"
permalink: /teaching/robotics
link: "https://robotika-fipu.netlify.app/"
redirect_to: "https://robotika-fipu.netlify.app/"
venue: "Faculty of Informatics - Juraj Dobrila University of Pula"
date: 2025-01-10
location: "Pula, Croatia"
---
```

Keep `permalink` unique inside a collection — two files sharing one silently overwrite each other.
Institution names in `venue` are turned into links automatically by
[`_includes/venue-link.html`](_includes/venue-link.html); add new ones there rather than putting
HTML in the front matter.

## Running it locally

```bash
bundle install
bundle exec jekyll serve -l -H localhost   # http://localhost:4000
```

## Talk map

[`talkmap.ipynb`](talkmap.ipynb) geocodes the `location` fields in `_talks/` and regenerates
`talkmap/`. Published at [/talkmap.html](https://ssegota.github.io/talkmap.html); set
`talkmap_link: true` in `_config.yml` to link it from the talks page.

## Licence

Site content © Sandi Baressi Šegota. Template is
[Academic Pages](https://github.com/academicpages/academicpages.github.io), MIT licensed (see
[`LICENSE`](LICENSE)).

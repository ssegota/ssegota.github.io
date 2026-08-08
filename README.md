# ssegota.github.io

Personal academic website of Sandi Baressi Šegota, Faculty of Informatics, Juraj Dobrila University
of Pula — live at [ssegota.github.io](https://ssegota.github.io).

Built with [Jekyll](https://jekyllrb.com/) on the
[Academic Pages](https://github.com/academicpages/academicpages.github.io) template and served by
GitHub Pages, which rebuilds the site on every push to `master`.

## Where the content lives

| What | Where | Shown at |
| --- | --- | --- |
| Biography (front page) | `_pages/about.md` | `/` |
| CV | `_pages/cv.md` | `/cv/` |
| Publications | `_publications/*.md` | `/publications/` |
| Talks | `_talks/*.md` | `/talks/` |
| Courses | `_teaching/*.md` | `/teaching/` |
| Thesis / project topics | `_pages/student-tasks.md` | `/student-tasks/` |
| Navigation bar | `_data/navigation.yml` | every page |
| Site-wide settings, profile links | `_config.yml` | every page |

`teme.md` in the repository root is the Croatian topic list; it is not published as a page.

## Adding an entry

Each publication, talk and course is a single Markdown file whose front matter drives the listing.
The simplest way to add one is to copy an existing file in the same folder and edit it.

A course entry that should link to an external course website uses the `link` field — the course title
in the listing then points there instead of to a local subpage, and `redirect_to` forwards the old
local URL as well:

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

Keep `permalink` unique across a collection — two files sharing one permalink silently overwrite each
other's page.

## Running it locally

```bash
bundle install
bundle exec jekyll serve -l -H localhost
```

The site is then available at <http://localhost:4000>.

## Talk map

`talkmap.ipynb` (or `talkmap.py`) geocodes the `location` fields of `_talks/*.md` and regenerates
`talkmap/`. The map is published at `/talkmap.html`; set `talkmap_link: true` in `_config.yml` to link
it from the talks page.

## Licence

Site content © Sandi Baressi Šegota. The underlying template is distributed under the MIT licence
(see `LICENSE`).

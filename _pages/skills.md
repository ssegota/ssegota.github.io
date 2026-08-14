---
layout: archive
title: "Skills"
permalink: /skills/
author_profile: true
---

{% include base_path %}

{% if site.data.skilltree.constellations %}

{% include skilltree.html %}

The chart is generated, not written. `scripts/build_skilltree.py` reads the
publication titles already cached in `_data/scholar.json` and the repository
list from the GitHub API, matches both against a taxonomy I maintain in
`_data/skills.yml`, and turns the number of matches into a brightness. A skill
with no paper and no repository behind it does not appear.

Levels come from one formula, applied the same way to everything:

`score = 3 × papers + 2 × repositories + min(citations ÷ 40, 6) + manual boost`

The manual boost exists for work that leaves no public trace &mdash; teaching,
supervision, review, industry projects &mdash; and is written down in the
taxonomy file rather than applied invisibly.

{% else %}

The skill chart has not been generated yet. Run `python3
scripts/build_skilltree.py` to create `_data/skilltree.json`.

{% endif %}

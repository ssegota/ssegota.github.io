---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

<div class="g-panel">
  <div class="g-controls">
    <a class="g-btn" href="{{ base_path }}/files/CV_Sandi_Baressi_Segota.pdf">Download CV (PDF)</a>
    <span class="g-meta">Biography summaries at five lengths are on the
      <a href="{{ base_path }}/">front page</a></span>
  </div>
</div>

Education
======

<ul>
{% for entry in site.data.cv.education %}
  <li><strong>{{ entry.degree }}</strong>, {{ entry.year }}<br>
  {% if entry.url %}<a href="{{ entry.url }}">{{ entry.org }}</a>{% else %}{{ entry.org }}{% endif %}</li>
{% endfor %}
</ul>

Work experience
======

<ul>
{% for entry in site.data.cv.experience %}
  <li><strong>{{ entry.role }}</strong>, {{ entry.period }}<br>
  {% if entry.url %}<a href="{{ entry.url }}">{{ entry.org }}</a>{% else %}{{ entry.org }}{% endif %}
  {%- if entry.note %} &mdash; {{ entry.note }}{% endif %}</li>
{% endfor %}
</ul>

Skills
======

<ul>
{% for group in site.data.cv.skills %}
  <li><strong>{{ group.group }}</strong>
    <ul>{% for item in group.items %}<li>{{ item }}</li>{% endfor %}</ul>
  </li>
{% endfor %}
</ul>

Awards
======

<ul>
{% for award in site.data.cv.awards %}
  <li><strong>{{ award.year }}</strong> &mdash; {{ award.text }}</li>
{% endfor %}
</ul>

Publications
======

{% if site.data.scholar.cited and site.data.scholar.cited.size > 0 %}
  <p class="g-meta">Ten most cited, from <a href="{{ site.author.googlescholar }}">Google Scholar</a>. The
  <a href="{{ base_path }}/publications/">publications page</a> has the full list and the most recent work.</p>
  <ol>
  {% for paper in site.data.scholar.cited %}
    <li>{{ paper.authors }} ({{ paper.year }}). <a href="{{ paper.url }}">{{ paper.title }}</a>.
    <i>{{ paper.venue }}</i>{% if paper.citations > 0 %} &mdash; {{ paper.citations }} citations{% endif %}</li>
  {% endfor %}
  </ol>
{% else %}
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
{% endif %}

Talks
======
  <ul>{% for post in site.talks reversed %}
    {% include archive-single-talk-cv.html  %}
  {% endfor %}</ul>

Teaching
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>

Service and leadership
======

<ul>
{% for item in site.data.cv.service %}
  <li>{{ item }}</li>
{% endfor %}
</ul>


---
layout: archive
title: "Editorial Work"
permalink: /editorial/
author_profile: true
redirect_from:
  - /editorial-work/
  - /special-issues/
---

{% include base_path %}

<p>Special issues and topical collections currently open for submissions. Contributions within scope
are welcome &mdash; if you are unsure whether your work fits, write to
<a href="mailto:{{ site.author.email }}">{{ site.author.email }}</a> before preparing a full
manuscript.</p>

{% assign now = site.time | date: '%s' | plus: 0 %}

{% for issue in site.data.editorial %}
  {% assign closes = issue.deadline_iso | date: '%s' | plus: 0 %}
  <div class="list__item">
    <article class="archive__item">
      <h2 class="archive__item-title">
        <a href="{{ issue.url }}" target="_blank" rel="noopener">{{ issue.title }}
        <i class="fa fa-arrow-up-right-from-square" aria-hidden="true" title="external link"></i><span class="sr-only">(external link)</span></a>
      </h2>

      <p class="page__meta">
        {{ issue.journal }}{% if issue.journal_detail %} ({{ issue.journal_detail }}){% endif %}
        &middot; {{ issue.publisher }} &middot; {{ issue.role }}
      </p>

      <p class="g-deadline{% if closes < now %} g-deadline--closed{% endif %}">
        {% if closes < now %}Closed &mdash; deadline was {{ issue.deadline }}
        {%- else %}Open for submissions &mdash; deadline {{ issue.deadline }}{% endif %}
      </p>

      {{ issue.description | markdownify }}

      {% if issue.topics %}
      <p><strong>Topics of interest include:</strong></p>
      <ul>
        {% for topic in issue.topics %}<li>{{ topic }}</li>{% endfor %}
      </ul>
      {% endif %}

      <p><a class="g-btn" href="{{ issue.url }}" target="_blank" rel="noopener">View the call at {{ issue.publisher }}</a></p>
    </article>
  </div>
{% endfor %}

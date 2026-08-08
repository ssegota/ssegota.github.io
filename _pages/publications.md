---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% include base_path %}

{% assign scholar = site.data.scholar %}

{% if scholar.cited and scholar.cited.size > 0 %}

<div class="g-panel">
  <span class="g-eyebrow">Google Scholar</span>
  <div class="g-controls">
    <button type="button" class="g-btn" id="pub-recent" aria-pressed="true">Ten most recent</button>
    <button type="button" class="g-btn" id="pub-cited" aria-pressed="false">Ten most cited</button>
    <span class="g-meta">
      {{ scholar.stats.citations_all }} citations &middot;
      h-index {{ scholar.stats.h_index_all }} &middot;
      i10 {{ scholar.stats.i10_all }} &middot;
      updated {{ scholar.fetched }}
    </span>
  </div>
</div>

<div id="pub-list-recent">
  {% for paper in scholar.recent %}
  <div class="list__item">
    <article class="archive__item">
      <h2 class="archive__item-title"><a href="{{ paper.url }}" rel="noopener">{{ paper.title }}</a></h2>
      <p class="page__meta">{{ paper.year }}{% if paper.venue != "" %} &middot; {{ paper.venue }}{% endif %}{% if paper.citations > 0 %} &middot; {{ paper.citations }} citations{% endif %}</p>
      <p class="archive__item-excerpt">{{ paper.authors }}</p>
    </article>
  </div>
  {% endfor %}
</div>

<div id="pub-list-cited" hidden>
  {% for paper in scholar.cited %}
  <div class="list__item">
    <article class="archive__item">
      <h2 class="archive__item-title"><a href="{{ paper.url }}" rel="noopener">{{ paper.title }}</a></h2>
      <p class="page__meta">{{ paper.citations }} citations &middot; {{ paper.year }}{% if paper.venue != "" %} &middot; {{ paper.venue }}{% endif %}</p>
      <p class="archive__item-excerpt">{{ paper.authors }}</p>
    </article>
  </div>
  {% endfor %}
</div>

<p class="g-meta" style="margin-top:1.5em">
  Full list on <a href="{{ scholar.profile_url }}">Google Scholar</a>{% if site.author.orcid %},
  <a href="{{ site.author.orcid }}">ORCID</a>{% endif %}{% if site.author.researchgate %} and
  <a href="{{ site.author.researchgate }}">ResearchGate</a>{% endif %}.
</p>

{% if site.publications.size > 0 %}
Selected papers with abstracts
======

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
{% endif %}

<script>
  // Switch between the two Scholar lists. Both are already in the page.
  (function () {
    var buttons = {
      recent: document.getElementById('pub-recent'),
      cited:  document.getElementById('pub-cited')
    };
    var lists = {
      recent: document.getElementById('pub-list-recent'),
      cited:  document.getElementById('pub-list-cited')
    };
    if (!buttons.recent || !lists.recent) return;

    function show(which) {
      Object.keys(lists).forEach(function (key) {
        lists[key].hidden = (key !== which);
        buttons[key].setAttribute('aria-pressed', String(key === which));
      });
    }

    Object.keys(buttons).forEach(function (key) {
      buttons[key].addEventListener('click', function () { show(key); });
    });
  })();
</script>

{% else %}

{% if site.author.googlescholar %}
  <div class="wordwrap">The automatic Google Scholar list is unavailable right now. You can find all
  articles on <a href="{{ site.author.googlescholar }}">my Google Scholar profile</a>.</div>
{% endif %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}

{% endif %}

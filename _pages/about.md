---
permalink: /
title: "About Me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% include base_path %}

{% comment %}
  The biography shown on load is the one flagged `default: true` in
  _data/cv_summaries.yml, falling back to the first entry. The switch itself
  stays in file order, longest to shortest.
{% endcomment %}
{% assign default_bio = site.data.cv_summaries | where: "default", true | first %}
{% unless default_bio %}{% assign default_bio = site.data.cv_summaries | first %}{% endunless %}

<div class="bio">
  {% for summary in site.data.cv_summaries %}
    {% assign plain = summary.text | markdownify | strip_html | strip %}
    <div class="bio__text" data-id="{{ summary.id }}"
         data-words="{{ plain | number_of_words }}"
         data-chars="{{ plain | size }}"
         {% unless summary.id == default_bio.id %}hidden{% endunless %}>
      {{ summary.text | markdownify }}
    </div>
  {% endfor %}

  <p class="g-switch">
    <span class="g-switch__label">Read the</span>
    {% for summary in site.data.cv_summaries %}
      <button type="button" class="g-switch__option" data-id="{{ summary.id }}"
              aria-pressed="{% if summary.id == default_bio.id %}true{% else %}false{% endif %}">{{ summary.label }}</button>
    {% endfor %}
    <span class="g-switch__count" id="bio-count"></span>
  </p>
</div>

<p>
Recent and most cited work is on the
<a href="{{ base_path }}/publications/">publications</a> page, and the full CV, including a PDF, is
<a href="{{ base_path }}/cv/">here</a>.
</p>

## Skills

{% if site.data.skilltree.constellations %}

{% include skilltree.html %}

<p>
The chart is generated rather than written: every star is scored from the
publications and public repositories that actually stand behind it. See
<a href="{{ base_path }}/skills/">the full skill chart</a> for how the levels
are derived.
</p>

{% endif %}


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
  <span class="g-eyebrow">Profile summary</span>
  <div class="g-controls">
    <label class="sr-only" for="cv-summary-pick">Summary length</label>
    <select id="cv-summary-pick" class="g-select">
      {% for summary in site.data.cv_summaries %}
        <option value="{{ summary.id }}">{{ summary.label }}</option>
      {% endfor %}
    </select>
    <button type="button" class="g-btn" id="cv-summary-copy">Copy text</button>
    <a class="g-btn" href="{{ base_path }}/files/CV_Sandi_Baressi_Segota.pdf">Download CV (PDF)</a>
    <span class="g-meta" id="cv-summary-count"></span>
  </div>
  <div class="g-readout">
    {% for summary in site.data.cv_summaries %}
      {% assign plain = summary.text | markdownify | strip_html | strip %}
      <div class="cv-summary" data-id="{{ summary.id }}"
           data-words="{{ plain | number_of_words }}"
           data-chars="{{ plain | size }}"
           {% unless forloop.first %}hidden{% endunless %}>
        {{ summary.text | markdownify }}
      </div>
    {% endfor %}
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

<script>
  // Profile summary picker: all five versions are in the page, one visible.
  (function () {
    var picker  = document.getElementById('cv-summary-pick');
    var copyBtn = document.getElementById('cv-summary-copy');
    var count   = document.getElementById('cv-summary-count');
    var blocks  = Array.prototype.slice.call(document.querySelectorAll('.cv-summary'));
    if (!picker || !blocks.length) return;

    function visible() {
      return blocks.filter(function (b) { return !b.hidden; })[0] || blocks[0];
    }

    function show(id) {
      blocks.forEach(function (b) { b.hidden = (b.dataset.id !== id); });
      var block = visible();
      count.textContent = block.dataset.words + ' words / ' + block.dataset.chars + ' characters';
    }

    picker.addEventListener('change', function () { show(picker.value); });
    show(picker.value);

    copyBtn.addEventListener('click', function () {
      var text = visible().innerText.trim();
      var done = function (ok) {
        copyBtn.textContent = ok ? 'Copied' : 'Copy failed';
        setTimeout(function () { copyBtn.textContent = 'Copy text'; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { done(true); },
                                                 function () { done(false); });
      } else {
        // Older browsers: bounce it through a throwaway textarea.
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.style.position = 'absolute';
        ta.style.left = '-9999px';
        document.body.appendChild(ta);
        ta.select();
        var ok = false;
        try { ok = document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta);
        done(ok);
      }
    });
  })();
</script>

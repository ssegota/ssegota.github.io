---
permalink: /
title: "About Me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% include base_path %}

<div class="bio">
  {% for summary in site.data.cv_summaries %}
    {% assign plain = summary.text | markdownify | strip_html | strip %}
    <div class="bio__text" data-id="{{ summary.id }}"
         data-words="{{ plain | number_of_words }}"
         data-chars="{{ plain | size }}"
         {% unless forloop.first %}hidden{% endunless %}>
      {{ summary.text | markdownify }}
    </div>
  {% endfor %}

  <p class="g-switch">
    <span class="g-switch__label">Read the</span>
    {% for summary in site.data.cv_summaries %}
      <button type="button" class="g-switch__option" data-id="{{ summary.id }}"
              aria-pressed="{% if forloop.first %}true{% else %}false{% endif %}">{{ summary.label }}</button>
    {% endfor %}
    <span class="g-switch__count" id="bio-count"></span>
  </p>
</div>

<p>
Students looking for a bachelor’s or master’s thesis topic will find a current list on the
<a href="{{ base_path }}/thesis-topics/">thesis topics</a> page. Recent and most cited work is on the
<a href="{{ base_path }}/publications/">publications</a> page, and the full CV, including a PDF, is
<a href="{{ base_path }}/cv/">here</a>.
</p>

<script>
  // Biography length switch. All five versions ship in the page; one is shown.
  (function () {
    var texts   = Array.prototype.slice.call(document.querySelectorAll('.bio__text'));
    var options = Array.prototype.slice.call(document.querySelectorAll('.g-switch__option'));
    var count   = document.getElementById('bio-count');
    if (!texts.length || !options.length) return;

    function show(id) {
      texts.forEach(function (t) { t.hidden = (t.dataset.id !== id); });
      options.forEach(function (o) {
        o.setAttribute('aria-pressed', String(o.dataset.id === id));
      });
      var active = texts.filter(function (t) { return !t.hidden; })[0];
      if (active && count) {
        count.textContent = active.dataset.words + ' words / ' + active.dataset.chars + ' characters';
      }
    }

    options.forEach(function (o) {
      o.addEventListener('click', function () { show(o.dataset.id); });
    });
    show(texts[0].dataset.id);
  })();
</script>

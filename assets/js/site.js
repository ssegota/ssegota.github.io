/*
 * Site behaviour: theme switch, biography length switch, publications switch.
 *
 * This lives in an external file on purpose. The `compress` layout strips
 * newlines from the HTML it wraps, which collapses any inline <script> onto a
 * single line - a `//` comment there silently comments out the rest of the
 * script. Jekyll 4 (local) and Jekyll 3 (GitHub Pages) differ here, so an
 * inline block can work locally and be dead once deployed. Keep page
 * JavaScript in this file rather than in the pages.
 *
 * Every block below is a no-op when its elements are absent, so the same file
 * is safe to load on every page.
 */
(function () {
  'use strict';

  /* ---- Light / dark switch ------------------------------------------------
     The active theme is already on <html>; the head sets it before first paint
     so the page never flashes. This only toggles and remembers. */
  function themeSwitch() {
    var button = document.getElementById('theme-switch');
    if (!button) return;

    button.addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-theme') === 'dark'
        ? 'light'
        : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try {
        window.localStorage.setItem('theme', next);
      } catch (e) {
        /* private browsing: the choice just will not persist */
      }
    });
  }

  /* ---- Biography length switch (front page) -------------------------------
     All five versions are in the page; exactly one is visible. */
  function bioSwitch() {
    var texts = Array.prototype.slice.call(document.querySelectorAll('.bio__text'));
    var options = Array.prototype.slice.call(document.querySelectorAll('.g-switch__option'));
    var count = document.getElementById('bio-count');
    if (!texts.length || !options.length) return;

    function show(id) {
      texts.forEach(function (text) {
        text.hidden = (text.getAttribute('data-id') !== id);
      });
      options.forEach(function (option) {
        option.setAttribute('aria-pressed',
          String(option.getAttribute('data-id') === id));
      });

      var active = texts.filter(function (text) { return !text.hidden; })[0];
      if (active && count) {
        count.textContent = active.getAttribute('data-words') + ' words / ' +
                            active.getAttribute('data-chars') + ' characters';
      }
    }

    options.forEach(function (option) {
      option.addEventListener('click', function () {
        show(option.getAttribute('data-id'));
      });
    });

    /* Start on whichever version the page left visible - that is the one
       flagged `default: true` in _data/cv_summaries.yml, not necessarily the
       first in the switch. */
    var initial = texts.filter(function (text) { return !text.hidden; })[0]
      || texts[0];
    show(initial.getAttribute('data-id'));
  }

  /* ---- Publications: most recent / most cited ----------------------------- */
  function publicationsSwitch() {
    var lists = {
      recent: document.getElementById('pub-list-recent'),
      cited: document.getElementById('pub-list-cited')
    };
    var buttons = {
      recent: document.getElementById('pub-recent'),
      cited: document.getElementById('pub-cited')
    };
    if (!lists.recent || !lists.cited || !buttons.recent || !buttons.cited) return;

    function show(which) {
      Object.keys(lists).forEach(function (key) {
        lists[key].hidden = (key !== which);
        buttons[key].setAttribute('aria-pressed', String(key === which));
      });
    }

    Object.keys(buttons).forEach(function (key) {
      buttons[key].addEventListener('click', function () { show(key); });
    });
  }

  function init() {
    themeSwitch();
    bioSwitch();
    publicationsSwitch();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

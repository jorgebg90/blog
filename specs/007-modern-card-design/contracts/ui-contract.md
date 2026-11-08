# UI Contract: Modern Card Design

## Card include
```liquid
{% include card.html eyebrow=... title=... description=... url=... link_text=... featured=true %}
```
Rendered markup:
```html
<article class="card card--featured">
  <p class="card__eyebrow">EYEBROW</p>
  <h2 class="card__title"><a href="URL">Title</a></h2>
  <p class="card__desc">Description</p>
  <a class="card__link" href="URL">Read →</a>
</article>
```
Accessibility: if both links are kept, the arrow link uses `aria-label` including the title; alternatively a single focusable link per card (decide at implementation, prefer one tab stop).

## Stable class hooks
`.card`, `.card--featured`, `.card__eyebrow`, `.card__title`, `.card__desc`, `.card__link`, `.card-list`, `.site-title` (wordmark), `.lang-switch`, `.lang-switch__btn`, `.is-active`.

## Preserved contracts (must not change)
- `.lang-switch` data-attributes and hrefs consumed by `assets/js/language-session.js` (it does not read `aria-current`).
- hreflang output of `hreflang-links.html`; permalinks; translation-unavailable banner.
- Switcher: active language exposes `aria-current`.

## Visual contract (tokens)
Background #f5f8fd; text #0f1b33; accent ≈ #1a56db; card radius 20px; 1px border; featured border = accent; focus ring 3px accent; transitions disabled under `prefers-reduced-motion: reduce`.

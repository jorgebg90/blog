# Validation Results: Modern Card Design

## Build (T025)
- `bundle exec jekyll build` succeeds (remote_theme fetched OK). Only pre-existing Sass deprecation warnings from `main.scss`.

## Visual (T026)
Headless Chromium via Playwright MCP, served from `_site` under `/blog/`.
- Screenshots reviewed: Home es (375, 1280), Home en (1280), Posts index en/es (375), Post es (375), Post en (1280), About es (375), About en (1280).
- Horizontal overflow check (documentElement scrollWidth vs. viewport minus 15px scrollbar) at 320/375/768/1280 for all 8 variants (Home/Index/Post/Page x es/en): no overflow.
- Not individually eyeballed: Home en 375, Index en 1280, Index es 1280, Post en 375, Post es 1280, About en 375, About es 1280 (covered only by the overflow check). 200% zoom, empty list and very long titles not exercised (only one post per language exists).

## Contrast (T027) — computed ratios
Light: text/bg 16.1, muted/bg 6.7, muted/white 7.1, accent/white 6.2, accent/bg 5.8, accent/pill 4.8, white on accent button 6.2.
Dark: text 15.8, muted 8.2–9.0, accent 7.0–7.7. All >= 4.5:1. Dark mode was not visually checked.

## Keyboard (T028)
- Each card has exactly one focusable link (title; the "Read →" text is `aria-hidden` and the title link is stretched over the card). Focus shows a 3px accent ring on the card (`:focus-within`) and on other controls (`:focus-visible`). Verified by markup/CSS inspection, not by an interactive Tab run.

## Reduced motion (T029)
- All transitions and the hover lift are inside `@media (prefers-reduced-motion: no-preference)`. Verified by CSS inspection.

## SEO / performance (T030, T024)
- `<head>` diff vs. baseline for all 10 built HTML files: only change is the added Inter stylesheet (+2 preconnect hints) and the `overrides.css` cache-buster. Titles, meta, canonical and hreflang are unchanged.
- Language-switcher `data-target-*`, `data-has-equivalent-*`, `data-translation-mode` are byte-identical to baseline for every page.
- Inter could not be loaded in the sandbox (external request blocked), so rendering used the system-sans fallback; Inter appearance unverified.

## Notes
- Home front matter (`site/en/index.markdown`, `site/es/index.markdown`): `show_inline_posts` changed false → true so Home shows the featured card, and an `eyebrow` was added.

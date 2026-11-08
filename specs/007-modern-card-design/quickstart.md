# Quickstart: Modern Card Design

1. Build: `bundle exec jekyll build` (must succeed).
2. Serve: `bundle exec jekyll serve` and open `/`, `/es/`, `/posts/`, `/es/posts/`, one post per language, `/about/`, `/es/about/`.
3. Check each of the 8 variants at 320, 375, 768, 1280px: no horizontal scroll; tinted background, navy text, blue wordmark left, pill switcher right, cards (first with blue border), thin footer divider.
4. Switcher: click EN↔ES on About and on a post with and without translation; destinations must match pre-change behavior (compare with `main`).
5. Keyboard: Tab through header, cards, switcher; focus ring always visible.
6. Reduced motion: enable OS/browser setting; no transitions.
7. Contrast: verify body, muted, accent text, and focus ring against AA.
8. SEO: diff `<head>` (title, meta, hreflang) vs. `main`; only one extra font request.
9. Rollback: revert edits to `overrides.css`, layouts, `card.html`, `messages.yml`, `head/custom.html`.

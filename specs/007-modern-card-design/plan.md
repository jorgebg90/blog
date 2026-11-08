# Implementation Plan: Modern Card Design

**Branch**: `007-modern-card-design` | **Date**: 2026-11-08 | **Spec**: `specs/007-modern-card-design/spec.md`
**Input**: Feature specification from `/specs/007-modern-card-design/spec.md`

## Summary

Restyle Home, Posts Index, Post, and Page (ES/EN) to the jblueprint.dev look: tinted background, navy text, bold tight headings, uppercase blue eyebrows, rounded white cards (first card featured with blue border), bold blue wordmark, pill language switcher, thin footer divider. Delivery is CSS design tokens plus small markup edits to existing layouts/includes. No URL, hreflang, switcher-target, or JS logic changes.

## Technical Context

**Language/Version**: Jekyll 4.4.1, Liquid, HTML, SCSS/CSS.
**Primary Dependencies**: `minimal-mistakes` remote theme (existing); no new gems, plugins or JS.
**Storage**: N/A (static files; localized strings in `_data/messages.yml`).
**Testing**: `bundle exec jekyll build`; manual/Playwright visual checks of 8 variants (Home/Index/Post/Page × es/en) at 320/375/768/1280px; WCAG AA contrast check; keyboard focus pass; reduced-motion check; switcher destination comparison before vs. after.
**Target Platform**: Static GitHub Pages-compatible site, modern browsers.
**Project Type**: Static multilingual blog (single Jekyll project).
**Performance Goals**: At most one extra font request (Inter, `display=swap`, system-sans fallback); no CSS payload regression beyond modest growth.
**Constraints**: Presentation-layer only; preserve spec 006 conventions; light mode primary, dark mode adapted via tokens; no horizontal scroll ≥320px.
**Scale/Scope**: 4 layouts × 2 languages; 2 includes (masthead, language-switcher) plus footer.

### Grounding: existing state (read before planning)

- `_layouts/default.html`: includes head, masthead, translation-feedback, `#main`, `#footer`, scripts, `language-session.js`.
- `_layouts/home.html`: hero (`home-hero`), `divider--subtle`, content, inline posts as a plain `ul.post-list` (date + h2 link).
- `_layouts/posts-index.html`: header + `ul.post-list` with translation_key de-dup and empty state; `li` has `.post-meta`, `h2 > a.post-link`, `.post-excerpt`.
- `_layouts/post.html`: bridge to MM `single`; only adds reading-time badge and script. `_layouts/page.html`: MM-style page layout.
- `_includes/masthead.html`: MM greedy-nav, `.site-title` and nav from `_data/navigation.yml`, includes language switcher. `language-switcher.html`: `.lang-switch` with `EN | ES` links, `is-active`, `aria-current="true"`, data-attributes consumed by `language-session.js` (must remain untouched).
- `_includes/footer.html` is empty; `_includes/head/custom.html` loads `assets/css/overrides.css?v=…` (currently 21 lines of hotfixes). `assets/css/main.scss` (1078 lines) imports the MM skin plus 006 tokens (`$space-token-*`, rhythm, motion) and Home/About/404 styles.
- No web font is currently loaded (`$sans-serif` from MM only).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] English-only implementation: code, comments, config keys in English (localized UI strings live in data files only).
- [x] Jekyll-first compliance: uses layouts, includes, `_data`, `assets/`, and MM override mechanism.
- [x] Conventional structure: one new include (`_includes/card.html`) and one stylesheet change; no plugins.
- [x] Build validation: `bundle exec jekyll build` required after each increment.
- [x] Change scope: split into focused increments (tokens → header → card → layouts → a11y/validation).

**Gate Status (Pre-Phase 0)**: PASS
**Gate Status (Post-Phase 1)**: PASS

## Design Decisions (summary; details in `research.md`)

1. Tokens as CSS custom properties in `assets/css/overrides.css` (loaded after `main.css`, already wired in `head/custom.html`); bump its `?v=` cache-buster. Legacy SCSS in `main.scss` is only touched where it conflicts (06 hero/post-list rules).
2. Reusable `_includes/card.html` (params: eyebrow, title, description, url, link_text, featured) used by Home and Posts Index.
3. Eyebrow/link text localization via new `_data/messages.yml` keys (`eyebrow_posts`, `eyebrow_reading`, `card_read`) with per-page front matter overrides.
4. Language switcher: markup keeps data attributes and hrefs; CSS turns it into a pill; drop the `|` separator visually (`display: none`); keep `aria-current`. Switch to `aria-current="page"`-compatible value only if JS does not rely on it (verify in `language-session.js`).
5. Wordmark: restyle existing `.site-title`; no markup change beyond optional nav tweak.
6. Font: Inter via a single non-blocking `<link>` (preconnect + `display=swap`) in `head/custom.html`, fallback `system-ui` stack.
7. Footer divider: `border-top` on `#footer`; `footer.html` stays empty.
8. Dark mode: tokens redefined under `@media (prefers-color-scheme: dark)`.
9. Motion: transitions only inside `@media (prefers-reduced-motion: no-preference)`.

## Project Structure

### Documentation (this feature)

```text
specs/007-modern-card-design/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── ui-contract.md
├── checklists/
└── tasks.md             # created later by /speckit.tasks
```

### Source Code (repository root)

```text
_layouts/
├── home.html            # eyebrow hero; posts rendered via card include
├── posts-index.html     # cards via include; keep dedup + empty state
├── post.html            # eyebrow + reading-time wrapper
└── page.html            # eyebrow + class hooks only
_includes/
├── card.html            # NEW reusable card
├── masthead.html        # class hooks for wordmark/pill positioning
├── language-switcher.html  # pill styling hooks only
└── head/custom.html     # font link + overrides.css version bump
_data/
└── messages.yml         # localized eyebrow / link strings
assets/css/
├── overrides.css        # tokens + new visual system
└── main.scss            # remove/neutralize conflicting 006 rules
```

**Structure Decision**: Single Jekyll project; changes confined to existing layout/include/CSS files plus one new include.

## Increments

1. **Tokens & base**: palette, typography, font loading, body/headings, focus ring, reduced motion.
2. **Header & footer**: wordmark, pill switcher, footer divider.
3. **Card component**: include + CSS; featured state.
4. **Layout adoption**: Home, Posts Index, Post, Page eyebrows and spacing; MM leftovers (tables, TOC, pagination, code) harmonized.
5. **Validation**: build, 8 variants × 4 widths, contrast, keyboard, reduced motion, switcher/fallback parity, SEO diff.

## Risks

- MM specificity overrides → use `.layout--*` scoping, avoid `!important`.
- Switcher JS coupling → no change to data-attributes/hrefs; verify `aria-current` value usage.
- Blue contrast: #1a56db on #f5f8fd ≈ 6:1 (passes); verify at implementation.

## Complexity Tracking

No constitution violations.

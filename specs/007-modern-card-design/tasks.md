# Tasks: Modern Card Design

**Input**: Design documents from `/specs/007-modern-card-design/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ui-contract.md, quickstart.md
**Tests**: Not requested; validation is build + manual/Playwright checks per quickstart.md (Polish phase).
**Rule**: Run `bundle exec jekyll build` after each increment. All code/comments in English.

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

---

## Phase 1: Setup

- [X] T001 Capture baseline from `main`: build output `<head>` (title, meta, hreflang) and language-switcher destinations for Home, Posts Index, one post (with/without translation), About in es/en; save notes in `specs/007-modern-card-design/checklists/baseline.md`
- [X] T002 [P] Confirm `assets/js/language-session.js` does not read `aria-current` (only data-attributes/hrefs) and note result in `specs/007-modern-card-design/research.md` R-005
- [X] T003 [P] Review `assets/css/overrides.css`, `assets/css/main.scss` (006 hero/post-list rules) and `_includes/head/custom.html` to list conflicting selectors to neutralize

---

## Phase 2: Foundational (blocks all stories)

- [X] T004 Add design tokens (`--bg`, `--surface`, `--text`, `--muted`, `--accent`, `--card`, `--border`, `--radius`, `--space-*`, `--font-sans`) to `assets/css/overrides.css`, with dark overrides under `@media (prefers-color-scheme: dark)`
- [X] T005 Add base styles in `assets/css/overrides.css`: tinted body background, navy text, bold tight-tracked headings, links harmonized, readable line length, no horizontal overflow (images/code/tables)
- [X] T006 Add `:focus-visible` 3px accent outline with offset and wrap all transitions in `@media (prefers-reduced-motion: no-preference)` in `assets/css/overrides.css`
- [X] T007 [P] Add Inter font (single `<link>` with preconnect + `display=swap`, system-sans fallback in `--font-sans`) and bump `overrides.css?v=` in `_includes/head/custom.html`
- [X] T008 [P] Add localized keys `eyebrow_posts`, `eyebrow_reading`, `card_read` (en/es) to `_data/messages.yml`
- [X] T009 Create reusable card include per `contracts/ui-contract.md` (params eyebrow, title, description, url, link_text, featured; omit eyebrow when blank; single tab stop per card; `relative_url`) in `_includes/card.html`
- [X] T010 Add card component CSS (`.card`, `.card--featured`, `.card__eyebrow` uppercase blue, `.card__title`, `.card__desc` muted, `.card__link` bold blue, `.card-list`; 20px radius, 1px border, featured accent border, subtle hover, long-text wrapping) in `assets/css/overrides.css`
- [X] T011 Neutralize conflicting 006 `home-hero`/`post-list` rules in `assets/css/main.scss` (no `!important`; scope via `.layout--*`)

**Checkpoint**: `bundle exec jekyll build` passes.

---

## Phase 3: User Story 1 - Modern brand on Home (P1) 🎯 MVP

**Goal**: Home (es/en) shows tinted page, blue wordmark, pill switcher, eyebrow hero, cards with featured first card, footer divider.
**Independent Test**: Load `/` and `/es/` at 375 and 1280px; compare with reference.

- [X] T012 [P] [US1] Add wordmark and header layout hooks (flex `space-between`, bold blue tight-tracked `.site-title`) in `_includes/masthead.html` and `assets/css/overrides.css`
- [X] T013 [P] [US1] Restyle `.lang-switch` as pill (active white pill + blue text, inactive muted, hide `|` separator visually, add `.lang-switch__btn` class hook, keep data-attributes/hrefs/`aria-current`) in `_includes/language-switcher.html` and `assets/css/overrides.css`
- [X] T014 [P] [US1] Add thin footer divider (`#footer { border-top: 1px solid var(--border) }`) in `assets/css/overrides.css` (keep `_includes/footer.html` empty)
- [X] T015 [US1] Update `_layouts/home.html`: eyebrow above hero title (front matter `eyebrow` or `messages.yml` default) and render inline posts via `{% include card.html %}` inside `.card-list`, first card `featured`; keep empty state
- [X] T016 [US1] Style Home hero/eyebrow spacing and responsive card grid/stack (320–1280px) in `assets/css/overrides.css`

---

## Phase 4: User Story 2 - Posts Index and Post (P2)

**Goal**: Index shows cards (newest featured); Post uses same palette, eyebrow, readable body.
**Independent Test**: Open `/posts/`, `/es/posts/`, one post per language.

- [X] T017 [US2] Update `_layouts/posts-index.html` to use `card.html` in `.card-list`, keep translation_key de-dup and empty state, set featured via flag on first visible (post-dedup) item
- [X] T018 [P] [US2] Update `_layouts/post.html`: localized eyebrow (`eyebrow_reading`) and reading-time wrapper hooks, no script changes
- [X] T019 [US2] Add Post styles in `assets/css/overrides.css`: bold title, navy body, readable line length, code/blockquote/images/tables no mobile overflow
- [X] T020 [US2] Style translation-unavailable banner and fallback notices consistently in `assets/css/overrides.css` (markup/logic unchanged)
- [X] T021 [P] [US2] Harmonize MM leftovers (TOC, pagination, tables, code, search) with tokens in `assets/css/overrides.css`

---

## Phase 5: User Story 3 - Page layouts and switching coherence (P3)

**Goal**: Page layout shares the system; switching lands on same destinations as before.
**Independent Test**: About es → en → es; destinations match baseline.

- [X] T022 [US3] Update `_layouts/page.html`: eyebrow (front matter `eyebrow`, omitted when blank) and class hooks only
- [X] T023 [US3] Add Page styles (title, content width, spacing) in `assets/css/overrides.css`
- [X] T024 [US3] Compare switcher destinations and hreflang/`<head>` output vs. baseline (T001) for About, a post with and without translation; fix any regression

---

## Phase 6: Polish & Validation

- [X] T025 Run `bundle exec jekyll build` and fix warnings/errors
- [X] T026 Visual check of 8 variants (Home/Index/Post/Page × es/en) at 320/375/768/1280px with no horizontal scroll (Playwright or manual); incl. single-card, empty list, long titles, 200% zoom
- [X] T027 [P] WCAG AA contrast check (body, muted, accent on white and tint, focus ring, dark mode) and adjust tokens in `assets/css/overrides.css`
- [X] T028 [P] Keyboard pass: tab through header, cards, switcher; focus always visible
- [X] T029 [P] Reduced-motion check: no transitions observed
- [X] T030 [P] SEO/performance: `<head>` diff vs. baseline unchanged; only one additional font request
- [X] T031 Update `specs/007-modern-card-design/quickstart.md` if steps changed and record results in `specs/007-modern-card-design/checklists/validation.md`

---

## Dependencies & Order

- Phase 1 → Phase 2 → Phases 3–5 → Phase 6.
- US1 (MVP) depends only on Foundational. US2 and US3 depend on Foundational (card include/CSS, header/footer from US1 are site-wide but not blocking); US2 and US3 can run in parallel after Phase 2.
- Same-file CSS edits in `overrides.css` must be sequenced even when logically parallel.

## Parallel Examples

- Setup: T002, T003. Foundational: T007, T008 alongside T004–T006.
- US1: T012, T013, T014 together. US2: T018, T021. Polish: T027–T030.

## Implementation Strategy

1. MVP: Phases 1–3, validate Home in es/en.
2. Add US2 (Index/Post), then US3 (Page + parity check).
3. Finish with Phase 6; rollback = revert `overrides.css`, layouts, `card.html`, `messages.yml`, `head/custom.html`.

## Summary

Total 31 tasks: Setup 3, Foundational 8, US1 5, US2 5, US3 3, Polish 7.

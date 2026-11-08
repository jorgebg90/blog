# Research: Modern Card Design

All Technical Context items resolved; no NEEDS CLARIFICATION remain.

## R-001 Where to put the styles
- **Decision**: CSS custom properties and new component rules in `assets/css/overrides.css`; minimal edits in `main.scss` only to neutralize conflicting 006 rules.
- **Rationale**: Already loaded after `main.css` with a cache-buster; avoids Sass recompile coupling and keeps rollback to a revert.
- **Alternatives**: Rewrite `main.scss` (large, risky); new partial dirs (non-standard for this project).

## R-002 Card implementation
- **Decision**: `_includes/card.html` with parameters `eyebrow`, `title`, `description`, `url`, `link_text`, `featured`.
- **Rationale**: One markup source for Home and Index; standard Jekyll include.
- **Alternatives**: Duplicated markup (drift); JS rendering (forbidden by FR-014).

## R-003 Featured card
- **Decision**: First rendered item gets `card--featured` via `forloop.first` (Index: first visible after de-dup, tracked with a flag).
- **Rationale**: Matches spec assumption; de-dup can skip items so `forloop.first` alone is insufficient on Index.

## R-004 Localization of eyebrows/link text
- **Decision**: Add keys to `_data/messages.yml` (`en`/`es`), overridable by front matter (`eyebrow`).
- **Rationale**: File already holds localized UI strings with English keys.
- **Alternatives**: Hardcode per layout (breaks FR-003 localization).

## R-005 Language switcher pill
- **Decision**: CSS-only restyle of `.lang-switch`; markup/data-attributes unchanged; `.is-active` = white pill, blue text; inactive muted. Verify what `language-session.js` reads before touching `aria-current`.
- **Rationale**: FR-008 forbids behavior change.

- **Verified (T002)**: `assets/js/language-session.js` does not read `aria-current` (no match); it only uses data-attributes/hrefs. Switcher markup left untouched.

## R-005b Wordmark
- **Decision**: Restyle `.site-title` (bold, blue, tight tracking) at top-left; switcher right via flex `justify-content: space-between`.

## R-006 Font
- **Decision**: Inter, one stylesheet request with `display=swap` and preconnect; fallback `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`.
- **Rationale**: SC-006 allows one extra font request; no font currently loaded.
- **Alternatives**: Self-host (more files); system only (diverges from reference).

## R-007 Color tokens and contrast
- **Decision**: `--bg #f5f8fd`, `--text #0f1b33`, `--muted #4a5877`, `--accent #1a56db`, `--card #fff`, `--border #dbe4f3`, `--radius 20px`. Dark equivalents under `prefers-color-scheme: dark`.
- **Rationale**: Values from spec assumptions; accent on white ≈ 6.7:1, muted on tint > 4.5:1 (to be verified).
- Border 3:1 for UI borders applies to interactive controls; decorative card borders use the thin light border, while focus rings use accent.

## R-008 Focus and motion
- **Decision**: `:focus-visible` 3px accent outline with offset; transitions wrapped in `prefers-reduced-motion: no-preference`.

## R-009 Footer divider
- **Decision**: `#footer { border-top: 1px solid var(--border) }`; `footer.html` remains empty.

## R-010 Legacy Minimal Mistakes elements
- **Decision**: Harmonize via tokens (links, code, blockquote, table, TOC, pagination); no redesign.

## R-011 Conflicting 006 selectors (T003)
- `.home-hero--emphasized` (background, border-bottom, radius, centered text), `.home-hero__title/__intro/__cta` (centered/justified), `.home-content-section` and `.home-posts-section` white backgrounds, `.home-posts-section .post-list` (now unused on Home), `.section-container` background, `.home-banner` 100vw breakout, `.lang-switch*` in main.scss, `.posts-index__header` and `.posts-index .post-list li` rules in the old `overrides.css`.
- Handled by editing the hero/section rules in `main.scss` (no `!important`) and overriding the rest in `overrides.css` (loaded later; `#main`-scoped where MM's `#main img` rule needed it).

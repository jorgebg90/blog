# Data Model: Modern Card Design

No stored data; these are template-level entities.

## Card (`_includes/card.html` parameters)
| Field | Required | Source | Notes |
|-------|----------|--------|-------|
| eyebrow | no | front matter `eyebrow` or `messages.yml` default | Omitted entirely when blank (no empty space) |
| title | yes | post/page title | Escaped |
| description | no | `excerpt` (truncated 160) or front matter | Muted text |
| url | yes | `post.url` | `relative_url` applied |
| link_text | yes | `messages.yml` `card_read[lang]` | "Leer →" / "Read →" |
| featured | no | first rendered card | Adds `card--featured` (blue border) |

## Eyebrow Label
Localized uppercase text; keys `eyebrow_posts`, `eyebrow_reading` in `_data/messages.yml`, each with `en` and `es`. Uppercasing via CSS `text-transform`.

## Language Switcher Pill
States: active (`.is-active`, `aria-current`), inactive. Existing data-attributes unchanged.

## Page Variant
layout ∈ {home, posts-index, post, page} × lang ∈ {es, en} = 8 validation targets.

## Design Tokens
`--bg`, `--surface`, `--text`, `--muted`, `--accent`, `--border`, `--radius`, `--space-*`, `--font-sans`; dark-mode overrides.

## State
Card: default → featured (first item only). No transitions beyond hover/focus styling.

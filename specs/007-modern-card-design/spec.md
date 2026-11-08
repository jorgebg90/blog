# Feature Specification: Modern Card Design

**Feature Branch**: `007-modern-card-design`  
**Created**: 2026-11-08  
**Status**: Draft  
**Input**: User description: "Restyle the existing bilingual Jekyll blog to match the look of the jblueprint.dev landing page: light blue-tinted background, dark navy text, bold tight-tracked sans-serif headings, small uppercase blue eyebrow labels, rounded white cards with thin borders (featured card with blue border), bold blue wordmark top-left, pill-style language switcher top-right, generous whitespace, mobile-first, thin bottom divider. Apply across home, posts index, post and page layouts for ES and EN, keeping accessibility and multilingual behavior intact."

## Scope Boundaries

### In Scope

- Visual restyle of the Home, Posts Index, Post, and Page layouts in both Spanish (es) and English (en).
- Site-wide header (wordmark + language switcher) and footer (thin divider).
- A reusable card pattern (eyebrow, title, muted description, "text →" link) used for content listings.
- Typography, color, spacing, border, and focus/hover/motion styling.

### Out of Scope

- Any change to URLs, permalinks, language structure, hreflang, or translation-fallback behavior (preserved from specs 001–006).
- New runtime JavaScript frameworks or new plugins.
- Content/copy rewrites beyond adding short eyebrow labels where a card needs one.
- A dark-mode redesign (see Assumptions).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Recognize a modern, consistent brand on Home (Priority: P1)

A visitor opening Home (es or en) sees a light blue-tinted page, a bold blue "jblueprint" wordmark top-left, a pill language switcher top-right, an eyebrow-labeled hero, and a stack/grid of rounded white cards where the first (featured) card has a blue border.

**Why this priority**: Home is the first impression and the reference for the whole visual system.

**Independent Test**: Load Home in es and en at 375px and 1280px widths and compare to the reference screenshot.

**Acceptance Scenarios**:

1. **Given** Home in either language, **When** it loads, **Then** the background is a light blue tint, text is dark navy, and headings are bold with tight letter-spacing.
2. **Given** the Home card list, **When** viewed, **Then** each card is white, ~20px rounded, has a thin light border, shows eyebrow + title + muted description + bold blue "text →" link, and the first card has a blue border.
3. **Given** the header, **When** viewed, **Then** the wordmark is bold blue at top-left and the switcher is top-right with the active language as a white rounded pill with blue text and the inactive one in muted text.

---

### User Story 2 - Browse and read posts in the same style (Priority: P2)

A visitor opens the Posts Index and a single Post; the index shows posts as cards, and the post page uses the same palette, heading style, eyebrow (e.g., "LECTURA"/"READING"), and generous whitespace with a readable line length.

**Why this priority**: These are the core reading journeys after Home.

**Independent Test**: Open the posts index and one post per language; verify card styling, post heading/eyebrow, and readable body text.

**Acceptance Scenarios**:

1. **Given** the Posts Index, **When** viewed, **Then** posts appear as cards matching Story 1, with the newest first card featured.
2. **Given** a Post, **When** viewed, **Then** it shows an eyebrow, bold tight-tracked title, dark navy body text, styled code/quotes/images that do not overflow on mobile.
3. **Given** a post without a translation, **When** viewed, **Then** existing fallback/translation-notice behavior still works and is styled consistently.

---

### User Story 3 - Page layouts and language switching stay coherent (Priority: P3)

A visitor opens a generic Page (e.g., About) and switches language via the pill switcher; the page shares the same system and the switch lands on the equivalent page as before.

**Why this priority**: Completes coverage and guards against multilingual regressions.

**Independent Test**: Open About in es, switch to en and back; confirm destination URLs match pre-change behavior.

**Acceptance Scenarios**:

1. **Given** a Page in es, **When** the visitor uses the switcher, **Then** they reach the same destination as before this feature.
2. **Given** any page, **When** scrolled to the bottom, **Then** a thin divider and footer are shown in the new style.

---

### Edge Cases

- Very long titles/descriptions wrap without breaking card layout; cards of unequal length align cleanly.
- A list with a single card or no posts still renders gracefully.
- Cards without an eyebrow omit the label without leaving empty space.
- Browser zoom at 200% and 320px viewports show no horizontal scroll.
- Users with reduced-motion preference see no hover/transition animation.
- Content in Minimal Mistakes elements not restyled (tables, TOC, pagination, search) remains legible and not visually broken.
- Fonts failing to load fall back to a system sans-serif with no layout break.

## Requirements *(mandatory)*

### Constitution Alignment *(mandatory)*

- **CA-001**: Implementation notes, config keys, and code comments in scope MUST be in English.
- **CA-002**: Layout/include/config changes MUST follow official Jekyll conventions (layouts, includes, front matter, `assets/`) and the Minimal Mistakes remote-theme override mechanism.
- **CA-003**: No non-standard Jekyll structure or plugins are introduced; rollback is reverting the style overrides and layout/include edits.

### Functional Requirements

- **FR-001**: The site MUST use a light blue-tinted page background (~#f5f8fd) and dark navy primary text across Home, Posts Index, Post, and Page in es and en.
- **FR-002**: Headings MUST be bold sans-serif (Roboto/Inter-like) with tight letter-spacing.
- **FR-003**: The system MUST provide small uppercase, letter-spaced blue eyebrow labels (e.g., "WEBS Y PROYECTOS", "LECTURA") above hero titles, card titles, and post titles, localized per language.
- **FR-004**: Content cards MUST be white, ~20px rounded, with a thin light border; the first/featured card MUST have a blue border.
- **FR-005**: Each card MUST present eyebrow, title, muted description, and a bold blue "text →" link whose text is localized.
- **FR-006**: The header MUST show a bold blue "jblueprint" wordmark at top-left linking to the current language's home.
- **FR-007**: The language switcher MUST be at top-right as a pill control: active = white rounded pill with blue text; inactive = muted text; the active language MUST be programmatically indicated (e.g., `aria-current`).
- **FR-008**: Existing multilingual behavior (URLs, hreflang, switcher targets, translation fallback and notices) MUST remain unchanged.
- **FR-009**: Layouts MUST be mobile-first with generous whitespace and no horizontal scroll from 320px upward.
- **FR-010**: A thin divider MUST appear at the bottom of the page above/within the footer.
- **FR-011**: Text and interactive elements MUST meet WCAG AA contrast (4.5:1 body, 3:1 large text/UI borders); blue used for text MUST satisfy this on white and on the tinted background.
- **FR-012**: All interactive elements MUST show a clearly visible keyboard focus indicator.
- **FR-013**: Hover/transition effects MUST be subtle and disabled under the reduced-motion preference.
- **FR-014**: The feature MUST NOT add new runtime JavaScript frameworks or plugins; styling is delivered via existing override stylesheet, layouts, and includes.
- **FR-015**: Prior conventions from spec 006 (English-only code comments, preserved URLs, SEO/performance baseline, no scripting-layer changes, external web-font compatibility) MUST NOT regress.
- **FR-016**: Web fonts, if used, MUST load with a fallback and not block rendering.

### Key Entities

- **Card**: A bounded content block with optional eyebrow, title, description, link text, and a featured/default state.
- **Eyebrow Label**: Short localized uppercase category text shown above a title.
- **Language Switcher Pill**: Control listing available languages with active/inactive states.
- **Page Variant**: Layout × language combination (Home/Index/Post/Page × es/en) used for validation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the 8 page variants (4 layouts × 2 languages) show the new palette, typography, header, and footer divider when compared to the reference.
- **SC-002**: 100% of text and UI elements on those variants pass WCAG AA contrast checks.
- **SC-003**: Every interactive element is reachable and visibly focused via keyboard alone.
- **SC-004**: No horizontal scrolling at 320px, 375px, 768px, and 1280px widths on any variant.
- **SC-005**: Language switching and translation fallback lead to the same destinations as before the change in 100% of tested pages.
- **SC-006**: Existing SEO metadata is unchanged, and page load experience is not perceptibly slower (no more than one additional font request).
- **SC-007**: With reduced-motion enabled, no animated transitions are observed.

## Assumptions

- The reference is the user's jblueprint.dev screenshot; it is a directional benchmark, not pixel-exact replication.
- Exact values: background ~#f5f8fd, card radius ~20px, a blue accent around #1a56db-range (adjusted as needed for AA contrast), navy text ~#0f1b33.
- The existing light/dark behavior from spec 006 is retained for dark mode with the new card structure adapted to dark equivalents; light is the primary designed mode.
- The first card in a listing is the "featured" card.
- Eyebrow labels come from front matter/localized site data when present, otherwise from per-layout defaults (e.g., "LECTURA"/"READING" for posts).
- Inter (or Roboto) may be loaded from the existing web-font pattern, with a system sans-serif fallback.
- The "text →" link text is localized (e.g., "Leer →"/"Read →").
- Minimal Mistakes elements without a design in the reference keep theme defaults, harmonized by palette.

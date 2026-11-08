# jblueprint.dev
Jorge Personal Blog for Software Architecture topics

## Contribution Rules

Project governance is defined in `.specify/memory/constitution.md`.

- Keep code, configuration keys, and code comments in English.
- Follow official Jekyll conventions and documentation for structural/config changes.
- Run `bundle exec jekyll build` for site-affecting changes before finalizing.

## Bilingual Content Workflow (en/es)

This site uses a language-first content layout with canonical routes for `en` and `es`.

Source structure:

- `site/en/` for English pages and `site/en/_posts/` for English posts
- `site/es/` for Spanish pages and `site/es/_posts/` for Spanish posts

For every bilingual page or post variant, include at least:

- `lang`: `en` or `es`
- `translation_key`: shared key across locale variants of the same logical document

Authoring checklist:

1. Add/update English variant (`lang: en`) under `site/en/` with canonical unprefixed route.
2. Add/update Spanish variant (`lang: es`) under `site/es/` using the same `translation_key`.
3. Keep permalinks aligned for equivalent pages when route parity is required.
4. Run `bundle exec jekyll build` and verify outputs under `_site/` and `_site/es/`.
5. Run `python3 scripts/validate_local_routes.py --site-dir _site`.
6. Verify alternate metadata (`hreflang`, `x-default`) for bilingual pages.

Related docs:

- `docs/multilingual-content-workflow.md`
- `docs/multilingual-redirects.md`
- `docs/multilingual-rollback.md`

## Production navigation validation

After deploying with your existing pipeline, run a live navigation check against production:

```zsh
python3 scripts/validate_production_navigation.py --base-url "https://jblueprint.dev/blog/"
python3 scripts/validate_production_navigation.py --base-url "https://www.jblueprint.dev/blog/"
```

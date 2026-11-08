# Production Navigation Validation

Use this checker to validate bilingual navigation directly against the live site.

Before running production checks, validate local build output first:

```zsh
python3 scripts/validate_local_routes.py --site-dir _site
```

## What it checks

- Critical EN and ES routes return HTTP 200.
- Pages are not serving the 404 template by mistake.
- Language switcher markup exists on each route.
- `data-current-lang` matches the expected locale.
- `data-target-en` and `data-target-es` are present and do not point to `/404.html`.
- Switcher targets themselves return HTTP 200.

## Run

```zsh
python3 scripts/validate_production_navigation.py
```

To validate a different domain:

```zsh
python3 scripts/validate_production_navigation.py --base-url "https://www.jblueprint.dev/blog/"
```

Include the deployed subpath in `--base-url` when the site is hosted below a domain root.

The command exits with code `1` when any validation fails.

## Canonical validation scope

- `/`, `/about/`, `/posts/`
- `/es/`, `/es/about/`, `/es/posts/`
- `/jekyll/speckit/2026/05/08/how-to-build-a-blog-with-spec-driven-design.html`
- `/es/jekyll/speckit/2026/05/08/como-crear-un-blog-con-spec-driven-design.html`
- `/jekyll/theme/2026/05/08/installing-minimal-mistakes-on-a-bilingual-jekyll-blog.html`
- `/es/jekyll/theme/2026/05/08/instalacion-minimal-mistakes.html`

# Contributing

Thanks for helping keep the AW Business Service site tidy.

## Editing rules

- Work inside the existing route structure.
- Keep English and Thai pages aligned when changing shared content.
- Do not change navbar markup unless the task explicitly calls for it.
- Prefer shared CSS and JS updates over repeating one-off styles on individual pages.
- Keep SEO copy professional and case-by-case.

## Before you push

- Run `python3 tests/check_site.py`
- Check that new content does not break existing routes or redirects
- Avoid moving files unless the deploy plan includes the URL impact

## Helpful files

- `README.md` - overview of the repository
- `docs/repo-structure.md` - route map and ownership notes
- `assets/css/styles.css` - shared styling
- `assets/js/site.js` - shared interactions

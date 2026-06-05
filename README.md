# AW Business Service Website

Static website for AW Business Service Pattaya.

## What lives where

- `index.html` - English home page
- `th/` - Thai site mirror
- `about/`, `contact/`, `faq/`, `services/`, `news/` - main content routes
- `visa-services/`, `work-permit/`, `business-services/`, `personal-services/`, `legal-consultant/` - service hubs and detail pages
- `assets/` - shared images, CSS, and JavaScript
- `docs/` - internal notes, plans, and site structure references
- `tests/` - static site checks
- `scripts/` - helper scripts for site generation and maintenance

## Local workflow

1. Edit the existing page tree in place.
2. Keep public URLs stable unless a redirect is added.
3. Run the site check before pushing:
   ```bash
   python3 tests/check_site.py
   ```
4. Commit to GitHub and let Netlify deploy from the connected branch.

## Notes

- The site is intentionally route-based, so folder names are part of the public URL structure.
- Avoid renaming live folders or files without planning redirects first.
- Shared styling and behavior live in `assets/css/styles.css` and `assets/js/site.js`.

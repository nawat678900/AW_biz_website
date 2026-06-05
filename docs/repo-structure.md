# Repository Structure

This site keeps the public URL structure stable and organizes work by page group.

## Top level

- `index.html` - home page
- `th/` - Thai mirror of the site
- `about/` - About Us pages
- `contact/` - Contact pages
- `faq/` - FAQ pages
- `services/` - service overview pages and legacy support pages
- `visa-services/` - visa service hub and detail pages
- `work-permit/` - work permit hub and detail pages
- `business-services/` - business service hub and detail pages
- `personal-services/` - personal service hub and detail pages
- `legal-consultant/` - legal service hub and detail pages
- `news/` - article and recommendation pages
- `assets/` - shared CSS, JS, and images
- `tests/` - static validation
- `scripts/` - utility scripts

## Shared responsibilities

- `assets/css/styles.css` handles the global design system.
- `assets/js/site.js` handles shared behavior like icons, menus, language switching, and pagination.
- `sitemap.xml`, `robots.txt`, and `_redirects` support SEO and routing.

## Editing rule of thumb

Keep changes close to the page group that owns them. If a change affects multiple routes, update the shared asset or shared template pattern instead of patching each page separately.

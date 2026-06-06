#!/usr/bin/env python3
"""Static checks for the AW Business Service Pattaya website."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ROUTES = {
    "Home": "index.html",
    "Services": "services/index.html",
    "Article": "news/index.html",
    "Trusted Local Support for Thai and Foreign Clients": "news/local-team-pattaya/index.html",
    "Visa Checklist for Foreigners": "news/visa-service-checklist-pattaya/index.html",
    "Business Registration and Accounting Basics": "news/business-accounting-guidance-pattaya/index.html",
    "Work Permit Renewal Guide": "news/work-permit-renewal-guide/index.html",
    "Tax Filing and VAT Basics": "news/tax-filing-vat-basics/index.html",
    "90-Day Report Document Guide": "news/ninety-day-report-document-guide/index.html",
    "Driving License Support Guide": "news/driving-license-support-guide/index.html",
    "Marriage Visa Documents": "news/marriage-visa-documents/index.html",
    "Retirement Visa Requirements": "news/retirement-visa-requirements/index.html",
    "Legal Consultation for Business Support": "news/legal-consultation-business-support/index.html",
    "About Us": "about/index.html",
    "FAQ": "faq/index.html",
    "Contact": "contact/index.html",
    "Legal Consultant": "legal-consultant/index.html",
    "Legal Consultation": "legal-consultant/legal-consultation/index.html",
    "Contract Review": "legal-consultant/contract-review/index.html",
    "Document Support": "legal-consultant/document-support/index.html",
    "Translation Support": "legal-consultant/translation-support/index.html",
    "Privacy Policy": "privacy-policy/index.html",
    "Terms": "terms/index.html",
    "PDPA Notice": "pdpa-notice/index.html",
    "Visa Services": "visa-services/index.html",
    "Business Visa Pattaya": "visa-services/business-visa-pattaya/index.html",
    "Retirement Visa Pattaya": "visa-services/retirement-visa-pattaya/index.html",
    "Marriage Visa Pattaya": "visa-services/marriage-visa-pattaya/index.html",
    "Child Support Visa": "visa-services/child-support-visa/index.html",
    "Neighboring Country Visa": "visa-services/neighboring-country-visa/index.html",
    "Visa Document Preparation": "visa-services/visa-document-preparation/index.html",
    "BOI Visa Support": "visa-services/boi-visa-support/index.html",
    "Schengen Visa Support": "visa-services/schengen-visa-support/index.html",
    "Work Permit": "work-permit/index.html",
    "Work Permit Application Pattaya": "work-permit/application-pattaya/index.html",
    "Work Permit Renewal Pattaya": "work-permit/renewal-pattaya/index.html",
    "Work Permit Employee Support": "work-permit/employee-support/index.html",
    "Work Permit Employer Support": "work-permit/employer-support/index.html",
    "Business Services": "business-services/index.html",
    "Company Registration Pattaya": "business-services/company-registration-pattaya/index.html",
    "Director Shareholder Change": "business-services/director-shareholder-change/index.html",
    "Accounting Services Pattaya": "business-services/accounting-services-pattaya/index.html",
    "Social Security": "business-services/social-security/index.html",
    "VAT Registration Pattaya": "business-services/vat-registration-pattaya/index.html",
    "Tax Filing Pattaya": "business-services/tax-filing-pattaya/index.html",
    "Financial Statement Closing": "business-services/financial-statement-closing/index.html",
    "Accounting Tax Consultation": "business-services/accounting-tax-consultation/index.html",
    "Business License Support": "business-services/business-license-support/index.html",
    "Personal Services": "personal-services/index.html",
    "Driving License Pattaya": "personal-services/driving-license-pattaya/index.html",
    "Residence Report": "personal-services/residence-report/index.html",
    "90-Day Report Pattaya": "personal-services/90-day-report-pattaya/index.html",
    "Visa Cancellation": "personal-services/visa-cancellation/index.html",
    "Work Permit Cancellation": "personal-services/work-permit-cancellation/index.html",
}

LOCAL_ASSETS = [
    "assets/css/styles.css",
    "assets/js/site.js",
    "assets/images/aw-business-logo.png",
    "assets/images/pattaya-coastline.jpg",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel_to_root(route: str) -> str:
    depth = len(Path(route).parent.parts)
    return "../" * depth


def assert_true(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def check_font_system(pages: dict[str, str], failures: list[str]) -> None:
    styles = read_text(ROOT / "assets/css/styles.css")
    font_href = "https://fonts.googleapis.com/css2?family=Kanit:wght@400;500;600;700;800;900&family=Prompt:wght@400;500;600;700;800;900&display=swap"

    for route, html in pages.items():
        assert_true(
            'https://fonts.googleapis.com' in html and font_href in html,
            f"{route} does not load the requested Google Fonts",
            failures,
        )

    for token in [
        '--font-heading: "Prompt", sans-serif;',
        '--font-logo-main: "Kanit", sans-serif;',
        '--font-logo-sub: "Prompt", sans-serif;',
        'font-family: var(--font-heading)',
    ]:
        assert_true(token in styles, f"Stylesheet missing requested font token: {token}", failures)

    assert_true(
        '.footer-brand' in styles and 'var(--font-logo-main)' in styles,
        "Brand text does not use the requested logo font",
        failures,
    )



def check_routes(failures: list[str]) -> dict[str, str]:
    pages: dict[str, str] = {}
    for title, route in ROUTES.items():
        path = ROOT / route
        assert_true(path.exists(), f"Missing route for {title}: {route}", failures)
        if path.exists():
            pages[route] = read_text(path)
    return pages


def check_assets(failures: list[str]) -> None:
    for asset in LOCAL_ASSETS:
        assert_true((ROOT / asset).exists(), f"Missing local asset: {asset}", failures)


def check_shared_markup(pages: dict[str, str], failures: list[str]) -> None:
    for route, html in pages.items():
        prefix = rel_to_root(route)
        assert_true(
            f'href="{prefix}assets/css/styles.css"' in html,
            f"{route} does not use the shared stylesheet",
            failures,
        )
        assert_true(
            f'src="{prefix}assets/js/site.js"' in html,
            f"{route} does not use the shared site script",
            failures,
        )
        assert_true(
            "cdn.tailwindcss.com" not in html,
            f"{route} still depends on the Tailwind CDN",
            failures,
        )
        assert_true(
            'href="#"' not in html and "href='#'" not in html,
            f"{route} still contains a dead href",
            failures,
        )
        assert_true(
            'action="#"' not in html and "action='#'" not in html,
            f"{route} still contains a placeholder form action",
            failures,
        )


def check_navigation(pages: dict[str, str], failures: list[str]) -> None:
    all_nav_targets = [
        "services/",
        "news/",
        "about/",
        "faq/",
        "contact/",
    ]

    required_top_level = [
        "Home",
        "Services",
        "Article",
        "Company",
        "Contact",
    ]

    for route, html in pages.items():
        header_start = html.find('<header class="site-header">')
        header_end = html.find("</header>", header_start)
        header = html[header_start:header_end] if header_start != -1 and header_end != -1 else html

        assert_true(
            'class="nav-line-link"' not in header or "line-logo.png" in header,
            f"{route} header LINE icon must use the shared LINE image asset",
            failures,
        )
        assert_true(
            'class="nav-line-link"' not in header or 'class="brand-icon"' not in header.split('class="nav-line-link"', 1)[1].split("</a>", 1)[0],
            f"{route} header LINE icon still uses the temporary vector mark",
            failures,
        )
        assert_true(
            "nav-dropdown-toggle" in header and "mobile-nav-group" in header,
            f"{route} does not expose sitemap pages through navbar dropdowns",
            failures,
        )
        assert_true(
            'aria-current="page"' in header,
            f"{route} does not mark the active navigation item",
            failures,
        )
        assert_true(
            'aria-label="Toggle navigation menu"' in header,
            f"{route} is missing an accessible mobile menu button",
            failures,
        )
        for label in required_top_level:
            assert_true(
                label in header,
                f"{route} navbar missing top-level item: {label}",
                failures,
            )
        for legacy_label in ["Process", "Reviews"]:
            assert_true(
                f">{legacy_label}<" not in header,
                f"{route} navbar still includes removed item: {legacy_label}",
                failures,
            )
        for legacy_legal_label in ["Privacy Policy", "Terms", "PDPA Notice"]:
            assert_true(
                f">{legacy_legal_label}<" not in header,
                f"{route} navbar still includes policy item in legal menu: {legacy_legal_label}",
                failures,
            )
        for target in all_nav_targets:
            assert_true(
                target in header,
                f"{route} navbar missing sitemap target: {target}",
                failures,
            )


def check_contact_flow(pages: dict[str, str], failures: list[str]) -> None:
    line_url = "https://line.me/R/ti/p/@awbizpattaya"
    all_html = "\n".join(pages.values())
    assert_true(line_url in all_html, "LINE contact URL is missing", failures)
    assert_true("@awbizpattaya" in all_html, "LINE handle is missing", failures)
    assert_true("tel:+66851247315" in all_html, "Phone CTA is missing", failures)

    contact = pages.get("contact/index.html", "")
    for field in ["name", "contact", "service", "message"]:
        assert_true(
            f'name="{field}"' in contact and "required" in contact,
            f"Contact form field is not present and required: {field}",
            failures,
        )
    assert_true(
        'data-contact-form' in contact,
        "Contact form is not wired for static client-side handling",
        failures,
    )
    assert_true(
        "No network request is sent" in contact,
        "Contact page does not explain static form behavior",
        failures,
    )
    map_embed = "https://www.google.com/maps?q=AW%20Business%20Services%20Pattaya&output=embed"
    map_search = "https://www.google.com/maps/search/?api=1&query=399%2F19%20Pornprapanimit%20Rd%2C%20Muang%20Pattaya%2C%20Bang%20Lamung%20District%2C%20Chon%20Buri%2020150%2C%20Thailand"
    assert_true(
        '<iframe' in contact and map_embed in contact,
        "Contact page is missing the requested embedded Google Map source",
        failures,
    )
    assert_true(
        f'href="{map_search}"' in contact,
        "Contact page Google Maps link does not use the precise address pin",
        failures,
    )
    assert_true(
        "Pornprapanimit Rd" in contact,
        "Contact page is missing the full office road address",
        failures,
    )
    assert_true(
        'title="AW Business Service Pattaya location"' in contact,
        "Contact Google Map iframe needs an accessible title",
        failures,
    )


def check_contact_widget(pages: dict[str, str], failures: list[str]) -> None:
    widget_links = [
        'href="tel:+66851247315"',
        'href="https://www.facebook.com/profile.php?id=61570829170335"',
        'href="https://line.me/R/ti/p/@awbizpattaya"',
        'href="mailto:info@awbizpattaya.com"',
        'href="#contact"',
    ]

    for route, html in pages.items():
        assert_true(
            'id="contact"' in html,
            f"{route} is missing a #contact target for the floating widget",
            failures,
        )
        assert_true(
            html.count('id="contact"') == 1,
            f"{route} must have exactly one #contact target",
            failures,
        )
        assert_true(
            'class="contact-widget"' in html,
            f"{route} is missing the floating contact widget",
            failures,
        )
        assert_true(
            'id="contactToggle"' in html,
            f"{route} is missing the contact widget toggle",
            failures,
        )
        assert_true(
            'class="floating-line"' not in html,
            f"{route} still uses the old floating LINE button",
            failures,
        )
        assert_true(
            '>LINE</a>' not in html,
            f"{route} floating contact widget still uses the old LINE text button",
            failures,
        )
        assert_true(
            'class="brand-image"' in html and 'line-logo.png' in html,
            f"{route} floating contact widget must use the provided LINE image asset",
            failures,
        )
        assert_true(
            'class="contact-option line"' not in html or 'class="brand-icon"' not in html.split('class="contact-option line"', 1)[1].split('</a>', 1)[0],
            f"{route} floating contact widget still uses the temporary LINE vector icon",
            failures,
        )
        for link in widget_links:
            assert_true(
                link in html,
                f"{route} floating contact widget missing {link}",
                failures,
            )


def check_local_links(pages: dict[str, str], failures: list[str]) -> None:
    href_pattern = re.compile(r'href="([^"]+)"')
    for route, html in pages.items():
        current_dir = (ROOT / route).parent
        for href in href_pattern.findall(html):
            if href.startswith(("http://", "https://", "tel:", "mailto:", "#")):
                continue
            target = (current_dir / href.split("#", 1)[0]).resolve()
            assert_true(
                target.exists(),
                f"{route} links to missing local target: {href}",
                failures,
            )


def check_local_images(pages: dict[str, str], failures: list[str]) -> None:
    src_pattern = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"', re.IGNORECASE)
    for route, html in pages.items():
        current_dir = (ROOT / route).parent
        for src in src_pattern.findall(html):
            if src.startswith(("http://", "https://", "data:")):
                continue
            target = (current_dir / src).resolve()
            assert_true(
                target.exists(),
                f"{route} references missing local image: {src}",
                failures,
            )


def check_icon_mappings(pages: dict[str, str], failures: list[str]) -> None:
    script = read_text(ROOT / "assets/js/site.js")
    icon_pattern = re.compile(
        r'<span class="icon-box(?: [^"]+)?">([A-Z0-9]{2})</span>'
    )
    icon_codes = sorted({code for html in pages.values() for code in icon_pattern.findall(html)})

    assert_true(
        "setupIconSystem" in script and 'data-lucide' in script,
        "Site script does not define the Lucide icon system",
        failures,
    )
    for code in icon_codes:
        assert_true(
            f'"{code}":' in script,
            f"Icon code {code} is not mapped to an SVG icon",
            failures,
        )
    assert_true(
        "window.lucide.createIcons()" in script,
        "Site script does not initialize Lucide icon rendering from the CDN",
        failures,
    )

    for route, html in pages.items():
        if 'assets/js/site.js' in html:
            assert_true(
                'https://unpkg.com/lucide@latest' in html,
                f"{route} does not load the Lucide CDN",
                failures,
            )



def check_hero_layout(pages: dict[str, str], failures: list[str]) -> None:
    home = pages.get("index.html", "")
    styles = read_text(ROOT / "assets/css/styles.css")

    assert_true(
        'class="aw-hero"' in home and 'id="home"' in home,
        "Home hero does not use the AW hero section",
        failures,
    )
    assert_true(
        'class="aw-hero-image"' in home
        and (
            'assets/images/Herosection5.png' in home
            or 'assets/images/Hero_section_background.png' in home
            or 'assets/images/Herosection_cover.png' in home
        ),
        "Home hero is missing the full-section team image",
        failures,
    )
    assert_true(
        'class="aw-hero-photo-space"' in home,
        "Home hero is missing the left-side photo spacing column",
        failures,
    )
    assert_true(
        "Professional Visa," in home and "Work Permit &amp;" in home and "Business Support" in home,
        "Home hero headline does not match the requested layout",
        failures,
    )
    assert_true(
        'class="aw-hero-trust"' in home,
        "Home hero is missing trust points",
        failures,
    )
    for token in [
        ".aw-hero {",
        ".aw-hero-container",
        ".aw-hero-image img",
        ".aw-hero-photo-space",
        ".aw-hero-content h1",
        ".aw-hero-trust",
    ]:
        assert_true(token in styles, f"Stylesheet missing requested hero CSS: {token}", failures)

def check_review_pagination(pages: dict[str, str], failures: list[str]) -> None:
    home = pages.get("index.html", "")
    script = read_text(ROOT / "assets/js/site.js")
    styles = read_text(ROOT / "assets/css/styles.css")

    assert_true(
        'data-review-pagination' in home,
        "Home reviews section is missing pagination wrapper",
        failures,
    )
    assert_true(
        'data-review-card' in home and home.count('data-review-card') >= 6,
        "Home reviews section must include at least 6 paginated review cards",
        failures,
    )
    for marker in [
        'data-review-prev',
        'data-review-next',
    ]:
        assert_true(marker in home, f"Home reviews pagination missing {marker}", failures)
    assert_true(
        'data-review-pages' not in home and 'data-review-status' not in home,
        "Home reviews pagination should use only left and right controls",
        failures,
    )

    assert_true(
        "setupReviewPagination" in script
        and 'listSelector: "[data-review-list]"' in script
        and "carousel-group" in script
        and "is-infinite" in script,
        "Site script does not initialize infinite customer review carousel",
        failures,
    )
    assert_true(
        "carouselInfinite" in styles and ".carousel-track.is-infinite" in styles,
        "Stylesheet is missing infinite carousel animation styles",
        failures,
    )


def check_customer_photo_pagination(pages: dict[str, str], failures: list[str]) -> None:
    home = pages.get("index.html", "")
    script = read_text(ROOT / "assets/js/site.js")
    styles = read_text(ROOT / "assets/css/styles.css")

    assert_true(
        'id="customer-photos"' in home,
        "Home page is missing the customer photo section below reviews",
        failures,
    )
    assert_true(
        'data-photo-pagination' in home,
        "Customer photo section is missing pagination wrapper",
        failures,
    )
    assert_true(
        home.count('data-photo-card') >= 6,
        "Customer photo section must include at least 6 paginated photo cards",
        failures,
    )
    for marker in [
        'data-photo-prev',
        'data-photo-next',
    ]:
        assert_true(marker in home, f"Customer photo pagination missing {marker}", failures)
    assert_true(
        'data-photo-pages' not in home and 'data-photo-status' not in home,
        "Customer photo pagination should use only left and right controls",
        failures,
    )
    assert_true(
        '<figcaption>' not in home[home.find('id="customer-photos"'):home.find('id="faq-preview"')],
        "Customer photo cards should display photos only",
        failures,
    )

    assert_true(
        "customer-photo-card" in styles and "customer-photo-card img" in styles,
        "Customer photo cards are missing dedicated image styles",
        failures,
    )
    assert_true(
        "data-photo-pagination" in script
        and 'listSelector: "[data-photo-list]"' in script
        and "carousel-group" in script
        and "is-infinite" in script,
        "Site script does not initialize infinite customer photo carousel",
        failures,
    )


def check_landing_page_revision(pages: dict[str, str], failures: list[str]) -> None:
    home = pages.get("index.html", "")
    styles = read_text(ROOT / "assets/css/styles.css")
    map_embed = "https://www.google.com/maps?q=AW%20Business%20Services%20Pattaya&output=embed"
    map_search = "https://www.google.com/maps/search/?api=1&query=399%2F19%20Pornprapanimit%20Rd%2C%20Muang%20Pattaya%2C%20Bang%20Lamung%20District%2C%20Chon%20Buri%2020150%2C%20Thailand"

    assert_true(
        'id="location"' in home and 'class="section section-soft landing-map-section"' in home,
        "Landing page is missing the dedicated location map section",
        failures,
    )
    assert_true(
        map_embed in home and f'href="{map_search}"' in home,
        "Landing page map section does not use the requested Google Maps embed source",
        failures,
    )
    assert_true(
        "Pornprapanimit Rd" in home,
        "Landing page map section is missing the full office address",
        failures,
    )
    for token in [
        ".landing-map-section",
        ".landing-map-layout",
        ".landing-map-copy",
        ".landing-map-panel",
    ]:
        assert_true(token in styles, f"Stylesheet missing landing map styling: {token}", failures)

    assert_true(
        "padding: 40 px" not in styles and "transform: translate(200px" not in styles,
        "Hero CSS still contains rough spacing overrides",
        failures,
    )


def check_seo_sitemap_pages(pages: dict[str, str], failures: list[str]) -> None:
    sitemap = ROOT / "sitemap.xml"
    assert_true(sitemap.exists(), "Missing sitemap.xml", failures)
    sitemap_text = read_text(sitemap) if sitemap.exists() else ""

    for route, html in pages.items():
        assert_true("<title>" in html and "</title>" in html, f"{route} missing SEO title", failures)
        assert_true('name="description"' in html, f"{route} missing SEO meta description", failures)
        assert_true("<h1" in html, f"{route} missing H1", failures)
        public_path = "/" if route == "index.html" else "/" + route[:-len("index.html")].rstrip("/")
        if sitemap_text:
            assert_true(public_path in sitemap_text, f"sitemap.xml missing {public_path}", failures)



def main() -> int:
    failures: list[str] = []
    pages = check_routes(failures)
    check_assets(failures)
    check_shared_markup(pages, failures)
    check_font_system(pages, failures)
    check_navigation(pages, failures)
    check_contact_flow(pages, failures)
    check_contact_widget(pages, failures)
    check_local_links(pages, failures)
    check_local_images(pages, failures)
    check_icon_mappings(pages, failures)
    check_hero_layout(pages, failures)
    check_review_pagination(pages, failures)
    check_customer_photo_pagination(pages, failures)
    check_landing_page_revision(pages, failures)
    check_seo_sitemap_pages(pages, failures)

    if failures:
        print("Static site checks failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Static site checks passed for {len(ROUTES)} routes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

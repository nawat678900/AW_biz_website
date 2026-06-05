# About Us Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a balanced About Us landing page for AW Business Service Pattaya that tells the company story, highlights 10+ years of professional management, and converts visitors into service inquiries with strong SEO signals.

**Architecture:** Add a new static `/about/` landing page that reuses the existing AW visual system, especially the stitched page-hero pattern, rounded content cards, and service CTA blocks. Wire the page into the shared header and footer so it is reachable from the Company menu and from all site-wide navigation surfaces. Keep the page content natural and local-focused, with keywords like visa services Pattaya, work permit Pattaya, business registration Pattaya, accounting services Pattaya, and document support Pattaya.

**Tech Stack:** Static HTML, shared CSS in `assets/css/styles.css`, shared client behavior in `assets/js/site.js`, site coverage checks in `tests/check_site.py`.

---

### Task 1: Create the About Us landing page

**Files:**
- Create: `about/index.html`
- Modify: `assets/css/styles.css:1768-1847`

- [ ] **Step 1: Write the page markup**

Create a new static landing page at `about/index.html` with the same document head pattern used by the other service pages, including title, meta description, keywords, canonical URL, fonts, stylesheet, and shared script.

Use this structure:

```html
<main id="main">
  <section class="page-hero stitched-hero">
    <div class="container stitched-hero-grid">
      <div class="page-copy">
        <span class="eyebrow">About AW Business Service</span>
        <h1>About AW Business Service Pattaya</h1>
        <p class="lead">Professional management and friendly local support for Thai and foreign clients in Pattaya.</p>
        <div class="inline-actions">
          <a class="button" href="https://line.me/R/ti/p/@awbizpattaya">Contact via LINE</a>
          <a class="button-secondary" href="../visa-services/">View Services</a>
        </div>
      </div>
      <div class="stitched-hero-visual">
        <img src="../assets/images/aw-office-team.jpg" alt="AW Business Service Pattaya office team">
        <div class="stitched-hero-card">
          <span class="eyebrow">10+ years of service</span>
          <h2>Trusted local support in Pattaya</h2>
          <ul class="check-list light-list">
            <li>Thai and English support</li>
            <li>Local Pattaya office</li>
            <li>Professional management</li>
            <li>One-stop document support</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section section-white">
    <div class="container">
      <div class="stitched-detail-grid">
        <div class="split-copy">
          <h2>Our story</h2>
          <p class="lead">AW Business Service Pattaya has supported Thai and foreign clients for more than 10 years with practical, organized service.</p>
          <p>We help with visa services Pattaya, work permit Pattaya, business registration Pattaya, accounting services Pattaya, tax filing, VAT registration, and personal document support with a professional and local-first approach.</p>
          <ul class="check-list">
            <li>Local experience in Pattaya</li>
            <li>Clear communication and follow-up</li>
            <li>Practical support for real documents</li>
            <li>Friendly help for Thai and foreign clients</li>
          </ul>
        </div>
        <div class="detail-note-card">
          <h3>Why clients choose us</h3>
          <p>We keep the process simple, consistent, and easy to understand so clients can move from document review to action with less confusion.</p>
          <h3>What we focus on</h3>
          <p>Visa support, work permits, company services, accounting, tax, and personal document services delivered by a local Pattaya team.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section-soft">
    <div class="container">
      <div class="section-heading left">
        <span class="eyebrow">Services</span>
        <h2>Explore the main service groups</h2>
      </div>
      <div class="stitched-bento-grid">
        <a class="stitched-bento-card stitched-service-card tall" href="../visa-services/">
          <span class="icon-box">VI</span>
          <h3>Visa Services</h3>
          <p>Visa services Pattaya for business, retirement, marriage, and document preparation.</p>
        </a>
        <a class="stitched-bento-card stitched-service-card tall" href="../work-permit/">
          <span class="icon-box">WP</span>
          <h3>Work Permit</h3>
          <p>Work permit Pattaya support for applications, renewals, employees, and employers.</p>
        </a>
        <a class="stitched-bento-card stitched-service-card tall" href="../business-services/">
          <span class="icon-box">BH</span>
          <h3>Business Services</h3>
          <p>Business registration Pattaya, accounting services, tax, VAT, and filing support.</p>
        </a>
        <a class="stitched-bento-card stitched-service-card tall" href="../personal-services/">
          <span class="icon-box">DC</span>
          <h3>Personal Services</h3>
          <p>Document support Pattaya for driving license, residence report, and visa cancellation.</p>
        </a>
      </div>
    </div>
  </section>

  <section class="section section-white">
    <div class="container">
      <div class="cta-panel">
        <h2>Talk to our Pattaya team</h2>
        <p class="lead">Send your case on LINE and we will help you choose the right next step.</p>
        <div class="cta-actions">
          <a class="button" href="https://line.me/R/ti/p/@awbizpattaya">Contact via LINE</a>
          <a class="button-dark" href="../contact/">Contact Page</a>
        </div>
      </div>
    </div>
  </section>
</main>
```

- [ ] **Step 2: Add page-level styling only where needed**

Use the existing stitched page classes first. If the About page needs any small unique styling, add it near the stitched section rules in `assets/css/styles.css` so the page still inherits the shared design language.

Keep the page visually aligned with the current service pages:

```css
.about-story-panel { ... }
.about-stats-grid { ... }
```

Do not introduce a separate visual system.

- [ ] **Step 3: Verify the page reads as About Us**

Make sure the page includes:

- 10+ years experience
- professional management
- Pattaya locality
- Thai and English support
- natural SEO wording for visa, work permit, business registration, accounting services, and document support

### Task 2: Wire About Us into global navigation and footer

**Files:**
- Modify: `index.html`
- Modify: `faq/index.html`
- Modify: `contact/index.html`
- Modify: `privacy-policy/index.html`
- Modify: `terms/index.html`
- Modify: `pdpa-notice/index.html`
- Modify: `visa-services/index.html`
- Modify: `visa-services/**/index.html`
- Modify: `work-permit/index.html`
- Modify: `work-permit/**/index.html`
- Modify: `business-services/index.html`
- Modify: `business-services/**/index.html`
- Modify: `personal-services/index.html`
- Modify: `personal-services/**/index.html`
- Modify: `news/**/index.html`
- Modify: `assets/css/styles.css` only if the new nav/footer link needs spacing adjustments

- [ ] **Step 1: Add the Company menu link**

Update the shared Company dropdown on every page so it includes About Us before FAQ and Contact:

```html
<div class="nav-menu-column">
  <h2>Company</h2>
  <a href="../about/">About Us</a>
  <a href="../faq/">FAQ</a>
  <a href="../contact/">Contact</a>
</div>
```

For nested pages, keep the relative path correct:

```html
<a href="../../about/">About Us</a>
```

- [ ] **Step 2: Add the About Us footer link**

Add About Us to the Company footer column so the page is reachable from the footer on every route:

```html
<div class="footer-links footer-contact-links">
  <h2>Company</h2>
  <a href="../about/">About Us</a>
  <a href="../faq/">FAQ</a>
  <a href="../contact/">Contact</a>
</div>
```

Use the correct relative path on nested pages.

- [ ] **Step 3: Keep policy links separate**

Do not move the legal policy pages into the About Us section. The About page is for company story and conversion. Policies stay in the Policy footer column and in the policy pages.

### Task 3: Register the page in site checks and sitemap

**Files:**
- Modify: `tests/check_site.py`
- Modify: `sitemap.xml`

- [ ] **Step 1: Add the route to the static checker**

Add the About page to the route map:

```python
ROUTES = {
    "Home": "index.html",
    "About Us": "about/index.html",
    "FAQ": "faq/index.html",
    "Contact": "contact/index.html",
    "Privacy Policy": "privacy-policy/index.html",
    "Terms": "terms/index.html",
    "PDPA Notice": "pdpa-notice/index.html",
}
```

Add `About Us` to the required top-level navigation labels or related assertions if needed:

The existing `required_top_level` list should stay unchanged. The only check change is that the Company menu assertion should now expect `About Us` in addition to `FAQ` and `Contact`.

Then make sure the Company menu assertions also accept `About Us`.

- [ ] **Step 2: Add the About page to sitemap.xml**

Include the new route in the sitemap alongside the other top-level pages:

```xml
<url>
  <loc>https://awbizpattaya.com/about/</loc>
</url>
```

- [ ] **Step 3: Run the static verification**

Run:

```bash
python3 tests/check_site.py
```

Expected: `Static site checks passed for 37 routes.`

- [ ] **Step 4: Smoke test the new page in a browser**

Open:

```text
http://localhost:8765/about/
```

Confirm:

- the hero image renders
- the About story reads naturally
- the service cards link correctly
- the header and footer still match the rest of the site

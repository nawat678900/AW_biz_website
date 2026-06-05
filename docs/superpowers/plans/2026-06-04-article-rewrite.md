# Article Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite all existing article pages into long-form, source-informed SEO articles with clear structure and reusable layout patterns.

**Architecture:** Keep the current article URLs and site navigation intact. Replace the body content of each detail page with a consistent article template that includes a hero, several structured content sections, a checklist or tips block, and the existing related-articles carousel. Preserve the current header/footer and pagination behavior while making the article copy substantially richer and easier to maintain.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, local Node scripting for batch page generation, public web research for topic grounding.

---

### Task 1: Gather source notes and article outlines

**Files:**
- Modify: `news/*.html` content only after outline approval
- Create: `scripts/rewrite-articles.mjs`

- [ ] **Step 1: Review official and reputable sources for each article topic**

Focus on the 10 current article topics and note the main facts to include: immigration 90-day reporting, VAT timing, DBD registration, work permit rules, retirement visa basics, marriage visa requirements, DLT guidance, and legal contract review principles.

- [ ] **Step 2: Draft a reusable content outline for every article**

Use the same pattern for each page:
hero lead, overview section, practical guidance section, common mistakes or checklist, CTA, and related articles block.

- [ ] **Step 3: Keep the article set and URLs unchanged**

Do not add new article URLs or rename the current ones.

### Task 2: Rewrite all 10 article pages

**Files:**
- Modify: `news/local-team-pattaya/index.html`
- Modify: `news/visa-service-checklist-pattaya/index.html`
- Modify: `news/business-accounting-guidance-pattaya/index.html`
- Modify: `news/work-permit-renewal-guide/index.html`
- Modify: `news/tax-filing-vat-basics/index.html`
- Modify: `news/ninety-day-report-document-guide/index.html`
- Modify: `news/driving-license-support-guide/index.html`
- Modify: `news/marriage-visa-documents/index.html`
- Modify: `news/retirement-visa-requirements/index.html`
- Modify: `news/legal-consultation-business-support/index.html`

- [ ] **Step 1: Replace each page’s main content with a long-form structured article**

Keep the existing header, footer, canonical URL, and related-articles carousel. Add enough original copy to exceed 300 words per article, with clear subheadings and practical guidance.

- [ ] **Step 2: Update metadata for each page**

Adjust the title, meta description, keywords, Open Graph tags, and JSON-LD so each article reflects its own topic and remains SEO focused.

- [ ] **Step 3: Keep related articles pagination working**

Exclude the current article from the “More articles to read” block while showing the rest of the library.

### Task 3: Verify site integrity

**Files:**
- Modify: `tests/check_site.py` if route coverage changes

- [ ] **Step 1: Run the static site checker**

Confirm every route still resolves and the updated article pages render as expected.

- [ ] **Step 2: Inspect the article hub and a sample detail page in a browser**

Check that the hub still lists all articles and the long-form pages keep their layout clean on desktop and mobile.

- [ ] **Step 3: Fix any mismatches found during verification**

Address broken links, malformed HTML, metadata mistakes, or layout regressions before finishing.

# Homepage Motion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add subtle, professional motion to the homepage so the landing page feels more polished without hurting readability, responsiveness, or conversion.

**Architecture:** Keep the motion scoped to the homepage and use two layers: a gentle hero entrance animation that plays on load, and scroll-triggered reveal animations for selected cards and section content. Use the existing CSS/JS structure, respect reduced-motion preferences, and avoid changes that compete with the primary CTA.

**Tech Stack:** Static HTML, CSS keyframes/transitions, vanilla JavaScript `IntersectionObserver`.

---

### Task 1: Mark the homepage and define motion styles

**Files:**
- Modify: `index.html`
- Modify: `assets/css/styles.css`

- [ ] **Step 1: Add a homepage-only hook**

```html
<body class="aw-homepage">
```

- [ ] **Step 2: Add hero entrance and subtle drift styles**

```css
.aw-homepage .aw-hero-image img {
  animation: awHeroFloat 18s ease-in-out infinite;
}

.aw-homepage .aw-hero-content > * {
  opacity: 0;
  transform: translateY(16px);
  animation: awHeroRise 720ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
```

- [ ] **Step 3: Add scroll-reveal styles for homepage blocks**

```css
.aw-homepage .motion-reveal {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 700ms ease, transform 700ms cubic-bezier(0.16, 1, 0.3, 1);
}

.aw-homepage .motion-reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}
```

### Task 2: Wire the scroll reveal behavior

**Files:**
- Modify: `assets/js/site.js`

- [ ] **Step 1: Add a homepage motion initializer**

```js
function setupHomepageMotion() {
  var root = document.body;

  if (!root || !root.classList.contains("aw-homepage")) {
    return;
  }

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var targets = Array.prototype.slice.call(document.querySelectorAll(
    ".section-heading, .feature-card, .process-step, .aw-news-card, .testimonial, .customer-photo-card, .cta-panel, .map-panel"
  ));

  targets.forEach(function (element) {
    element.classList.add("motion-reveal");
  });

  if (reduceMotion || !("IntersectionObserver" in window)) {
    targets.forEach(function (element) {
      element.classList.add("is-visible");
    });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.18, rootMargin: "0px 0px -8% 0px" });

  targets.forEach(function (element) {
    observer.observe(element);
  });
}
```

- [ ] **Step 2: Call the new initializer with the existing startup chain**

```js
setupHomepageMotion();
```

### Task 3: Verify homepage motion behavior

**Files:**
- Modify: none unless verification finds issues

- [ ] **Step 1: Run the static site checker**

Confirm all routes still pass after the motion hooks are added.

- [ ] **Step 2: Review the homepage in a browser**

Check that the hero animates softly, section cards reveal on scroll, and the page still feels calm on mobile.

- [ ] **Step 3: Confirm reduced-motion behavior**

Ensure motion is skipped for users who prefer reduced motion.

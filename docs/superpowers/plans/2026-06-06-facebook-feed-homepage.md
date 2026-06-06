# Facebook Feed Homepage Section Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an automatic 6-post Facebook feed section directly under the homepage hero on the English and Thai landing pages.

**Architecture:** A Netlify Function will fetch the latest public posts from the AW Business Facebook Page using a server-side access token stored in Netlify environment variables. The homepage will render a clean card grid below the hero and populate it with the function response. If the feed cannot load, the section will remain usable and show a short fallback message instead of breaking the page.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Netlify Functions, Facebook Graph API, Netlify environment variables.

---

### Task 1: Add the server-side Facebook feed endpoint

**Files:**
- Create: `netlify/functions/facebook-posts.js`
- Modify: `_redirects`

- [ ] **Step 1: Write the endpoint**

```js
const PAGE_ID = process.env.FACEBOOK_PAGE_ID;
const ACCESS_TOKEN = process.env.FACEBOOK_PAGE_ACCESS_TOKEN;
const GRAPH_VERSION = process.env.FACEBOOK_GRAPH_VERSION || "v20.0";

exports.handler = async function () {
  if (!PAGE_ID || !ACCESS_TOKEN) {
    return {
      statusCode: 503,
      headers: { "content-type": "application/json; charset=utf-8" },
      body: JSON.stringify({ posts: [], source: "missing-credentials" })
    };
  }

  const url = new URL(`https://graph.facebook.com/${GRAPH_VERSION}/${PAGE_ID}/posts`);
  url.searchParams.set("fields", "message,full_picture,permalink_url,created_time,story");
  url.searchParams.set("limit", "6");
  url.searchParams.set("access_token", ACCESS_TOKEN);

  const response = await fetch(url);
  const data = await response.json();

  const posts = Array.isArray(data.data)
    ? data.data.slice(0, 6).map((post) => ({
        id: post.id || "",
        message: post.message || post.story || "",
        image: post.full_picture || "",
        url: post.permalink_url || `https://www.facebook.com/${PAGE_ID}`,
        createdTime: post.created_time || ""
      }))
    : [];

  return {
    statusCode: 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "public, max-age=300, stale-while-revalidate=3600"
    },
    body: JSON.stringify({ posts })
  };
};
```

- [ ] **Step 2: Add a friendly redirect**

```txt
/api/facebook-posts /.netlify/functions/facebook-posts 200
```

- [ ] **Step 3: Verify the endpoint path exists**

Run: `cat _redirects && test -f netlify/functions/facebook-posts.js`
Expected: the redirect line is present and the function file exists.

### Task 2: Add the homepage feed section and render logic

**Files:**
- Modify: `index.html`
- Modify: `th/index.html`
- Modify: `assets/js/site.js`
- Modify: `assets/css/styles.css`

- [ ] **Step 1: Add the section markup below the hero**

```html
<section class="section section-soft facebook-feed-section" data-facebook-feed>
  <div class="container">
    <div class="section-heading">
      <span class="eyebrow">Facebook updates</span>
      <h2>Latest updates from AW Business Service</h2>
      <p>See the newest public posts from our Facebook page in a clean card layout.</p>
    </div>
    <div class="facebook-feed-grid" data-facebook-feed-list aria-live="polite"></div>
    <div class="section-link-row">
      <a class="button-secondary" href="https://www.facebook.com/profile.php?id=61570829170335" target="_blank" rel="noopener">Visit Facebook page</a>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add the fetch-and-render logic**

```js
function setupFacebookFeed() {
  var section = document.querySelector("[data-facebook-feed]");
  var list = document.querySelector("[data-facebook-feed-list]");
  if (!section || !list) return;

  fetch("/api/facebook-posts")
    .then(function (response) { return response.json(); })
    .then(function (data) {
      var posts = Array.isArray(data.posts) ? data.posts.slice(0, 6) : [];
      if (!posts.length) {
        section.setAttribute("data-facebook-feed-state", "empty");
        list.innerHTML = '<div class="facebook-feed-empty">Facebook updates will appear here once the feed credentials are configured.</div>';
        return;
      }

      list.innerHTML = posts.map(function (post) {
        var text = (post.message || "").trim();
        var excerpt = text.length > 140 ? text.slice(0, 137) + "..." : text;
        return (
          '<article class="facebook-feed-card">' +
            '<a class="facebook-feed-image" href="' + escapeHtml(post.url) + '" target="_blank" rel="noopener">' +
              (post.image ? '<img src="' + escapeHtml(post.image) + '" alt="Facebook post image" loading="lazy" decoding="async">' : '') +
            '</a>' +
            '<div class="facebook-feed-body">' +
              '<p class="facebook-feed-meta">Facebook update</p>' +
              '<p class="facebook-feed-text">' + escapeHtml(excerpt || "Open the post on Facebook to read more.") + '</p>' +
              '<a class="facebook-feed-link" href="' + escapeHtml(post.url) + '" target="_blank" rel="noopener">Read on Facebook</a>' +
            '</div>' +
          '</article>'
        );
      }).join("");
    })
    .catch(function () {
      section.setAttribute("data-facebook-feed-state", "error");
      list.innerHTML = '<div class="facebook-feed-empty">Facebook updates could not be loaded right now.</div>';
    });
}
```

- [ ] **Step 3: Style the new card grid for desktop and mobile**

```css
.facebook-feed-section { padding-top: 0; }
.facebook-feed-grid { display: grid; gap: 20px; grid-template-columns: repeat(3, minmax(0, 1fr)); }
.facebook-feed-card { background: #fff; border: 1px solid #dbe8f2; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(7, 98, 150, 0.08); }
.facebook-feed-image img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; display: block; }
.facebook-feed-body { padding: 18px; display: grid; gap: 10px; }
.facebook-feed-meta { margin: 0; font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; color: #6b7c8d; }
.facebook-feed-text { margin: 0; color: #253341; }
.facebook-feed-link { color: #0b6f95; font-weight: 600; }
.facebook-feed-empty { padding: 20px; border: 1px dashed #c5d7e4; border-radius: 18px; background: #f7fbfe; color: #456; }
@media (max-width: 900px) { .facebook-feed-grid { grid-template-columns: 1fr; } }
```

- [ ] **Step 4: Add the section to the homepage motion observer**

```js
var targets = Array.prototype.slice.call(document.querySelectorAll(
  ".section-heading, .feature-card, .process-step, .testimonial, .customer-photo-card, .cta-panel, .map-panel, .facebook-feed-card"
));
```

- [ ] **Step 5: Confirm the homepage still loads without the feed**

Run: `python3 tests/check_site.py`
Expected: `Static site checks passed for 54 routes.`

### Task 3: Mirror the section on the Thai homepage

**Files:**
- Modify: `th/index.html`
- Modify: `assets/js/site.js`
- Modify: `assets/css/styles.css`

- [ ] **Step 1: Add the Thai section copy below the hero**

```html
<section class="section section-soft facebook-feed-section" data-facebook-feed>
  <div class="container">
    <div class="section-heading">
      <span class="eyebrow">อัปเดตจาก Facebook</span>
      <h2>โพสต์ล่าสุดจาก AW Business Service</h2>
      <p>ดูอัปเดตสาธารณะล่าสุดจากหน้า Facebook ของเราในรูปแบบการ์ดที่อ่านง่าย</p>
    </div>
    <div class="facebook-feed-grid" data-facebook-feed-list aria-live="polite"></div>
    <div class="section-link-row">
      <a class="button-secondary" href="https://www.facebook.com/profile.php?id=61570829170335" target="_blank" rel="noopener">ไปที่เพจ Facebook</a>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Re-run the site checker**

Run: `python3 tests/check_site.py`
Expected: `Static site checks passed for 54 routes.`

- [ ] **Step 3: Confirm both language pages preserve the hero-first layout**

Run: `rg -n \"aw-hero|facebook-feed-section|news-info\" index.html th/index.html`
Expected: the new Facebook section appears directly after the hero and before the article/news section.


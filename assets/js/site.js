(function () {
  var TRACKING_CONFIG = {
    ga4Id: "",
    metaPixelId: ""
  };

  var CONSENT_VERSION = "2";
  var CONSENT_STORAGE_KEY = "awbiz_cookie_consent";
  var CONSENT_COOKIE_NAME = "awbiz_cookie_consent";
  var ICON_MAP = {
    "1S": "shield-check",
    "AC": "receipt-text",
    "AD": "map-pin",
    "AP": "calendar-days",
    "AU": "file-check",
    "BH": "building-2",
    "BK": "banknote",
    "CE": "refresh-cw",
    "CF": "building-2",
    "CO": "landmark",
    "CP": "clipboard-check",
    "CT": "signature",
    "DB": "clipboard-check",
    "DC": "file-text",
    "DS": "clipboard-check",
    "ED": "file-text",
    "EN": "globe",
    "FA": "users",
    "FM": "users",
    "FR": "user",
    "LG": "map-pin",
    "LI": "message-circle",
    "LN": "message-circle",
    "MA": "users",
    "NB": "passport",
    "NW": "briefcase",
    "OF": "map-pin",
    "OK": "circle-check-big",
    "LW": "scale",
    "PH": "user",
    "PS": "user",
    "PT": "map-pin",
    "QU": "clipboard",
    "RE": "map-pin",
    "RN": "refresh-cw",
    "RO": "shield-check",
    "SM": "briefcase",
    "SS": "users",
    "TH": "globe",
    "TR": "languages",
    "TX": "receipt-text",
    "UP": "message-circle",
    "VI": "plane",
    "VS": "plane",
    "VT": "receipt-text",
    "WP": "briefcase"
  };

  var LIGHT_ICON_MAP = {
    "PH": "phone"
  };

  function setupIconSystem() {
    document.querySelectorAll(".icon-box").forEach(function (box) {
      var code = box.textContent.trim();
      var iconName =
        (box.classList.contains("light-icon") && LIGHT_ICON_MAP[code]) ||
        ICON_MAP[code];

      if (!iconName) {
        return;
      }

      box.setAttribute("data-lucide", iconName);
      box.textContent = "";
      box.classList.add("has-svg-icon");
      box.setAttribute("aria-hidden", "true");
    });

    if (window.lucide && typeof window.lucide.createIcons === "function") {
      window.lucide.createIcons();
    }
  }

  function setupMobileMenu() {
    var toggle = document.querySelector("[data-menu-toggle]");
    var menu = document.querySelector("[data-mobile-nav]");

    if (!toggle || !menu) {
      return;
    }

    toggle.addEventListener("click", function () {
      var isOpen = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });

    menu.addEventListener("click", function (event) {
      if (event.target instanceof HTMLAnchorElement) {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  function setupLanguageSwitch() {
    var translations = {
      en: {
        "nav.home": "Home",
        "nav.services": "Services",
        "nav.article": "Article",
        "nav.company": "Company",
        "nav.contact": "Contact",
        "nav.contact_line": "Contact",
        "nav.services_home": "Services Home",
        "nav.visa_services": "Visa Services",
        "nav.work_permit": "Work Permit",
        "nav.business_services": "Business Services",
        "nav.personal_services": "Personal Services",
        "nav.article_home": "Article Home",
        "nav.about_us": "About Us",
        "nav.faq": "FAQ",
        "nav.visa_title": "Visa Services",
        "nav.work_title": "Work Permit",
        "nav.business_title": "Business Services",
        "nav.personal_title": "Personal Services",
        "nav.legal_title": "Legal Service",
        "nav.business_visa": "Business Visa Pattaya",
        "nav.retirement_visa": "Retirement Visa Pattaya",
        "nav.visa_document": "Visa Document Preparation",
        "nav.view_all_visa": "View all visa services",
        "nav.work_application": "Work Permit Application Pattaya",
        "nav.work_renewal": "Work Permit Renewal Pattaya",
        "nav.work_employer": "Employer Support",
        "nav.view_all_work": "View all work permit services",
        "nav.company_registration": "Company Registration Pattaya",
        "nav.accounting_services": "Accounting Services Pattaya",
        "nav.tax_filing": "Tax Filing Pattaya",
        "nav.view_all_business": "View all business services",
        "nav.driving_license": "Driving License Pattaya",
        "nav.residence_report": "Residence Report",
        "nav.ninety_day_report": "90-Day Report Pattaya",
        "nav.view_all_personal": "View all personal services",
        "nav.legal_consultation": "Legal Consultation",
        "nav.contract_review": "Contract Review",
        "nav.document_support": "Document Support",
        "nav.view_all_legal": "View all legal services"
      },
      th: {
        "nav.home": "หน้าหลัก",
        "nav.services": "บริการ",
        "nav.article": "บทความ",
        "nav.company": "บริษัท",
        "nav.contact": "ติดต่อ",
        "nav.contact_line": "ติดต่อ LINE",
        "nav.services_home": "หน้าบริการ",
        "nav.visa_services": "บริการวีซ่า",
        "nav.work_permit": "ใบอนุญาตทำงาน",
        "nav.business_services": "บริการธุรกิจ",
        "nav.personal_services": "บริการส่วนบุคคล",
        "nav.article_home": "หน้าบทความ",
        "nav.about_us": "เกี่ยวกับเรา",
        "nav.faq": "คำถามที่พบบ่อย",
        "nav.visa_title": "บริการวีซ่า",
        "nav.work_title": "ใบอนุญาตทำงาน",
        "nav.business_title": "บริการธุรกิจ",
        "nav.personal_title": "บริการส่วนบุคคล",
        "nav.legal_title": "บริการกฎหมาย",
        "nav.business_visa": "วีซ่าธุรกิจ พัทยา",
        "nav.retirement_visa": "วีซ่าเกษียณ พัทยา",
        "nav.visa_document": "เตรียมเอกสารวีซ่า",
        "nav.view_all_visa": "ดูบริการวีซ่าทั้งหมด",
        "nav.work_application": "ยื่นใบอนุญาตทำงาน พัทยา",
        "nav.work_renewal": "ต่อใบอนุญาตทำงาน พัทยา",
        "nav.work_employer": "บริการนายจ้าง",
        "nav.view_all_work": "ดูบริการใบอนุญาตทำงานทั้งหมด",
        "nav.company_registration": "จดทะเบียนบริษัท พัทยา",
        "nav.accounting_services": "บริการบัญชี พัทยา",
        "nav.tax_filing": "ยื่นภาษี พัทยา",
        "nav.view_all_business": "ดูบริการธุรกิจทั้งหมด",
        "nav.driving_license": "ใบขับขี่ พัทยา",
        "nav.residence_report": "แจ้งที่พักอาศัย",
        "nav.ninety_day_report": "รายงาน 90 วัน พัทยา",
        "nav.view_all_personal": "ดูบริการส่วนบุคคลทั้งหมด",
        "nav.legal_consultation": "ให้คำปรึกษากฎหมาย",
        "nav.contract_review": "ตรวจสัญญา",
        "nav.document_support": "จัดเตรียมเอกสาร",
        "nav.view_all_legal": "ดูบริการกฎหมายทั้งหมด"
      }
    };

    var options = Array.prototype.slice.call(document.querySelectorAll("[data-lang-option]"));

    function normalizePath(pathname) {
      if (!pathname) {
        return "/";
      }

      return pathname.replace(/\/{2,}/g, "/");
    }

    function isThaiPath(pathname) {
      pathname = normalizePath(pathname);
      return pathname === "/th" || pathname.indexOf("/th/") === 0;
    }

    function languageFromPath(pathname) {
      return isThaiPath(pathname) ? "th" : "en";
    }

    function counterpartPath(pathname, lang) {
      pathname = normalizePath(pathname);

      if (lang === "th") {
        if (isThaiPath(pathname)) {
          return pathname;
        }

        return pathname === "/" ? "/th/" : "/th" + pathname;
      }

      if (pathname === "/th") {
        return "/";
      }

      if (isThaiPath(pathname)) {
        return pathname.slice(3) || "/";
      }

      return pathname;
    }

    var activeLang = languageFromPath(window.location.pathname);

    if (!options.length) {
      return;
    }

    options.forEach(function (button) {
      button.addEventListener("click", function () {
        var targetLang = button.getAttribute("data-lang-option") === "th" ? "th" : "en";
        var targetPath = counterpartPath(window.location.pathname, targetLang);
        var nextUrl = targetPath + window.location.search + window.location.hash;

        if (nextUrl !== window.location.pathname + window.location.search + window.location.hash) {
          window.location.href = nextUrl;
        }
      });
    });

    document.documentElement.lang = activeLang;

    options.forEach(function (button) {
      var isActive = button.getAttribute("data-lang-option") === activeLang;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
    });
  }

  function setupContactForm() {
    var form = document.querySelector("[data-contact-form]");
    var status = document.querySelector("[data-form-status]");

    if (!form || !status) {
      return;
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      if (!form.checkValidity()) {
        form.reportValidity();
        status.classList.remove("is-visible");
        return;
      }

      var lang = document.documentElement.lang === "th" ? "th" : "en";
      var nameField = form.querySelector("[name='name']");
      var contactField = form.querySelector("[name='contact']");
      var serviceField = form.querySelector("[name='service']");
      var messageField = form.querySelector("[name='message']");

      var name = nameField && nameField.value ? nameField.value.trim() : "";
      var contact = contactField && contactField.value ? contactField.value.trim() : "";
      var service = serviceField && serviceField.value ? serviceField.value.trim() : "";
      var message = messageField && messageField.value ? messageField.value.trim() : "";
      var subject = (lang === "th" ? "สอบถามบริการจาก AW Business Service Pattaya" : "Inquiry for AW Business Service Pattaya") +
        (service ? " - " + service : "");
      var bodyLines = [];

      if (name) {
        bodyLines.push((lang === "th" ? "ชื่อ:" : "Name:") + " " + name);
      }
      if (contact) {
        bodyLines.push((lang === "th" ? "ช่องทางติดต่อ:" : "Contact:") + " " + contact);
      }
      if (service) {
        bodyLines.push((lang === "th" ? "บริการที่ต้องการ:" : "Service required:") + " " + service);
      }
      if (message) {
        bodyLines.push("");
        bodyLines.push(message);
      }

      var mailtoUrl =
        "mailto:info@awbizpattaya.com?subject=" +
        encodeURIComponent(subject) +
        "&body=" +
        encodeURIComponent(bodyLines.join("\n"));

      window.location.href = mailtoUrl;
      status.innerHTML =
        lang === "th"
          ? "<strong>กำลังเปิดแอปอีเมลของคุณ</strong> พร้อมร่างข้อความถึง info@awbizpattaya.com"
          : "<strong>Your email app is opening.</strong> A draft is being prepared for info@awbizpattaya.com.";
      status.classList.add("is-visible");
      status.focus();
    });
  }

  function setupHomepageMotion() {
    var root = document.body;

    if (!root || !root.classList.contains("aw-homepage")) {
      return;
    }

    var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var targets = Array.prototype.slice.call(document.querySelectorAll(
      ".section-heading, .feature-card, .process-step, .testimonial, .customer-photo-card, .cta-panel, .map-panel"
    ));

    if (!targets.length) {
      return;
    }

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
    }, {
      threshold: 0.18,
      rootMargin: "0px 0px -8% 0px"
    });

    targets.forEach(function (element) {
      observer.observe(element);
    });
  }

  function setupConsentBanner() {
    if (!document.body) {
      return;
    }

    var existingConsent = readConsentState();
    var language = document.documentElement.lang === "th" ? "th" : "en";

    if (existingConsent) {
      applyConsentState(existingConsent);
      return;
    }

    var banner = createConsentBanner(language);
    document.body.appendChild(banner);

    var acceptAllButton = banner.querySelector("[data-cookie-accept-all]");
    var rejectAllButton = banner.querySelector("[data-cookie-reject-all]");
    var manageButton = banner.querySelector("[data-cookie-manage]");

    function persistAndApply(state) {
      writeConsentState(state);
      applyConsentState(state);
      banner.remove();
    }

    acceptAllButton.addEventListener("click", function () {
      persistAndApply({
        necessary: true,
        analytics: true,
        marketing: true
      });
    });

    rejectAllButton.addEventListener("click", function () {
      persistAndApply({
        necessary: true,
        analytics: false,
        marketing: false
      });
    });

    manageButton.addEventListener("click", function () {
      window.location.href = "/pdpa-notice/";
    });
  }

  function createConsentBanner(language) {
    var texts = {
      en: {
        title: "Cookies and privacy",
        body:
          "We use essential cookies to keep the site working. You can choose whether to allow analytics and marketing cookies.",
        acceptAll: "Accept all",
        rejectAll: "Reject all",
        manage: "Manage",
        privacy: "Privacy Policy",
        pdpa: "PDPA Notice"
      },
      th: {
        title: "คุกกี้และความเป็นส่วนตัว",
        body:
          "เราใช้คุกกี้ที่จำเป็นเพื่อให้เว็บไซต์ทำงานได้อย่างถูกต้อง คุณสามารถเลือกอนุญาตคุกกี้วิเคราะห์และคุกกี้การตลาดได้",
        acceptAll: "ยอมรับทั้งหมด",
        rejectAll: "ปฏิเสธทั้งหมด",
        manage: "จัดการ",
        privacy: "นโยบายความเป็นส่วนตัว",
        pdpa: "ประกาศ PDPA"
      }
    };

    var t = texts[language] || texts.en;
    var banner = document.createElement("section");
    banner.className = "cookie-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-label", t.title);
    banner.innerHTML =
      '<div class="cookie-banner__panel">' +
      '<div class="cookie-banner__copy">' +
      '<div class="cookie-banner__title-row">' +
      '<span class="cookie-banner__icon" aria-hidden="true">' +
      '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-cookie-icon lucide-cookie">' +
      '<path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5"></path>' +
      '<path d="M8.5 8.5v.01"></path>' +
      '<path d="M16 15.5v.01"></path>' +
      '<path d="M12 12v.01"></path>' +
      '<path d="M11 17v.01"></path>' +
      '<path d="M7 14v.01"></path>' +
      "</svg>" +
      "</span>" +
      '<p class="cookie-banner__eyebrow">' + escapeHtml(t.title) + "</p>" +
      "</div>" +
      "<p>" + escapeHtml(t.body) + "</p>" +
      '<p class="cookie-banner__links"><a href="/privacy-policy/">' + escapeHtml(t.privacy) + '</a><a href="/pdpa-notice/">' + escapeHtml(t.pdpa) + "</a></p>" +
      "</div>" +
      '<div class="cookie-banner__actions">' +
      '<button type="button" class="button-dark cookie-button" data-cookie-reject-all>' + escapeHtml(t.rejectAll) + "</button>" +
      '<button type="button" class="button-secondary cookie-button" data-cookie-manage>' + escapeHtml(t.manage) + "</button>" +
      '<button type="button" class="button cookie-button" data-cookie-accept-all>' + escapeHtml(t.acceptAll) + "</button>" +
      "</div>" +
      "</div>";

    return banner;
  }

  function readConsentState() {
    var stored = null;

    try {
      stored = window.localStorage.getItem(CONSENT_STORAGE_KEY);
    } catch (error) {
      stored = null;
    }

    if (!stored) {
      var cookieMatch = document.cookie.match(new RegExp("(^|; )" + CONSENT_COOKIE_NAME + "=([^;]*)"));
      stored = cookieMatch ? decodeURIComponent(cookieMatch[2]) : null;
    }

    if (!stored) {
      return null;
    }

    try {
      var parsed = JSON.parse(stored);

      if (!parsed || parsed.version !== CONSENT_VERSION) {
        return null;
      }

      return parsed;
    } catch (error) {
      return null;
    }
  }

  function writeConsentState(state) {
    var serialized = JSON.stringify({
      version: CONSENT_VERSION,
      necessary: true,
      analytics: Boolean(state && state.analytics),
      marketing: Boolean(state && state.marketing)
    });

    try {
      window.localStorage.setItem(CONSENT_STORAGE_KEY, serialized);
    } catch (error) {
      // Ignore storage failures and continue with the cookie fallback.
    }

    document.cookie =
      CONSENT_COOKIE_NAME +
      "=" +
      encodeURIComponent(serialized) +
      "; path=/; max-age=31536000; samesite=lax";
  }

  function applyConsentState(state) {
    var consent = state || { necessary: true, analytics: false, marketing: false };

    if (consent.analytics && TRACKING_CONFIG.ga4Id) {
      loadGoogleAnalytics(TRACKING_CONFIG.ga4Id);
    }

    if (consent.marketing && TRACKING_CONFIG.metaPixelId) {
      loadMetaPixel(TRACKING_CONFIG.metaPixelId);
    }
  }

  function loadGoogleAnalytics(measurementId) {
    if (document.querySelector('script[data-awbiz-ga4]')) {
      return;
    }

    window.dataLayer = window.dataLayer || [];

    function gtag() {
      window.dataLayer.push(arguments);
    }

    window.gtag = window.gtag || gtag;

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(measurementId);
    script.setAttribute("data-awbiz-ga4", "true");
    document.head.appendChild(script);

    window.gtag("js", new Date());
    window.gtag("config", measurementId, { anonymize_ip: true });
  }

  function loadMetaPixel(pixelId) {
    if (document.querySelector('script[data-awbiz-meta-pixel]')) {
      return;
    }

    if (!window.fbq) {
      var fbq = function () {
        fbq.callMethod ? fbq.callMethod.apply(fbq, arguments) : fbq.queue.push(arguments);
      };

      fbq.queue = [];
      fbq.version = "2.0";
      fbq.loaded = true;
      fbq.push = fbq;
      fbq.callMethod = null;
      window.fbq = fbq;
    }

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://connect.facebook.net/en_US/fbevents.js";
    script.setAttribute("data-awbiz-meta-pixel", "true");
    document.head.appendChild(script);

    window.fbq("init", pixelId);
    window.fbq("track", "PageView");
  }

  function setupPagination(options) {
    document.querySelectorAll(options.sectionSelector).forEach(function (section) {
      var list = section.querySelector(options.listSelector);
      var cards = Array.prototype.slice.call(section.querySelectorAll(options.cardSelector));
      var previousButton = section.querySelector(options.previousSelector);
      var nextButton = section.querySelector(options.nextSelector);
      var perPage = Number(section.getAttribute("data-page-size")) || 3;
      var duration = Number(section.getAttribute("data-carousel-duration")) || Math.max(cards.length * 6, 36);
      var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      var isInfinite = options.infinite !== false;

      if (!list || !cards.length || !previousButton || !nextButton) {
        return;
      }

      if (!isInfinite) {
        var totalPages = Math.max(Math.ceil(cards.length / perPage), 1);
        var currentPage = 0;

        cards.forEach(function (card) {
          card.hidden = false;
          card.removeAttribute("aria-hidden");
          list.appendChild(card);
        });

        function renderPage() {
          var start = currentPage * perPage;
          var end = start + perPage;

          cards.forEach(function (card, index) {
            var visible = index >= start && index < end;

            card.hidden = !visible;
            card.setAttribute("aria-hidden", String(!visible));
          });

          previousButton.disabled = totalPages <= 1;
          nextButton.disabled = totalPages <= 1;
          previousButton.setAttribute("aria-disabled", String(totalPages <= 1));
          nextButton.setAttribute("aria-disabled", String(totalPages <= 1));
        }

        function go(direction) {
          if (totalPages <= 1) {
            return;
          }

          currentPage = (currentPage + direction + totalPages) % totalPages;
          renderPage();
        }

        previousButton.addEventListener("click", function () {
          go(-1);
        });

        nextButton.addEventListener("click", function () {
          go(1);
        });

        renderPage();
        return;
      }

      var viewport = document.createElement("div");
      viewport.className = "carousel-viewport";
      list.parentNode.insertBefore(viewport, list);
      viewport.appendChild(list);
      list.classList.add("carousel-track", "is-infinite");
      list.style.setProperty("--carousel-duration", duration + "s");
      list.style.setProperty("--carousel-items", perPage);
      list.innerHTML = "";

      [false, true].forEach(function (isClone) {
        var group = document.createElement("div");

        group.className = "carousel-group";
        if (isClone) {
          group.setAttribute("aria-hidden", "true");
        }

        cards.forEach(function (card) {
          group.appendChild(isClone ? card.cloneNode(true) : card);
        });
        list.appendChild(group);
      });

      if (reduceMotion) {
        list.classList.add("is-paused");
      }

      function setDirection(direction) {
        list.classList.toggle("is-reversed", direction === "reverse");
      }

      function pauseCarousel() {
        list.classList.add("is-paused");
      }

      function resumeCarousel() {
        if (reduceMotion) {
          return;
        }

        list.classList.remove("is-paused");
      }

      previousButton.addEventListener("click", function () {
        setDirection("reverse");
      });

      nextButton.addEventListener("click", function () {
        setDirection("normal");
      });

      section.addEventListener("mouseenter", pauseCarousel);
      section.addEventListener("focusin", pauseCarousel);
      section.addEventListener("mouseleave", resumeCarousel);
      section.addEventListener("focusout", resumeCarousel);
    });
  }

  function setupReviewPagination() {
    setupPagination({
      sectionSelector: "[data-review-pagination]",
      listSelector: "[data-review-list]",
      cardSelector: "[data-review-card]",
      previousSelector: "[data-review-prev]",
      nextSelector: "[data-review-next]",
      label: "customer review",
    });
  }

  function setupCustomerPhotoPagination() {
    setupPagination({
      sectionSelector: "[data-photo-pagination]",
      listSelector: "[data-photo-list]",
      cardSelector: "[data-photo-card]",
      previousSelector: "[data-photo-prev]",
      nextSelector: "[data-photo-next]",
      label: "customer photo",
    });
  }

  function setupArticlePagination() {
    setupPagination({
      sectionSelector: "[data-article-pagination]",
      listSelector: "[data-article-list]",
      cardSelector: "[data-article-card]",
      previousSelector: "[data-article-prev]",
      nextSelector: "[data-article-next]",
      label: "article recommendation",
      infinite: false,
    });
  }

  function setupNewsPagination() {
    setupPagination({
      sectionSelector: "[data-news-pagination]",
      listSelector: "[data-news-list]",
      cardSelector: "[data-news-card]",
      previousSelector: "[data-news-prev]",
      nextSelector: "[data-news-next]",
      label: "news teaser",
    });
  }

  function escapeHtml(value) {
    return value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  setupIconSystem();
  setupMobileMenu();
  setupLanguageSwitch();
  setupContactForm();
  setupConsentBanner();
  setupHomepageMotion();
  setupNewsPagination();
  setupArticlePagination();
  setupReviewPagination();
  setupCustomerPhotoPagination();
})();

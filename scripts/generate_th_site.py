#!/usr/bin/env python3
"""Generate Thai mirror pages under /th with translated visible content."""

from __future__ import annotations

import concurrent.futures
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from bs4 import BeautifulSoup, Comment, NavigableString


ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = "https://awbizpattaya.com"
CACHE_PATH = ROOT / "scripts" / ".th-translation-cache.json"
MAX_WORKERS = 8

TRANSLATION_PROTECT = {
    "__Q7X9P1__": "AW Business Service Pattaya",
    "__Q7X9P2__": "AW Biz Co., Ltd.",
    "__Q7X9P3__": "LINE",
}

MANUAL_TRANSLATIONS = {
    "Home": "หน้าหลัก",
    "Contact LINE": "ติดต่อ",
}

URL_PREFIX_RE = re.compile(r"^https?://awbizpattaya\.com/?", re.I)
WHITESPACE_RE = re.compile(r"\s+")


def load_cache() -> Dict[str, str]:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: Dict[str, str]) -> None:
    CACHE_PATH.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def normalize_spaces(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def is_translatable_text_node(node: NavigableString) -> bool:
    parent = getattr(node, "parent", None)
    if parent is None:
        return False
    if isinstance(node, Comment):
        return False
    parent_classes = parent.get("class") or []
    if parent.name in {"script", "style", "noscript", "svg", "path", "code", "pre"}:
        return False
    if parent.get("data-lang-option") is not None:
        return False
    if "nav-lang-switch" in parent_classes:
        return False
    if "icon-box" in parent_classes:
        return False
    return True


def make_site_url(pathname: str, lang: str) -> str:
    pathname = pathname or "/"
    if not pathname.startswith("/"):
        pathname = "/" + pathname
    pathname = re.sub(r"/{2,}", "/", pathname)

    if lang == "th":
        if pathname == "/":
            return SITE_ROOT + "/th/"
        if pathname == "/th":
            return SITE_ROOT + "/th/"
        if pathname.startswith("/th/"):
            return SITE_ROOT + pathname
        return SITE_ROOT + "/th" + pathname

    if pathname == "/th":
        return SITE_ROOT + "/"
    if pathname.startswith("/th/"):
        pathname = pathname[3:]
        if not pathname:
            pathname = "/"
    return SITE_ROOT + pathname


def translate_via_google(text: str) -> str:
    protected = text
    for token, phrase in TRANSLATION_PROTECT.items():
        protected = protected.replace(phrase, token)

    url = (
        "https://translate.googleapis.com/translate_a/single"
        f"?client=gtx&sl=en&tl=th&dt=t&q={urllib.parse.quote(protected)}"
    )

    for attempt in range(3):
      try:
        raw = urllib.request.urlopen(url, timeout=30).read().decode("utf-8")
        payload = json.loads(raw)
        translated = "".join(piece[0] for piece in payload[0] if piece and piece[0])
        for token, phrase in TRANSLATION_PROTECT.items():
            translated = translated.replace(token, phrase)
        return translated
      except Exception:
        if attempt == 2:
          return text
        time.sleep(0.4 * (attempt + 1))


def collect_strings(paths: Iterable[Path]) -> List[str]:
    strings = set()
    for path in paths:
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

        for node in soup.find_all(string=True):
            if not is_translatable_text_node(node):
                continue
            text = normalize_spaces(str(node))
            if text:
                strings.add(text)

        for tag in soup.find_all(True):
            for attr in ("alt", "title", "aria-label", "placeholder", "content"):
                if tag.has_attr(attr):
                    value = normalize_spaces(str(tag.get(attr) or ""))
                    if value and not value.startswith("http"):
                        strings.add(value)

            if tag.name == "script" and tag.get("type") == "application/ld+json":
                try:
                    data = json.loads(tag.string or tag.get_text())
                except Exception:
                    continue
                gather_jsonld_strings(data, strings)

    return sorted(strings)


def gather_jsonld_strings(value, strings: set) -> None:
    if isinstance(value, str):
        if value and not value.startswith("http") and not value.startswith("mailto:") and not value.startswith("tel:"):
            strings.add(normalize_spaces(value))
        return
    if isinstance(value, list):
        for item in value:
            gather_jsonld_strings(item, strings)
        return
    if isinstance(value, dict):
        for item in value.values():
            gather_jsonld_strings(item, strings)


def translate_cache(strings: Iterable[str], cache: Dict[str, str]) -> None:
    pending = [text for text in strings if text not in cache]
    if not pending:
        return

    print(f"Translating {len(pending)} unique strings...")

    def worker(text: str) -> Tuple[str, str]:
        return text, translate_via_google(text)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for original, translated in pool.map(worker, pending):
            cache[original] = translated


def translate_text(text: str, cache: Dict[str, str]) -> str:
    key = normalize_spaces(text)
    translated = cache.get(key, text)
    if text != key:
        leading = text[: len(text) - len(text.lstrip())]
        trailing = text[len(text.rstrip()) :]
        return f"{leading}{translated}{trailing}"
    return translated


def maybe_translate_attr(tag, attr: str, cache: Dict[str, str]) -> None:
    if not tag.has_attr(attr):
        return
    value = str(tag.get(attr) or "")
    if not value or value.startswith("http") or value.startswith("tel:") or value.startswith("mailto:"):
        return
    tag[attr] = translate_text(value, cache)


def rewrite_jsonld(value, lang: str, cache: Dict[str, str]):
    if isinstance(value, str):
        if value.startswith("http://") or value.startswith("https://"):
            return rewrite_internal_url(value, lang)
        if value.startswith("mailto:") or value.startswith("tel:"):
            return value
        return translate_text(value, cache)

    if isinstance(value, list):
        return [rewrite_jsonld(item, lang, cache) for item in value]

    if isinstance(value, dict):
        rewritten = {}
        for key, item in value.items():
            if key in {"url", "mainEntityOfPage", "sameAs", "image", "logo"}:
                rewritten[key] = rewrite_jsonld(item, lang, cache)
            elif key == "inLanguage":
                rewritten[key] = lang
            elif key in {"@context", "@type", "@id"}:
                rewritten[key] = item
            else:
                rewritten[key] = rewrite_jsonld(item, lang, cache)
        return rewritten

    return value


def rewrite_internal_url(value: str, lang: str) -> str:
    if not isinstance(value, str):
        return value
    if not URL_PREFIX_RE.match(value):
        return value
    pathname = value[len(SITE_ROOT) :]
    if lang == "th":
        if pathname == "/":
            return SITE_ROOT + "/th/"
        if pathname.startswith("/th/"):
            return value
        return SITE_ROOT + "/th" + pathname
    if pathname.startswith("/th/"):
        pathname = pathname[3:]
        if not pathname:
            pathname = "/"
    return SITE_ROOT + pathname


def rebase_asset_url(value: str, dest_depth: int) -> str:
    if not isinstance(value, str):
        return value

    if value.startswith(("http://", "https://", "data:", "mailto:", "tel:", "#")):
        return value

    if "assets/" not in value:
        return value

    asset_path = value.split("assets/", 1)[1]
    return "../" * dest_depth + "assets/" + asset_path


def update_head(
    soup: BeautifulSoup,
    source_path: Path,
    lang: str,
    cache: Dict[str, str],
    dest_depth: int,
) -> None:
    head = soup.head
    if head is None:
        return

    route = path_to_route(source_path)
    target_url = make_site_url(route, lang)
    en_url = make_site_url(route, "en")
    th_url = make_site_url(route, "th")

    html_tag = soup.find("html")
    if html_tag is not None:
        html_tag["lang"] = lang

    canonical = head.find("link", attrs={"rel": lambda value: value and "canonical" in value})
    if canonical is not None:
        canonical["href"] = target_url

    og_url = head.find("meta", attrs={"property": "og:url"})
    if og_url is not None:
        og_url["content"] = target_url

    og_locale = head.find("meta", attrs={"property": "og:locale"})
    if og_locale is not None:
        og_locale["content"] = "th_TH" if lang == "th" else "en_US"

    title_tag = head.find("title")
    if title_tag and title_tag.string:
        title_tag.string.replace_with(translate_text(str(title_tag.string), cache) if lang == "th" else str(title_tag.string))

    for meta_name in ("description", "keywords"):
        tag = head.find("meta", attrs={"name": meta_name})
        if tag and tag.get("content"):
            tag["content"] = translate_text(str(tag["content"]), cache) if lang == "th" else str(tag["content"])

    for tag in head.find_all(["img", "a", "button", "input", "summary"]):
        for attr in ("alt", "title", "aria-label", "placeholder"):
            if tag.has_attr(attr):
                value = str(tag.get(attr) or "")
                if value and not value.startswith("http"):
                    if lang == "th":
                        tag[attr] = translate_text(value, cache)
        for attr in ("href", "src"):
            if tag.has_attr(attr):
                tag[attr] = rebase_asset_url(str(tag.get(attr) or ""), dest_depth)

    for script in head.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or script.get_text())
        except Exception:
            continue
        if lang == "th":
            data = rewrite_jsonld(data, lang, cache)
        else:
            data = rewrite_jsonld(data, lang, cache)
        script.string = json.dumps(data, ensure_ascii=False, indent=2)

    # Alternate links.
    for alt in head.find_all("link", attrs={"rel": "alternate"}):
        if alt.get("hreflang"):
            alt.decompose()

    th_link = soup.new_tag("link", rel="alternate", hreflang="th", href=th_url)
    en_link = soup.new_tag("link", rel="alternate", hreflang="en", href=en_url)
    head.append(th_link)
    head.append(en_link)


def translate_body(soup: BeautifulSoup, cache: Dict[str, str], dest_depth: int) -> None:
    for node in soup.find_all(string=True):
        if not is_translatable_text_node(node):
            continue
        raw = str(node)
        key = normalize_spaces(raw)
        if not key:
            continue
        translated = cache.get(key)
        if not translated:
            continue
        if raw != key:
            leading = raw[: len(raw) - len(raw.lstrip())]
            trailing = raw[len(raw.rstrip()) :]
            node.replace_with(f"{leading}{translated}{trailing}")
        else:
            node.replace_with(translated)

    for tag in soup.find_all(True):
        if "nav-lang-switch" in (tag.get("class") or []):
            continue
        if tag.name == "script" and tag.get("type") == "application/ld+json":
            continue
        for attr in ("alt", "title", "aria-label", "placeholder"):
            if tag.has_attr(attr):
                value = str(tag.get(attr) or "")
                if value and not value.startswith("http"):
                    key = normalize_spaces(value)
                    translated = cache.get(key)
                    if translated:
                        tag[attr] = translated
        for attr in ("href", "src"):
            if tag.has_attr(attr):
                tag[attr] = rebase_asset_url(str(tag.get(attr) or ""), dest_depth)


def insert_services_home_link(soup: BeautifulSoup, th_depth: int) -> None:
    desktop_nav = soup.find("nav", class_="desktop-nav")
    if desktop_nav is None:
        return

    first_services_link = desktop_nav.find("a", attrs={"data-lang-key": "nav.services_home"})
    if first_services_link is not None:
        return

    services_menu = desktop_nav.find("div", class_="nav-dropdown-service")
    if services_menu is None:
        return

    first_column = services_menu.find("div", class_="nav-menu-column")
    if first_column is None:
        return

    services_href = "../" * th_depth + "services/"
    home_link = soup.new_tag("a", **{
        "class": "nav-menu-all",
        "href": services_href,
        "data-lang-key": "nav.services_home",
    })
    home_link.string = "หน้าบริการ"

    heading = first_column.find("h2")
    if heading is not None:
        heading.insert_before(home_link)
    else:
        first_column.insert(0, home_link)


def path_to_route(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("/index.html")] + "/"
    if rel.endswith(".html"):
        return "/" + rel
    return "/" + rel


def route_to_output(path: Path) -> Path:
    rel = path.relative_to(ROOT)
    return ROOT / "th" / rel


def source_files() -> List[Path]:
    files = []
    for path in ROOT.rglob("*.html"):
        if "th" in path.parts:
            continue
        if path.name.startswith("."):
            continue
        files.append(path)
    return sorted(files)


def generate() -> None:
    sources = source_files()
    cache = load_cache()

    strings = collect_strings(sources)
    translate_cache(strings, cache)
    cache.update(MANUAL_TRANSLATIONS)
    save_cache(cache)

    for src in sources:
        dst = route_to_output(src)
        dst.parent.mkdir(parents=True, exist_ok=True)

        soup = BeautifulSoup(src.read_text(encoding="utf-8"), "html.parser")
        update_head(soup, src, "th", cache, len(dst.parent.relative_to(ROOT).parts))
        translate_body(soup, cache, len(dst.parent.relative_to(ROOT).parts))
    # The desktop Services mega menu now starts directly with the category title.

        html_root = soup.find("html")
        html = str(html_root) if html_root is not None else str(soup)
        if not html.lstrip().lower().startswith("<!doctype html>"):
            html = "<!doctype html>\n" + html
        dst.write_text(html, encoding="utf-8")
        print(f"wrote {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    generate()

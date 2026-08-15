from __future__ import annotations

import re
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup, Comment, Tag

from models import FetchJobFailed, FetchJobResult

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

NOISE_KEYWORDS: frozenset[str] = frozenset(
    {
        "cookie",
        "banner",
        "menu",
        "sidebar",
        "related",
        "newsletter",
        "advert",
        "ads",
        "ad-",
        "promo",
        "popup",
        "modal",
        "consent",
        "gdpr",
        "footer",
        "header",
        "nav-",
        "navigation",
        "social",
        "share",
        "subscribe",
        "login",
        "signup",
        "register",
        "breadcrumb",
        "pagination",
        "widget",
        "tracking",
    }
)

MIN_CONTENT_LENGTH = 300

REMOVE_TAGS: tuple[str, ...] = (
    "script",
    "style",
    "noscript",
    "iframe",
    "svg",
    "nav",
    "footer",
    "header",
    "aside",
    "form",
)




def _failed(source_url: str, error: str) -> FetchJobFailed:
    return {
        "status": "failed",
        "source_url": source_url,
        "error": error,
        "title": None,
        "cleaned_text": None,
        "raw_html_length": None,
    }


def _is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def _extract_title(soup: BeautifulSoup) -> str | None:
    title_tag = soup.find("title")
    if title_tag:
        text = title_tag.get_text(strip=True)
        if text:
            return text

    for heading in soup.find_all(["h1", "h2"], limit=5):
        text = heading.get_text(strip=True)
        if text and len(text) > 5:
            return text
    return None


def _remove_noise(soup: BeautifulSoup) -> None:
    for tag_name in REMOVE_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()

    candidates = list(soup.find_all(True))
    for tag in candidates:
        if not isinstance(tag, Tag) or tag.decomposed:
            continue
        attrs = " ".join(
            [
                str(tag.get("id") or ""),
                " ".join(tag.get("class") or []),
                str(tag.get("role") or ""),
            ]
        ).lower()
        if any(kw in attrs for kw in NOISE_KEYWORDS):
            tag.decompose()


def _get_main_content(soup: BeautifulSoup) -> Tag:
    for selector in ("article", "main", "[role='main']"):
        elem = soup.select_one(selector)
        if elem is not None:
            return elem
    body = soup.find("body")
    return body if body is not None else soup


def _html_to_clean_text(element: Tag) -> str:
    raw = element.get_text(separator="\n", strip=True)

    lines: list[str] = []
    for line in raw.splitlines():
        normalised = re.sub(r"\s+", " ", line).strip()

        if len(normalised) < 25:
            continue

        lower = normalised.lower()
        if any(
            phrase in lower
            for phrase in (
                "accept cookies",
                "cookie policy",
                "all rights reserved",
                "© ",
                "privacy policy",
                "terms of service",
                "terms of use",
            )
        ):
            continue

        lines.append(normalised)

    text = "\n\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text

def fetch_job(url: str, timeout: float = 12.0) -> FetchJobResult:
    source_url = (url or "").strip()

    if not _is_valid_url(source_url):
        return _failed(source_url, "invalid_url")

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,pl;q=0.8",
    }

    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            headers=headers,
        ) as client:
            response = client.get(source_url)
    except httpx.TimeoutException:
        return _failed(source_url, "timeout")
    except httpx.RequestError as exc:
        return _failed(source_url, f"request_error:{type(exc).__name__}")

    if response.status_code == 403:
        return _failed(source_url, "http_403")
    if response.status_code == 404:
        return _failed(source_url, "http_404")
    if not response.is_success:
        return _failed(source_url, f"http_{response.status_code}")

    raw_html = response.text
    raw_html_length = len(raw_html)

    if not raw_html.strip():
        return _failed(source_url, "empty_content")

    content_type = response.headers.get("content-type", "").lower()
    if "html" not in content_type and "text/" not in content_type:
        return _failed(source_url, "not_html")

    soup = BeautifulSoup(raw_html, "html.parser")

    # Count scripts *before* we strip them – useful for the JS-heavy heuristic.
    script_count = len(soup.find_all("script"))

    title = _extract_title(soup)
    _remove_noise(soup)
    main = _get_main_content(soup)
    cleaned_text = _html_to_clean_text(main)

    if len(cleaned_text) < MIN_CONTENT_LENGTH:
        if script_count >= 5:
            return _failed(source_url, "js_heavy_suspected")
        return _failed(source_url, "empty_content")

    return {
        "status": "success",
        "source_url": source_url,
        "title": title,
        "cleaned_text": cleaned_text,
        "raw_html_length": raw_html_length,
    }


if __name__ == "__main__":
    import json
    import sys

    # Example – replace with any real job-offer URL you want to try.
    demo_url = sys.argv[1] if len(sys.argv) > 1 else "https://nofluffjobs.com/job/senior-java-cloud-developer-azure-dahliamatic-warszawa-1"

    result = fetch_job(demo_url)
    print(json.dumps(result, indent=2, ensure_ascii=False))
from __future__ import annotations

import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Comment, Tag

from src.config import (
    FETCH_JOB_NOISE_KEYWORDS,
    FETCH_JOB_NOISE_PHRASES,
    FETCH_JOB_REMOVE_TAGS,
)
from src.models import FetchJobFailed


def build_failed_fetch_result(source_url: str, error: str) -> FetchJobFailed:
    return {
        "status": "failed",
        "source_url": source_url,
        "error": error,
        "title": None,
        "cleaned_text": None,
        "raw_html_length": None,
    }


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def extract_title(soup: BeautifulSoup) -> str | None:
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


def remove_noise(soup: BeautifulSoup) -> None:
    for tag_name in FETCH_JOB_REMOVE_TAGS:
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
        if any(keyword in attrs for keyword in FETCH_JOB_NOISE_KEYWORDS):
            tag.decompose()


def get_main_content(soup: BeautifulSoup) -> Tag:
    for selector in ("article", "main", "[role='main']"):
        elem = soup.select_one(selector)
        if elem is not None:
            return elem
    body = soup.find("body")
    return body if body is not None else soup


def html_to_clean_text(element: Tag) -> str:
    raw = element.get_text(separator="\n", strip=True)

    lines: list[str] = []
    for line in raw.splitlines():
        normalised = re.sub(r"\s+", " ", line).strip()

        if len(normalised) < 25:
            continue

        lower = normalised.lower()
        if any(phrase in lower for phrase in FETCH_JOB_NOISE_PHRASES):
            continue

        lines.append(normalised)

    text = "\n\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text

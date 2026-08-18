from __future__ import annotations

import httpx
from bs4 import BeautifulSoup

from src.config import FETCH_JOB_MIN_CONTENT_LENGTH, FETCH_JOB_USER_AGENT
from src.models import FetchJobResult
from src.utils import (
    build_failed_fetch_result,
    extract_title,
    get_main_content,
    html_to_clean_text,
    is_valid_url,
    remove_noise,
)

def fetch_job(url: str, timeout: float = 12.0) -> FetchJobResult:
    source_url = (url or "").strip()

    if not is_valid_url(source_url):
        return build_failed_fetch_result(source_url, "invalid_url")

    headers = {
        "User-Agent": FETCH_JOB_USER_AGENT,
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
        return build_failed_fetch_result(source_url, "timeout")
    except httpx.RequestError as exc:
        return build_failed_fetch_result(source_url, f"request_error:{type(exc).__name__}")

    if response.status_code == 403:
        return build_failed_fetch_result(source_url, "http_403")
    if response.status_code == 404:
        return build_failed_fetch_result(source_url, "http_404")
    if not response.is_success:
        return build_failed_fetch_result(source_url, f"http_{response.status_code}")

    raw_html = response.text
    raw_html_length = len(raw_html)

    if not raw_html.strip():
        return build_failed_fetch_result(source_url, "empty_content")

    content_type = response.headers.get("content-type", "").lower()
    if "html" not in content_type and "text/" not in content_type:
        return build_failed_fetch_result(source_url, "not_html")

    soup = BeautifulSoup(raw_html, "html.parser")

    # Count scripts *before* we strip them – useful for the JS-heavy heuristic.
    script_count = len(soup.find_all("script"))

    title = extract_title(soup)
    remove_noise(soup)
    main = get_main_content(soup)
    cleaned_text = html_to_clean_text(main)

    if len(cleaned_text) < FETCH_JOB_MIN_CONTENT_LENGTH:
        if script_count >= 5:
            return build_failed_fetch_result(source_url, "js_heavy_suspected")
        return build_failed_fetch_result(source_url, "empty_content")

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
    from src.config import DEMO_JOB_OFFER_URL

    demo_url = sys.argv[1] if len(sys.argv) > 1 else DEMO_JOB_OFFER_URL

    result = fetch_job(demo_url)
    print(json.dumps(result, indent=2, ensure_ascii=False))
#!/usr/bin/env python3
"""Validate bilingual navigation behavior against the live production site."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from html import unescape
from typing import Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


@dataclass
class PageExpectation:
    path: str
    expected_lang: str


@dataclass
class FetchResult:
    url: str
    status: int
    html: str


@dataclass
class ValidationIssue:
    path: str
    message: str


SWITCHER_DIV_RE = re.compile(r"<div[^>]*data-language-switcher[^>]*>", re.IGNORECASE | re.DOTALL)
ATTR_RE = re.compile(r"([:\w-]+)=(\"([^\"]*)\"|'([^']*)')")
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def fetch_html(url: str, timeout: float) -> FetchResult:
    request = Request(
        url,
        headers={
            "User-Agent": "jblueprint-nav-validator/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return FetchResult(url=response.geturl(), status=getattr(response, "status", 200), html=body)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return FetchResult(url=exc.geturl(), status=exc.code, html=body)
    except URLError as exc:
        raise RuntimeError(f"Cannot reach {url}: {exc}") from exc


def extract_title(html: str) -> str:
    match = TITLE_RE.search(html)
    if not match:
        return ""
    return unescape(match.group(1)).strip()


def extract_switcher_attrs(html: str) -> Optional[Dict[str, str]]:
    match = SWITCHER_DIV_RE.search(html)
    if not match:
        return None

    tag = match.group(0)
    attrs: Dict[str, str] = {}
    for attr_match in ATTR_RE.finditer(tag):
        attr_name = attr_match.group(1)
        attr_value = attr_match.group(3) if attr_match.group(3) is not None else attr_match.group(4)
        attrs[attr_name] = unescape(attr_value)
    return attrs


def validate_page(base_url: str, page: PageExpectation, timeout: float) -> Tuple[List[ValidationIssue], List[str]]:
    issues: List[ValidationIssue] = []
    checks: List[str] = []

    page_url = urljoin(base_url.rstrip("/") + "/", page.path.lstrip("/"))
    result = fetch_html(page_url, timeout=timeout)
    checks.append(f"{page.path} -> HTTP {result.status}")

    if result.status != 200:
        issues.append(ValidationIssue(page.path, f"Expected HTTP 200 but got {result.status}"))
        return issues, checks

    title = extract_title(result.html)
    if "404" in title.lower() or "not found" in title.lower():
        issues.append(ValidationIssue(page.path, f"Returned a 404 template title: '{title}'"))

    switcher = extract_switcher_attrs(result.html)
    if not switcher:
        issues.append(ValidationIssue(page.path, "Language switcher markup was not found"))
        return issues, checks

    current_lang = switcher.get("data-current-lang", "")
    if current_lang != page.expected_lang:
        issues.append(
            ValidationIssue(
                page.path,
                f"Expected data-current-lang='{page.expected_lang}' but got '{current_lang or '[missing]'}'",
            )
        )

    target_en = switcher.get("data-target-en", "")
    target_es = switcher.get("data-target-es", "")

    if not target_en:
        issues.append(ValidationIssue(page.path, "Missing data-target-en in switcher"))
    if not target_es:
        issues.append(ValidationIssue(page.path, "Missing data-target-es in switcher"))

    for label, target in (("en", target_en), ("es", target_es)):
        if not target:
            continue
        if "/404.html" in target:
            issues.append(ValidationIssue(page.path, f"Switcher target for {label} points to 404 route: {target}"))
            continue

        target_url = urljoin(base_url, target)
        target_result = fetch_html(target_url, timeout=timeout)
        checks.append(f"{page.path} [{label}] -> {target} => HTTP {target_result.status}")

        if target_result.status != 200:
            issues.append(
                ValidationIssue(
                    page.path,
                    f"Switcher target for {label} returned HTTP {target_result.status}: {target}",
                )
            )

    return issues, checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate production navigation and language switcher")
    parser.add_argument(
        "--base-url",
        default="https://jblueprint.dev/blog/",
        help="Production site URL, including its base path",
    )
    parser.add_argument("--timeout", default=10.0, type=float, help="HTTP timeout in seconds")
    args = parser.parse_args()

    pages = [
        PageExpectation(path="/", expected_lang="en"),
        PageExpectation(path="/about/", expected_lang="en"),
        PageExpectation(path="/posts/", expected_lang="en"),
        PageExpectation(
            path="/jekyll/speckit/2026/05/08/how-to-build-a-blog-with-spec-driven-design.html",
            expected_lang="en",
        ),
        PageExpectation(
            path="/jekyll/theme/2026/05/08/installing-minimal-mistakes-on-a-bilingual-jekyll-blog.html",
            expected_lang="en",
        ),
        PageExpectation(path="/es/", expected_lang="es"),
        PageExpectation(path="/es/about/", expected_lang="es"),
        PageExpectation(path="/es/posts/", expected_lang="es"),
        PageExpectation(
            path="/es/jekyll/speckit/2026/05/08/como-crear-un-blog-con-spec-driven-design.html",
            expected_lang="es",
        ),
        PageExpectation(
            path="/es/jekyll/theme/2026/05/08/instalacion-minimal-mistakes.html",
            expected_lang="es",
        ),
    ]

    all_issues: List[ValidationIssue] = []
    all_checks: List[str] = []

    for page in pages:
        try:
            issues, checks = validate_page(args.base_url, page, timeout=args.timeout)
        except RuntimeError as exc:
            print(f"ERROR: {exc}")
            return 2
        all_issues.extend(issues)
        all_checks.extend(checks)

    print("\nNavigation checks:")
    for check in all_checks:
        print(f"- {check}")

    if all_issues:
        print("\nValidation issues:")
        for issue in all_issues:
            print(f"- {issue.path}: {issue.message}")
        print(f"\nResult: FAILED ({len(all_issues)} issue(s))")
        return 1

    print("\nResult: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())

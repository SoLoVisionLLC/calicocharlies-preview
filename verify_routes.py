#!/usr/bin/env python3
"""Static contract checks for canonical preview-pill route links."""

import re
from pathlib import Path

from preview_dock import VARIANT_DOMAINS, preview_dock, route_path

ROOT = Path(__file__).resolve().parent
ROUTES = ("/", "/treats-gifts/", "/our-story/", "/whats-new/", "/visit/")


def assert_route_normalization():
    for source in ("", "/", "treats-gifts", "/treats-gifts", "//treats-gifts//"):
        expected = "/" if source in ("", "/") else "/treats-gifts/"
        assert route_path(source) == expected, (source, route_path(source))


def assert_dock_links():
    for variant in VARIANT_DOMAINS:
        for route in ROUTES:
            slug = route.strip("/")
            html = preview_dock(variant, slug)
            hrefs = re.findall(r'href="([^"]+)"', html)
            expected = [f"{domain}{route}" for domain in VARIANT_DOMAINS.values()]
            assert hrefs == expected, (variant, route, hrefs)
            assert html.count('aria-current="page"') == 1
            assert f'class="preview-design is-active"' in html


def assert_committed_artifacts():
    for variant in VARIANT_DOMAINS:
        for route in ROUTES:
            path = ROOT / "variants" / variant / route.strip("/") / "index.html"
            if route == "/":
                path = ROOT / "variants" / variant / "index.html"
            html = path.read_text()
            assert "preview-dock" in html
            assert 'name="robots" content="noindex, nofollow"' in html
            assert 'styles.css?v=20260907-dock-v7-pill-slim' in html


if __name__ == "__main__":
    assert_route_normalization()
    assert_dock_links()
    assert_committed_artifacts()
    print("verified canonical pill routes and 15 committed artifacts")

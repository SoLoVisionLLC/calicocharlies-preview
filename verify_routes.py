#!/usr/bin/env python3
"""Static contract checks for canonical preview-pill routes and typography."""

import re
from pathlib import Path

from preview_dock import ASSET_VERSION, VARIANT_DOMAINS, preview_dock, route_path

ROOT = Path(__file__).resolve().parent
ROUTES = ("/", "/treats-gifts/", "/our-story/", "/whats-new/", "/visit/", "/contact/")
EXPECTED_VERSION = "20260907-dock-v8-typography"
EXPECTED_LABELS = (
    "A (Main Street Classic)",
    "B (Candy Counter Energy)",
    "C (Curated Nostalgia)",
)


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
            assert (
                f'class="preview-design is-active" '
                f'href="{VARIANT_DOMAINS[variant]}{route}" aria-current="page"'
            ) in html
            labels = re.findall(r'<a\b[^>]*>(.*?)</a>', html)
            labels = tuple(re.sub(r'<[^>]+>', '', label) for label in labels)
            assert labels == EXPECTED_LABELS, (variant, route, labels)


def assert_dock_typography():
    assert ASSET_VERSION == EXPECTED_VERSION
    for variant in VARIANT_DOMAINS:
        css = (ROOT / "variants" / f"{variant}.css").read_text()
        deployed = (ROOT / "variants" / variant / "styles.css").read_text()
        assert css == deployed, (variant, "stale deployment stylesheet")
        rules = dict(re.findall(r'([^{}]+)\{([^{}]*)\}', css))
        rules = {selector.strip(): body for selector, body in rules.items()}
        reset = rules[".preview-dock, .preview-dock *"]
        for declaration in ("font:inherit;", "letter-spacing:normal;", "text-transform:none;"):
            assert declaration in re.sub(r'\s+', '', reset), (variant, declaration)
        root = re.sub(r'\s+', '', rules[".preview-dock"])
        assert "font:50011px/1.2system-ui,sans-serif;" in root, variant
        assert "height:34px;" in root, variant
        chip = re.sub(r'\s+', '', rules[".preview-design"])
        for declaration in ("min-width:44px;", "min-height:28px;", "height:28px;"):
            assert declaration in chip, (variant, declaration)


def assert_committed_artifacts():
    for variant in VARIANT_DOMAINS:
        for route in ROUTES:
            path = ROOT / "variants" / variant / route.strip("/") / "index.html"
            if route == "/":
                path = ROOT / "variants" / variant / "index.html"
            html = path.read_text()
            assert preview_dock(variant, route) in html, (variant, route)
            assert 'name="robots" content="noindex, nofollow"' in html
            assert f'styles.css?v={EXPECTED_VERSION}' in html, (variant, route)
            if route == "/contact/":
                assert "Contact Calico Charlie" in html
                assert 'href="tel:' in html
                assert "Call (419) 701-1585" in html


if __name__ == "__main__":
    assert_route_normalization()
    assert_dock_links()
    assert_dock_typography()
    assert_committed_artifacts()
    print("verified v8 dock typography in 3 variants, exact chip labels, canonical routes, and 18 committed artifacts")

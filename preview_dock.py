"""Shared A/B/C comparison pill for the Calico Charlie's preview."""

from html import escape

VARIANT_DOMAINS = {
    "a": "https://calicocharlies-a.sololink.cloud",
    "b": "https://calicocharlies-b.sololink.cloud",
    "c": "https://calicocharlies-c.sololink.cloud",
}
VARIANT_NAMES = {
    "a": ("A", "Main Street Classic"),
    "b": ("B", "Candy Counter Energy"),
    "c": ("C", "Curated Nostalgia"),
}
ASSET_VERSION = "20260907-dock-v8-typography"


def route_path(slug):
    """Return one canonical trailing-slash path for a generated route slug."""
    normalized = slug.strip("/") if slug else ""
    return "/" if not normalized else f"/{normalized}/"


def preview_dock(variant, slug):
    """Render the floating, route-preserving comparison pill."""
    route = route_path(slug)
    links = []
    for key, domain in VARIANT_DOMAINS.items():
        code, name = VARIANT_NAMES[key]
        active = " is-active" if key == variant else ""
        current = ' aria-current="page"' if key == variant else ""
        label = escape(f"Design {code}: {name}", quote=True)
        links.append(
            f'<a class="preview-design{active}" href="{domain}{route}"{current} '
            f'title="{label}" aria-label="{label}">'
            f'<span class="preview-design-code" aria-hidden="true">{code}</span> '
            f'<strong>({escape(name)})</strong></a>'
        )
    return f'''<aside class="preview-dock" aria-label="Calico Charlie's preview comparison">
  <div class="preview-dock-scroll">
    <nav class="preview-designs" aria-label="Preview designs">
      <span class="preview-group-label">DESIGN:</span>
      {"".join(links)}
    </nav>
  </div>
</aside>'''

# Calico Charlie's Preview

Three-variant website preview for Calico Charlie's Candy & More (Fostoria, OH).

| Variant | Directory | Theme | Coolify resource | URL |
|---|---|---|---|---|
| A | `variants/a` + `variants/a.css` | Main Street Classic | calicocharlies-a | https://calicocharlies-a.sololink.cloud |
| B | `variants/b` + `variants/b.css` | Candy Counter Energy | calicocharlies-b | https://calicocharlies-b.sololink.cloud |
| C | `variants/c` + `variants/c.css` | Curated Nostalgia | calicocharlies-c | https://calicocharlies-c.sololink.cloud |

Routes per variant: `/`, `/treats-gifts/`, `/our-story/`, `/whats-new/`, `/visit/`.

Build: `python3 build.py` renders static HTML into `/tmp/cc/site` (assets shared at site root).
All routes are `noindex, nofollow`. All resources deploy from `main`.

## Preview comparison pill

Every generated page includes the shared A/B/C comparison pill. Links preserve the current route on each deployed sibling domain, and the active design uses `aria-current="page"`. The internal v7 pill is 34px high with 28px chips, dark charcoal (`#252525`) chrome, brand red (`#BC2026`) active chips, horizontal scrolling on narrow screens, visible keyboard focus, reduced-motion support, and 64px page clearance above the bottom safe area. Stylesheets are linked with `?v=20260907-dock-v7-pill-slim`; this preview has no approved alternate palette, so no palette control is rendered.

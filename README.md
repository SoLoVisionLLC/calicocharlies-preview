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

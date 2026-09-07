#!/usr/bin/env python3
"""Build Calico Charlie's Candy & More preview: variants A/B/C, static HTML, 5 routes each."""
import os, shutil
from preview_dock import ASSET_VERSION, preview_dock

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = '/tmp/cc/site'
DEPLOY_ROOT = f'{ROOT}/variants'
ROUTES = {
    '/': 'index.html',
    '/treats-gifts': 'treats-gifts/index.html',
    '/our-story': 'our-story/index.html',
    '/whats-new': 'whats-new/index.html',
    '/visit': 'visit/index.html',
}

NAV_LINKS = [
    ('/', 'Home'),
    ('/treats-gifts', 'Treats &amp; Gifts'),
    ('/our-story', 'Our Story'),
    ('/whats-new', "What&rsquo;s New"),
    ('/visit', 'Visit'),
]

ADDRESS = '206 S. Main St., Fostoria, OH 44830'
PHONE_DISPLAY = '(419) 701-1585'
PHONE_TEL = '+14197011585'
FB = 'https://www.facebook.com/CalicoCharlie'
IG = 'https://www.instagram.com/calicocharlie/'
MAPS_DIR = 'https://www.google.com/maps/dir/?api=1&destination=206+S.+Main+St.%2C+Fostoria%2C+OH+44830'

Q_KIDS = '&ldquo;We need something in town for kids, a candy store!&rdquo;'
Q_FARMERS = '&ldquo;We love working with local farmers and small businesses, it keeps us connected and gives our customers a real taste of home.&rdquo;'
Q_EXPECT = '&ldquo;But we opened a candy store. We expect joy and excitement. That&rsquo;s what this place is for.&rdquo;'
Q_JOY = '&ldquo;It&rsquo;s not just about candy. It&rsquo;s about bringing people together and reminding them that joy still lives right here in our hometown.&rdquo;'
ATTR = '<cite>Kristin VanCuren Koester, owner</cite>'
CATEGORIES = ['Vintage &amp; Retro Candy', 'Handcrafted Treats', 'Premium Popcorn', 'Gifts &amp; Local Finds']

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} | Calico Charlie's Candy &amp; More</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/jpeg" href="/assets/fb-profile-avatar.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={fontq}&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css?v={ASSET_VERSION}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
__NAV__
<main id="main">"""

FOOT = """
</main>
<footer class="footer">
  <div class="foot-inner">
    <div>
      <p class="foot-name"><img src="/assets/fb-profile-avatar.jpg" alt="Calico Charlie's profile mark" class="foot-mark"> Calico Charlie&rsquo;s Candy &amp; More</p>
      <p>{addr}</p>
      <p><a href="tel:{tel}">{phoned}</a></p>
      <p>Call or message us for today&rsquo;s hours.</p>
    </div>
    <nav aria-label="Footer">
      {footlinks}
    </nav>
    <div>
      <p><a href="{fb}" rel="noopener">Follow on Facebook</a></p>
      <p><a href="{ig}" rel="noopener">Follow on Instagram</a></p>
      <p><a href="{maps}" rel="noopener">Get Directions</a></p>
    </div>
  </div>
</footer>
<script>/* static site */</script>
</body>
</html>
"""


def nav(active):
    links = ''.join(
        ('<a href="%s" aria-current="page">%s</a>' % (h, t)) if h == active else f'<a href="{h}">{t}</a>'
        for h, t in NAV_LINKS)
    return f"""
<header class="hdr"><div class="hdr-in">
<a class="brand" href="/"><span class="brand-mark">CC</span><span class="brand-name">Calico Charlie&rsquo;s</span></a>
<input type="checkbox" id="m{active.replace('/', '')}" class="menu-toggle" aria-label="Menu">
<label class="menu-btn" for="m{active.replace('/', '')}"><span class="menu-btn-bar"></span>Menu</label>
<nav class="links" aria-label="Primary">{links}</nav>
</div></header>"""


def foot():
    fl = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV_LINKS)
    return FOOT.format(addr=ADDRESS, tel=PHONE_TEL, phoned=PHONE_DISPLAY,
                       fb=FB, ig=IG, maps=MAPS_DIR, footlinks=fl)


def page(v, slug, title, desc, body):
    css = open(f'{ROOT}/variants/{v}.css').read()
    fonts = {'a': ('Fraunces:opsz,wght@9..144,600;9..144,700|Source+Sans+3:wght@400;600',
                   'Fraunces&quot;,serif|Source Sans'),
             }
    return HEAD.format(title=title, desc=desc, css=css,
                       fontq=FONTS[v], ASSET_VERSION=ASSET_VERSION).replace('__NAV__', nav(slug)) + body + preview_dock(v, slug) + foot()


FONTS = {
    'a': 'Fraunces:opsz,wght@9..144,600%3B9..144,700|Source+Sans+3:wght@400%3B600',
    'b': 'Archivo:wght@500%3B700%3B900|Inter:wght@400%3B600',
    'c': 'Bebas+Neue|Zilla+Slab:wght@500%3B600|Newsreader:opsz,wght@6..72,400%3B6..72,600',
}


# ---------------- shared fragments ----------------

def cat_grid(cls):
    items = ''.join(f'<li class="cat {cls}-cat{i+1}"><h3>{c}</h3></li>'
                    for i, c in enumerate(CATEGORIES))
    return f'<ul class="cats {cls}">{items}</ul>'


VISIT_STRIP = f"""
<section class="visit-strip" aria-labelledby="vs-h">
  <h2 id="vs-h">Plan Your Visit</h2>
  <p>{ADDRESS}</p>
  <p><a class="cta cta-secondary" href="tel:{PHONE_TEL}">Call the Shop</a>
     <a class="cta cta-ghost" href="{MAPS_DIR}" rel="noopener">Get Directions</a></p>
</section>"""


def story_body(img_variant_note=''):
    return f"""
<section class="page-head">
<h1>Our Story</h1>
<p>A hometown candy shop built by Kristin and Matt Koester &mdash; named for Fostoria itself.</p>
</section>
<figure class="story-figure">
<img src="/assets/owner-store.jpg" width="1600" height="900"
 alt="Owners Kristin and Matt Koester behind the counter at Calico Charlie&rsquo;s Candy &amp; More, surrounded by shelves of gifts and treats">
<figcaption>Kristin and Matt Koester behind the counter. Photo: Seneca County Chamber coverage of Calico Charlie&rsquo;s.</figcaption>
</figure>
<blockquote class="big-quote">{Q_JOY}{ATTR}</blockquote>
<section class="prose">
<h2>A childhood dream, opened with joy</h2>
<p>Kristin&rsquo;s idea began with a simple thought: {Q_KIDS} After years of working with preschoolers, she and her husband Matt turned that wish into a shop on South Main Street.</p>
<p>{Q_EXPECT}{ATTR}</p>
<h2>Why &ldquo;Calico Charlie&rsquo;s&rdquo;?</h2>
<p>The name honors Charles Foster, Fostoria&rsquo;s namesake and a former governor of Ohio, whose nickname was &ldquo;Calico Charlie.&rdquo; Kristin embraced the story for its colorful spirit.</p>
<h2>Pieces of Fostoria inside</h2>
<p>The shop itself carries local history: shelving from a long-closed hardware store, chandeliers from the church Kristin grew up attending, and a cart from an old five-and-dime &mdash; donated or discovered by locals who recognized the care behind Calico Charlie&rsquo;s.</p>
</section>
{VISIT_STRIP}"""


def treats_body():
    cats = ''.join(f'<section class="module"><h2>{c}</h2>'
                   f'<p>A discovery corner of the shop &mdash; ask what&rsquo;s out on the counter today.</p></section>'
                   for c in CATEGORIES)
    return f"""
<section class="page-head">
<h1>Treats &amp; Gifts</h1>
<p>Wander the aisles and see what you find &mdash; every visit is a little treasure hunt.</p>
</section>
<p class="note">Selection changes often &mdash; stop in to see what&rsquo;s on the counter today.</p>
<div class="modules">{cats}</div>
<section class="local-band">
<h2>A real taste of home</h2>
<p>Look for Premium Popcorn from Buckeye Family Farms &mdash; a local farm partner listed among Calico Charlie&rsquo;s retail locations.</p>
<blockquote>{Q_FARMERS}{ATTR}</blockquote>
</section>
<section class="close-cta">
<a class="cta cta-primary" href="/visit">Plan Your Visit</a>
</section>"""


def whatsnew_body():
    return f"""
<section class="page-head">
<h1>What&rsquo;s New</h1>
<p>The fastest way to hear about fresh treats and seasonal displays is straight from the shop.</p>
</section>
<section class="follow-panel">
<h2>Follow along</h2>
<p>New goodies, seasonal displays, and shop moments show up first on our social pages:</p>
<p><a class="cta cta-primary" href="{FB}" rel="noopener">Follow on Facebook</a>
   <a class="cta cta-secondary" href="{IG}" rel="noopener">Follow on Instagram</a></p>
<p class="note">Or call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> and ask what&rsquo;s new this week.</p>
</section>
{VISIT_STRIP}"""


def visit_body():
    return f"""
<section class="page-head">
<h1>Visit</h1>
<p>Find us on Main Street in downtown Fostoria.</p>
</section>
<section class="visit-card">
<h2>{ADDRESS}</h2>
<p><a class="cta cta-primary" href="tel:{PHONE_TEL}">Call the Shop</a>
   <a class="cta cta-secondary" href="{MAPS_DIR}" rel="noopener">Get Directions</a></p>
<p>Call or message us for today&rsquo;s hours.</p>
<p><a href="{FB}" rel="noopener">Facebook</a> &middot; <a href="{IG}" rel="noopener">Instagram</a></p>
<p class="map-link"><a href="{MAPS_DIR}" rel="noopener">Open map &amp; directions &rarr;</a></p>
</section>
<section class="map-embed">
<iframe title="Map to Calico Charlie's Candy &amp; More" src="https://www.google.com/maps?q=206+S.+Main+St.,+Fostoria,+OH+44830&amp;output=embed" loading="lazy"></iframe>
</section>"""


HOME_A = f"""
<section class="hero split">
<div class="hero-copy">
<p class="kicker">Downtown Fostoria, Ohio</p>
<h1>Candy, gifts, and a little hometown joy</h1>
<p class="lede">{Q_KIDS}</p>
<p><a class="cta cta-primary" href="/visit">Plan Your Visit</a>
<a class="cta cta-ghost" href="/whats-new">See What&rsquo;s New</a></p>
</div>
<figure class="hero-media r43">
<img src="/assets/cover.jpg" width="1200" height="1008" alt="Inside Calico Charlie&rsquo;s: chocolates, an engraved wooden sign, and the historic Foster Block building">
</figure>
</section>
<section aria-labelledby="disc-h">
<h2 id="disc-h">Wander and discover</h2>
{cat_grid('rail')}
</section>
<section class="history-panel">
<figure><img src="/assets/owner-store.jpg" width="800" height="450" alt="Kristin and Matt Koester behind the counter at Calico Charlie&rsquo;s"></figure>
<div>
<h2>A shop named for Fostoria itself</h2>
<p>&ldquo;Calico Charlie&rdquo; was the nickname of Charles Foster, the former Ohio governor Fostoria is named after. Inside the shop, shelving, chandeliers, and a five-and-dime cart carry pieces of local history.</p>
<a class="textlink" href="/our-story">Discover the Story</a>
</div>
</section>
<section class="quote-band">
<blockquote>{Q_JOY}<br>{ATTR}</blockquote>
</section>
{VISIT_STRIP}"""

HOME_B = f"""
<section class="hero-typo">
<p class="kicker">206 S. Main St. &middot; Fostoria</p>
<h1>Sweet finds.<br>Hometown pride.<br>Zero pretense.</h1>
<p><a class="cta cta-primary" href="/visit">Plan Your Visit</a></p>
</section>
<section class="band band-media">
<figure><img src="/assets/food-small.jpg" width="412" height="412" alt="Wrapped caramels from Calico Charlie&rsquo;s"></figure>
</section>
<section class="band band-cats" aria-labelledby="dc-h">
<h2 id="dc-h">Four corners of discovery</h2>
{cat_grid('grid')}
</section>
<section class="band band-visit">
<h2>Swing by Main Street</h2>
<p>{ADDRESS} &middot; <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
<p><a class="cta cta-light" href="{MAPS_DIR}" rel="noopener">Get Directions</a></p>
</section>
<section class="band band-farm">
<h2>Popped local</h2>
<p>Look for Buckeye Family Farms Premium Popcorn &mdash; a local farm partner.</p>
<blockquote>{Q_FARMERS}</blockquote>
</section>
<section class="band band-quote" aria-label="Owner quote">
<p>{Q_EXPECT}</p>
<span>{ATTR}</span>
</section>
<section class="band band-new">
<h2>See what&rsquo;s new</h2>
<p><a class="cta cta-dark" href="/whats-new">See What&rsquo;s New</a></p>
</section>
<section class="visit-strip">
<h2>Plan Your Visit</h2>
<p>{ADDRESS}</p>
<p><a class="cta cta-secondary" href="/visit">Plan Your Visit</a></p>
</section>"""

HOME_C = f"""
<section class="collage-hero">
<figure class="c1 rot-neg"><img src="/assets/cover.jpg" width="900" height="756" alt="Chocolates, an engraved sign, and the Foster Block building"></figure>
<figure class="c2 rot-pos"><img src="/assets/food-small.jpg" width="360" height="360" alt="A pile of wrapped caramels"></figure>
<blockquote class="oversized">&ldquo;We expect joy and excitement. That&rsquo;s what this place is for.&rdquo;<cite>Kristin VanCuren Koester, owner</cite></blockquote>
<p class="collage-cta"><a class="cta cta-primary" href="/visit">Plan Your Visit</a></p>
</section>
<section class="fragments">
<h1 class="frag-title">Calico Charlie&rsquo;s Candy &amp; More</h1>
<article class="frag"><h2>The name</h2><p>Fostoria&rsquo;s namesake, Charles Foster, was nicknamed &ldquo;Calico Charlie.&rdquo;</p></article>
<article class="frag"><h2>The dream</h2><p>{Q_KIDS}</p></article>
<article class="frag"><h2>The roots</h2><p>Shelving from an old hardware store. Chandeliers from a childhood church. A five-and-dime cart.</p></article>
</section>
<section class="treats-index" aria-labelledby="ti-h">
<h2 id="ti-h">The treats index</h2>
<ul class="idx">
{''.join(f'<li><a href="/treats-gifts">{c}</a></li>' for c in CATEGORIES)}
</ul>
</section>
<section class="roots-spread">
<figure><img src="/assets/owner-store.jpg" width="900" height="506" alt="Kristin and Matt Koester behind the counter"></figure>
<div>
<h2>Built by Kristin &amp; Matt</h2>
<p>{Q_FARMERS}</p>
<a class="textlink" href="/our-story">Discover the Story</a>
</div>
</section>
<section class="practical-card">
<h2>Practical bits</h2>
<p>{ADDRESS}<br><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
<p>Call or message us for today&rsquo;s hours.</p>
<p><a class="cta cta-primary" href="/visit">Plan Your Visit</a></p>
</section>
<section class="social-footer-note">
<p><a href="{FB}" rel="noopener">Facebook</a> &middot; <a href="{IG}" rel="noopener">Instagram</a> &middot; <a href="/whats-new">What&rsquo;s New</a></p>
</section>"""


HOMES = {'a': HOME_A, 'b': HOME_B, 'c': HOME_C}
DESC_HOME = "Vintage and retro candy, handcrafted treats, premium popcorn, and local gifts in downtown Fostoria, Ohio."


def build():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(f'{SITE}/assets', exist_ok=True)
    shutil.rmtree(f'{SITE}/assets', ignore_errors=True)
    shutil.copytree(f'{ROOT}/assets', f'{SITE}/assets')
    for v in ('a', 'b', 'c'):
        base = f'{SITE}/{v}'
        os.makedirs(base, exist_ok=True)
        shutil.copyfile(f'{ROOT}/variants/{v}.css', f'{base}/styles.css')
        for route, fname in ROUTES.items():
            d = os.path.join(base, route.lstrip('/'))
            os.makedirs(d, exist_ok=True)
        bodies = {
            '/': HOMES[v],
            '/treats-gifts': treats_body(),
            '/our-story': story_body(),
            '/whats-new': whatsnew_body(),
            '/visit': visit_body(),
        }
        titles = {'/': '', '/treats-gifts': 'Treats & Gifts',
                  '/our-story': 'Our Story', '/whats-new': "What's New",
                  '/visit': 'Visit'}
        for route, body in bodies.items():
            html = page(v, route, titles[route], DESC_HOME, body)
            with open(os.path.join(base, route.lstrip('/'), 'index.html'), 'w') as f:
                f.write(html)
        # Keep the committed Docker build context in lockstep with the generated
        # site. Each Coolify service copies its variant directory directly, so
        # generating only /tmp/cc/site leaves production artifacts stale.
        deploy = f'{DEPLOY_ROOT}/{v}'
        for name in os.listdir(deploy):
            path = os.path.join(deploy, name)
            if os.path.isdir(path) and name != '.git':
                shutil.rmtree(path)
            elif name != 'Dockerfile':
                os.remove(path)
        for name in os.listdir(base):
            source = os.path.join(base, name)
            target = os.path.join(deploy, name)
            if os.path.isdir(source):
                shutil.copytree(source, target)
            else:
                shutil.copyfile(source, target)
    print('built', SITE)


if __name__ == '__main__':
    build()

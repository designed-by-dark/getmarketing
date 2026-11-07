#!/usr/bin/env python3
"""Give the hand-built pages (partners, press, legal) the homepage look:
homepage nav + footer, homepage CSS stack, lead form on the sales pages."""
import re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_seo_pages as B
ROOT = B.ROOT
PAGES = {  # file: (lang, counterpart, kind)
 "partners/index.html": ("en", "/de/partners/", "sales"), "de/partners/index.html": ("de", "/partners/", "sales"),
 "press/index.html": ("en", "/de/presse/", "sales"), "de/presse/index.html": ("de", "/press/", "sales"),
 "impressum.html": ("de", "/impressum-en.html", "legal"), "impressum-en.html": ("en", "/impressum.html", "legal"),
 "datenschutz.html": ("de", "/datenschutz-en.html", "legal"), "datenschutz-en.html": ("en", "/datenschutz.html", "legal"),
}
CSS = ('<link rel="stylesheet" href="/home.css?v=1" />\n<link rel="stylesheet" href="/home-hero.css?v=14" />\n'
       '<link rel="stylesheet" href="/theme.css?v=18" />\n<link rel="stylesheet" href="/landing.css?v=1" />\n<link rel="stylesheet" href="/subpage.css?v=2" />')
FONT = '<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400..800&display=swap" rel="stylesheet" />'

def lead_and_mission(lang):
    secs = B.home_parts(lang)["sections"]
    out = [re.search(r'<section id="start" class="lead-section">.*?</section>', secs, re.S).group(0)]
    return "\n\n".join(out)

for rel, (lang, alt, kind) in PAGES.items():
    f = ROOT / rel; s = f.read_text()
    s = re.sub(r'<link href="https://fonts.googleapis.com/css2\?family=Geist[^>]*>', FONT, s)
    s = re.sub(r'<link rel="stylesheet" href="/site.css\?v=\d+" />', CSS, s)
    s = s.replace('<script defer src="/nav-menu.js', '<script defer src="/site.js?v=1"></script>\n<script defer src="/nav-menu.js', 1) if "/site.js" not in s else s
    s = re.sub(r"<nav>.*?</nav>", lambda m: B.nav_for(lang, alt).replace('href="#', f'href="{B.T[lang]["home"]}#'), s, count=1, flags=re.S)
    foot = B.home_parts(lang)["footer"].replace('href="#', f'href="{B.T[lang]["home"]}#')
    foot = re.sub(r'(<div class="ft-legal">.*?)<a href="/(de/)?"( id="switch-en-foot")?>(Deutsch|English)</a>', lambda m: m.group(1) + f'<a href="{alt}">{m.group(4)}</a>', foot, flags=re.S)
    s = re.sub(r'<footer class="ft">.*?</footer>', lambda m: foot, s, count=1, flags=re.S)
    s = re.sub(r"\n<script>\n  const io = new IntersectionObserver.*?</script>\n", "\n", s, flags=re.S)
    s = s.replace('<header class="hero">', '<header class="hero hero-light sp-hero2">', 1)
    if kind == "legal" and "legal-hero" not in s:
        h1 = re.search(r'<main class="legal">\s*<div class="wrap">\s*<h1>(.*?)</h1>', s, re.S)
        if h1:
            s = s.replace(h1.group(0), f'<header class="hero hero-light legal-hero"><div class="wrap"><h1>{h1.group(1)}</h1></div></header>\n<main class="legal">\n  <div class="wrap">', 1)
    if kind == "sales":
        s = re.sub(r'\n<!-- lead\+mission -->.*?<!-- /lead\+mission -->\n', "\n", s, flags=re.S)
        s = s.replace('<footer class="ft">', f'<!-- lead+mission -->\n{lead_and_mission(lang)}\n<!-- /lead+mission -->\n\n<footer class="ft">', 1)
    s = s.replace('<body>', '<body class="sub-page">', 1) if 'class="sub-page"' not in s else s
    f.write_text(s); print("restyled", rel)

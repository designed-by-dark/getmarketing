#!/usr/bin/env python3
"""Build the topic pages from _content/*.md.

  python3 _tools/build_seo_pages.py

- Every markdown file becomes /<slug>/index.html (slug = file name).
- marketing-plan-generator.md and marketingplan-erstellen.md are tool pages that already exist:
  their text goes into the page's SEO section, and title/description are updated.
- Also writes sitemap.xml and robots.txt.
Markdown format: first lines "TITLE: ..." and "DESCRIPTION: ...", then "# H1", intro, "[ Button ]" lines.
"""
import html, json, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_content"
SITE = "https://getmarketing.team"
TOOL_PAGES = {"marketing-plan-generator", "marketingplan-erstellen"}
# German slug -> English slug. Every topic exists in both languages.
PAIRS = {"ki-marketing-agentur": "ai-marketing-agency", "ki-marketing-manager": "ai-marketing-manager", "ki-seo-tool": "ai-seo-tool",
         "marketing-automatisierung": "marketing-automation", "marketing-ki": "ai-in-marketing", "b2b-leadgenerierung": "b2b-lead-generation",
         "marketing-fuer-kleine-unternehmen": "marketing-for-small-businesses", "marketingplan-erstellen": "marketing-plan-generator",
         "ki-cmo": "ai-cmo", "virtueller-cmo": "virtual-cmo", "ki-marketingteam": "ai-marketing-team",
         "ki-marketing-automatisierung": "ai-marketing-automation", "marketing-auslagern": "done-for-you-marketing",
         "seo-automatisieren": "automate-seo", "ki-blogartikel-schreiben": "ai-blog-writing", "saas-marketing": "marketing-for-saas",
         "b2b-leadgenerierung-strategien": "b2b-lead-generation-strategies", "linkedin-leadgenerierung-b2b": "b2b-linkedin-lead-generation"}
DE_SLUGS = set(PAIRS)
# Short names for breadcrumbs, related cards and footers, where the title is too long to shorten automatically
SHORT = {"ai-blog-writing": "AI Blog Writing", "ai-marketing-automation": "AI Marketing Automation", "ai-marketing-team": "AI Marketing Team",
         "b2b-lead-generation-strategies": "B2B Lead Generation Strategies", "virtual-cmo": "Virtual CMO",
         "b2b-leadgenerierung-strategien": "B2B-Leadgenerierung: Strategien", "ki-blogartikel-schreiben": "KI-Blogartikel",
         "ki-marketing-automatisierung": "KI-Marketing-Automatisierung", "ki-marketingteam": "KI-Marketingteam", "virtueller-cmo": "Virtueller CMO"}

ALT = {**PAIRS, **{en: de for de, en in PAIRS.items()}}
TODAY = datetime.date.today().isoformat()
BOLT = '<svg viewBox="0 0 100 150" aria-hidden="true"><path d="M62 0 8 86h36L30 150 92 58H56z"/></svg>'

T = {
 "en": dict(home="/", start="/#start", plan="/marketing-plan-generator/", lang_href="/de/", lang_label="DE",
            nav=[("/#how-it-works", "How it works"), ("/#results", "Results"), ("/#diff", "Compare"), ("/partners/", "Partners"), ("/marketing-plan-generator/", "Marketing plan")],
            cta="Try it now", diag="Book a diagnosis", plan_cta="Generate my marketing plan", crumb_home="Home",
            band_h="Your AI marketing team <span>brings the customers.</span>", band_p="You approve. Everything else runs in the background.",
            related="More on this topic", faq_words=("frequently", "faq", "questions"),
            ft_tag="Marketing you no longer have to worry about", ft_desc="A team of AI agents that plans, runs and measures your marketing. Built for small and mid-sized companies across Europe.",
            ft_prod="Product", ft_topics="Topics", ft_contact="Contact", ft_start="Get started",
            legal=[("/impressum-en.html", "Legal Notice"), ("/datenschutz-en.html", "Privacy Policy"), ("/de/", "Deutsch")], city="Berlin, Germany"),
 "de": dict(home="/de/", start="/de/#start", plan="/marketingplan-erstellen/", lang_href="/", lang_label="EN",
            nav=[("/de/#so-funktionierts", "So funktioniert's"), ("/de/#ergebnisse", "Ergebnisse"), ("/de/#diff", "Vergleich"), ("/de/partners/", "Partner"), ("/marketingplan-erstellen/", "Marketingplan")],
            cta="Jetzt testen", diag="Diagnose anfragen", plan_cta="Marketingplan erstellen", crumb_home="Start",
            band_h="Dein KI-Marketingteam <span>bringt die Kunden.</span>", band_p="Du gibst frei. Alles andere läuft im Hintergrund.",
            related="Mehr zum Thema", faq_words=("häufige fragen", "faq", "fragen"),
            ft_tag="Marketing, um das du dich nicht mehr kümmern musst", ft_desc="Ein Team aus KI-Agenten, das dein Marketing plant, umsetzt und misst. Für kleine und mittlere Unternehmen in Europa.",
            ft_prod="Produkt", ft_topics="Themen", ft_contact="Kontakt", ft_start="Jetzt starten",
            legal=[("/impressum.html", "Impressum"), ("/datenschutz.html", "Datenschutz"), ("/", "English")], city="Berlin, Deutschland"),
}

def esc(s): return html.escape(s, quote=True)
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    return s
def plain(s): return re.sub(r"\*\*|__", "", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s))

def cta_buttons(line, lang, ghost_second=True):
    t = T[lang]; labels = re.findall(r"\[\s*([^\]]+?)\s*\]", line)
    notes = [p.strip() for p in re.sub(r"\[[^\]]*\]", "", line).split("·") if p.strip() and not re.fullmatch(r"(or|oder)?\s*(for|für)?\s*(Enterprise)?", p.strip(), re.I)]
    btns = []
    for i, l in enumerate(labels):
        low = l.lower()
        if "diagnos" in low: href, text = t["start"], t["diag"]
        elif "plan" in low: href, text = t["plan"], t["plan_cta"]
        else: href, text = t["start"], t["cta"]
        cls = "btn-ghost" if (i and ghost_second) else "btn-lime"
        btns.append(f'<a href="{href}" class="{cls}">{esc(text)}</a>')
    return btns, notes

def parse(md):
    lines = md.split("\n"); meta = {}
    while lines and re.match(r"^(TITLE|DESCRIPTION):", lines[0]):
        k, v = lines.pop(0).split(":", 1); meta[k.lower()] = v.strip()
    blocks, i = [], 0
    while i < len(lines):
        l = lines[i]
        if not l.strip(): i += 1; continue
        m = re.match(r"^(#{1,3})\s+(.*)", l)
        if m: blocks.append(("h%d" % len(m.group(1)), m.group(2).strip())); i += 1; continue
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[\s\-:|]+\|$", lines[i]): rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append(("table", rows)); continue
        if re.match(r"^(- |\d+\. )", l):
            ordered = bool(re.match(r"^\d+\. ", l)); items = []
            while i < len(lines) and re.match(r"^(- |\d+\. )", lines[i]):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[i])); i += 1
            blocks.append(("ol" if ordered else "ul", items)); continue
        if re.match(r"^\[\s*[^\]]+\]", l): blocks.append(("cta", l)); i += 1; continue
        para = [l]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||- |\d+\. |\[)", lines[i]):
            para.append(lines[i]); i += 1
        blocks.append(("p", para))
    return meta, blocks

def faq_pairs(blocks):
    """FAQ items: '**Q?**' line + answer lines in one paragraph, or '### Q' + paragraphs."""
    out, cur = [], None
    for kind, val in blocks:
        if kind == "h3": cur = [val, []]; out.append(cur); continue
        if kind == "p" and re.match(r"^\*\*.+\*\*$", val[0].strip()):
            cur = [val[0].strip().strip("*").strip(), [" ".join(val[1:])] if len(val) > 1 else []]; out.append(cur); continue
        if cur is not None:
            if kind == "p": cur[1].append(" ".join(val))
            elif kind in ("ul", "ol"): cur[1].append(" ".join(val))
    return [(q, [a for a in ans if a]) for q, ans in out if ans]

def render_blocks(blocks, lang, faq_collect):
    out, i = [], 0
    while i < len(blocks):
        kind, val = blocks[i]
        if kind == "h2":
            out.append(f"<h2>{inline(val)}</h2>")
            if any(w in val.lower() for w in T[lang]["faq_words"]):
                j = i + 1
                while j < len(blocks) and blocks[j][0] != "h2": j += 1
                pairs = faq_pairs(blocks[i + 1:j])
                if pairs:
                    faq_collect.extend(pairs)
                    out.append('<div class="sp-faq">' + "".join(
                        f'<details{" open" if k == 0 else ""}><summary>{inline(q)}</summary>' + "".join(f"<p>{inline(a)}</p>" for a in ans) + "</details>"
                        for k, (q, ans) in enumerate(pairs)) + "</div>")
                    i = j; continue
        elif kind == "h3": out.append(f"<h3>{inline(val)}</h3>")
        elif kind == "p":
            text = " ".join(val)
            tail = re.search(r"\s*(\[\s*[^\]]+\])\s*$", text)
            if tail and not text.rstrip().endswith(")"):
                b, _ = cta_buttons(tail.group(1), lang)
                out.append(f'<div class="sp-inline-cta"><p>{inline(text[:tail.start()])}</p>{b[0]}</div>'); i += 1; continue
            q =re.match(r'^[„"“](.+?)[“"”]\s*(.*)$', text)
            if q and len(text) < 260: out.append(f'<blockquote class="sp-quote">„{inline(q.group(1))}“<span>{inline(q.group(2))}</span></blockquote>' if lang == "de" else f'<blockquote class="sp-quote">“{inline(q.group(1))}”<span>{inline(q.group(2))}</span></blockquote>')
            else: out.append(f"<p>{inline(text)}</p>")
        elif kind in ("ul", "ol"): out.append(f"<{kind}>" + "".join(f"<li>{inline(x)}</li>" for x in val) + f"</{kind}>")
        elif kind == "table":
            head, *rows = val
            out.append('<div class="sp-table"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>" +
                       "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
        elif kind == "cta":
            btns, notes = cta_buttons(val, lang)
            out.append(f'<div class="sp-inline-cta"><p>{esc(" · ".join(notes)) if notes else T[lang]["band_p"]}</p>{btns[0]}</div>')
        i += 1
    return "\n".join(out)

def split_page(blocks):
    """-> h1, intro paragraphs, hero cta line, body blocks, closing (h2, cta) or None"""
    h1 = next(v for k, v in blocks if k == "h1")
    rest = blocks[[k for k, _ in blocks].index("h1") + 1:]
    intro, hero_cta = [], None
    while rest and rest[0][0] in ("p", "cta") and len(intro) < 2:
        k, v = rest.pop(0)
        if k == "cta": hero_cta = v; break
        intro.append(" ".join(v))
    closing = None
    if len(rest) >= 2 and rest[-1][0] == "cta" and rest[-2][0] == "h2":
        closing = (rest[-2][1], rest[-1][1]); rest = rest[:-2]
    return h1, intro, hero_cta, rest, closing

def nav_html(lang, alt=None):
    t = T[lang]
    links = "".join(f'<li><a href="{h}">{esc(x)}</a></li>' for h, x in t["nav"])
    return f'''<nav>
  <div class="wrap nav-inner">
    <a href="{t["home"]}" class="nav-logo"><img src="/logo.jpg" alt="GetMarketing" /><span class="nav-logo-text">GetMarketing</span></a>
    <ul class="nav-links">{links}</ul>
    <a href="{alt or t["lang_href"]}" class="nav-lang">{t["lang_label"]}</a>
    <a href="{t["start"]}" class="nav-cta">{t["cta"]}</a>
  </div>
</nav>'''

def footer_html(lang, pages):
    t = T[lang]
    prod = "".join(f'<li><a href="{h}">{esc(x)}</a></li>' for h, x in t["nav"][:3]) + f'<li><a href="{t["plan"]}">{esc(t["plan_cta"])}</a></li>'
    topics = "".join(f'<li><a href="/{p["slug"]}/">{esc(p["short"])}</a></li>' for p in pages if p["lang"] == lang and p["slug"] not in TOOL_PAGES)
    legal = "".join(f'<a href="{h}">{esc(x)}</a>' for h, x in t["legal"])
    return f'''<footer class="ft">
  <div class="wrap">
    <div class="ft-grid">
      <div class="ft-brand"><a href="{t["home"]}" class="ft-logo"><img src="/logo.jpg" alt="" /><span>GetMarketing</span></a><p class="ft-tag">{esc(t["ft_tag"])}</p><p class="ft-desc">{esc(t["ft_desc"])}</p></div>
      <div class="ft-col"><h4>{t["ft_prod"]}</h4><ul>{prod}</ul></div>
      <div class="ft-col"><h4>{t["ft_topics"]}</h4><ul class="ft-topics-list">{topics}</ul></div>
      <div class="ft-col"><h4>{t["ft_contact"]}</h4><ul><li><a href="mailto:darya@getmarketing.team">darya@getmarketing.team</a></li><li><a href="{t["start"]}">{t["ft_start"]}</a></li><li>{t["city"]}</li></ul></div>
    </div>
    <div class="ft-bottom"><span>© {TODAY[:4]} GetMarketing</span><div class="ft-legal">{legal}</div></div>
  </div>
</footer>'''

def short_title(title, h1):
    s = re.split(r"\s[|:–—]\s|:\s", title)[0].strip()
    return s if len(s) <= 48 else plain(h1)[:48].rsplit(" ", 1)[0]

def build_page(p, pages):
    lang, t = p["lang"], T[p["lang"]]
    h1, intro, hero_cta, body, closing = split_page(p["blocks"])
    btns, notes = cta_buttons(hero_cta, lang) if hero_cta else ([f'<a href="{t["start"]}" class="btn-lime">{t["cta"]}</a>'], [])
    faq = []
    article = render_blocks(body, lang, faq)
    if closing:
        cb, cnotes = cta_buttons(closing[1], lang)
        band = f'<h2>{inline(closing[0])}</h2><p>{t["band_p"]}</p><div class="sp-ctas">{"".join(cb)}</div>'
    else:
        band = f'<h2>{t["band_h"]}</h2><p>{t["band_p"]}</p><div class="sp-ctas"><a href="{t["start"]}" class="btn-lime">{t["cta"]}</a><a href="{t["plan"]}" class="btn-ghost">{t["plan_cta"]}</a></div>'
    same = [q for q in pages if q["lang"] == lang and q["slug"] != p["slug"]]
    k = pages.index(p) % max(1, len(same)); rel = (same[k:] + same[:k])[:6]
    related = "".join(f'<a href="/{q["slug"]}/"><b>{esc(q["short"])}</b><span>{esc(q["desc"][:120].rsplit(" ", 1)[0])}…</span></a>' for q in rel)
    url = f'{SITE}/{p["slug"]}/'
    de_s, en_s = (p["slug"], ALT[p["slug"]]) if lang == "de" else (ALT[p["slug"]], p["slug"])
    hreflang = (f'<link rel="alternate" hreflang="de" href="{SITE}/{de_s}/" />\n<link rel="alternate" hreflang="en" href="{SITE}/{en_s}/" />\n'
                f'<link rel="alternate" hreflang="x-default" href="{SITE}/{en_s}/" />')
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": p["title"], "description": p["desc"], "url": url, "inLanguage": lang,
           "dateModified": TODAY, "publisher": {"@type": "Organization", "name": "GetMarketing", "url": SITE, "logo": SITE + "/logo.jpg"}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "GetMarketing", "item": SITE + t["home"]},
              {"@type": "ListItem", "position": 2, "name": p["short"], "item": url}]}]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(" ".join(a))}} for q, a in faq]})
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    intro_html = "".join(f'<p class="sp-intro">{inline(x)}</p>' for x in intro[:1])
    extra_intro = "".join(f"<p>{inline(x)}</p>" for x in intro[1:])
    note = f'<p class="sp-note">{esc(" · ".join(notes))}</p>' if notes else ""
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}" />
<link rel="canonical" href="{url}" />
{hreflang}
<meta property="og:type" content="website" />
<meta property="og:title" content="{esc(p["title"])}" />
<meta property="og:description" content="{esc(p["desc"])}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE}/logo.jpg" />
<meta name="twitter:card" content="summary" />
<link rel="icon" href="/logo.jpg" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400..800&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/seo-page.css?v=2" />
{ld_html}
<script defer src="/analytics.js"></script>
<script defer src="/nav-menu.js?v=2"></script>
</head>
<body>
<!-- generated from _content/{p["file"]} by _tools/build_seo_pages.py, edit the markdown, not this file -->
{nav_html(lang, "/" + ALT[p["slug"]] + "/")}
<header class="sp-hero">
  <div class="wrap">
    <p class="sp-crumbs"><a href="{t["home"]}">{t["crumb_home"]}</a><span>›</span><span>{esc(p["short"])}</span></p>
    <h1>{inline(h1)}</h1>
    {intro_html}
    <div class="sp-ctas">{"".join(btns)}</div>
    {note}
  </div>
</header>
<main class="sp-main">
  <div class="wrap"><article class="sp-article">
{extra_intro}
{article}
  </article></div>
</main>
<section class="sp-band"><div class="wrap">{band}</div></section>
<section class="sp-related"><div class="wrap"><h2>{t["related"]}</h2><div class="sp-rel-grid">{related}</div></div></section>
{footer_html(lang, pages)}
</body>
</html>
'''

TOOL_CSS = """<style>
  .seo-inner ul, .seo-inner ol { margin: 4px 0 20px 1.2em; display: grid; gap: 8px; }
  .seo-inner li { line-height: 1.6; }
  .seo-inner .sp-table { overflow-x: auto; margin: 8px 0 24px; }
  .seo-inner table { width: 100%; border-collapse: collapse; font-size: 15px; }
  .seo-inner th, .seo-inner td { text-align: left; padding: 10px 12px; border-bottom: 1px solid #E6E7E3; vertical-align: top; }
  .seo-inner th { font-weight: 700; }
  .seo-inner .sp-faq details { border-bottom: 1px solid #E6E7E3; padding: 14px 0; }
  .seo-inner .sp-faq summary { cursor: pointer; font-weight: 700; }
  .seo-inner .sp-faq p { margin-top: 8px; }
  .seo-inner .sp-quote { margin: 20px 0; font-weight: 600; }
  .seo-inner .sp-quote span { display: block; font-weight: 400; font-size: 14px; opacity: .7; }
  .seo-inner .sp-inline-cta { display: none; }
</style>"""

def build_tool(p):
    path = ROOT / p["slug"] / "index.html"; s = path.read_text()
    h1, intro, hero_cta, body, closing = split_page(p["blocks"])
    faq = []; article = render_blocks(body, p["lang"], faq)
    s, n = re.subn(r'(<div class="seo-inner">).*?(</div>\s*</div>\s*</section>)', lambda m: m.group(1) + "\n" + article + "\n    " + m.group(2), s, count=1, flags=re.S)
    assert n == 1, p["slug"]
    s = re.sub(r"<title>.*?</title>", f'<title>{esc(p["title"])}</title>', s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(p["desc"]), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(p["title"]), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + esc(p["desc"]), s, count=1)
    s = re.sub(r"\n?<style id=\"seo-text-css\">.*?</style>", "", s, flags=re.S)
    s = s.replace("</head>", TOOL_CSS.replace("<style>", '<style id="seo-text-css">') + "\n</head>", 1)
    if faq and '"FAQPage"' not in s:
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(" ".join(a))}} for q, a in faq]}
        s = s.replace("</head>", f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n</head>', 1)
    path.write_text(s)

def main():
    pages = []
    for f in sorted(SRC.glob("*.md")):
        meta, blocks = parse(f.read_text())
        slug = f.stem; lang = "de" if slug in DE_SLUGS else "en"
        h1 = next(v for k, v in blocks if k == "h1")
        pages.append(dict(file=f.name, slug=slug, lang=lang, blocks=blocks, title=meta.get("title", plain(h1)), desc=meta.get("description", ""), short=SHORT.get(slug) or short_title(meta.get("title", h1), h1)))
    for p in pages:
        if p["slug"] in TOOL_PAGES: build_tool(p); print("tool page", p["slug"]); continue
        out = ROOT / p["slug"] / "index.html"; out.parent.mkdir(exist_ok=True); out.write_text(build_page(p, pages)); print("page", p["slug"])
    urls = ["/", "/de/", "/partners/", "/press/", "/de/presse/", "/de/partners/"] + [f'/{p["slug"]}/' for p in pages]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(len(urls), "urls in sitemap")

if __name__ == "__main__":
    main()

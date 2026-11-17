#!/usr/bin/env python3
"""Use-case landing pages (EN + DE), in the Enterprise page design.

  python3 _tools/usecase_pages.py

Copy lives in _tools/usecase_content.py. Nav, footer and lead form come from the homepage
(via build_static_pages), the layout CSS from enterprise_page. Writes
use-cases/[...]/index.html and de/loesungen/[...]/index.html, adds the URLs to sitemap.xml
and puts the mega menu into every page (nav_usecases.py).
"""
import datetime, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_static_pages as S
import enterprise_page as E
import nav_usecases
from usecase_content import ORDER, SLUG, BASE, MENU, HUB, UC

ROOT = S.ROOT
OTHER = {"en": "de", "de": "en"}

UC_CSS = """<style>
  .uc-find .lp-checks li strong { color: #111; }
  .wf-dark .wf-ai { color: #1B2B22; }
  .uc-hub { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }
  .uc-card { display: flex; flex-direction: column; gap: 10px; background: #fff; border-radius: 24px; padding: 32px; box-shadow: var(--card-shadow); color: inherit; text-decoration: none; transition: transform .15s; }
  .uc-card:hover { transform: translateY(-3px); }
  .uc-card small { font-size: 11.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--forest); }
  .uc-card b { font-size: clamp(24px, 2.2vw, 30px); font-weight: 600; letter-spacing: -0.035em; line-height: 1.1; color: #111; }
  .uc-card p { font-size: 16px; line-height: 1.55; color: #555; }
  .uc-card em { margin-top: auto; font-style: normal; font-weight: 600; color: var(--forest); }
  .uc-card:first-child { background: radial-gradient(420px 220px at 100% 0%, rgba(82,183,136,.35), transparent 70%), var(--deep); }
  .uc-card:first-child small, .uc-card:first-child em { color: var(--lime); }
  .uc-card:first-child b { color: #fff; }
  .uc-card:first-child p { color: rgba(255,255,255,.75); }
  @media (max-width: 800px) { .uc-hub { grid-template-columns: 1fr; } .uc-card { padding: 26px 22px; } }
</style>"""


def url(key, lang):
    return BASE[lang] if key == "hub" else f"{BASE[lang]}{SLUG[key][lang]}/"


def proof(c, lang):
    stats = "".join(f"<div><b>{n}</b><span>{l}</span></div>" for n, l in c["stats"])
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="360"/>' for x in range(0, 1001, 91))
    return (f'<section class="cs-section ent-proof"><div class="wrap"><div class="growth reveal"><div class="g-head"><h2>{c["stats_h"]}</h2>'
            f'<p class="sec-sub">{c["stats_sub"]}</p></div><div class="g-stats">{stats}</div>'
            '<svg class="g-curve" viewBox="0 0 1000 360" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="gFillU" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#52B788" stop-opacity=".22"/><stop offset="1" stop-color="#52B788" stop-opacity="0"/></linearGradient></defs>'
            f'<g class="g-grid">{grid}</g><path class="g-area" d="M0 340 C 420 335, 720 260, 1000 12 L1000 360 L0 360 Z" fill="url(#gFillU)"/>'
            '<path class="g-line" pathLength="1" d="M0 340 C 420 335, 720 260, 1000 12" fill="none"/></svg></div>'
            f'{E.reviews(lang)}</div></section>')


def interest_script(value):
    return ('<script>document.addEventListener("DOMContentLoaded",function(){var s=document.querySelector("#lead-form select[name=interest]");'
            f'if(s)s.value="{value}";}});</script>')


def usecase(key, lang):
    c = UC[key][lang]
    find = S.split(c["find_h"], S.ul(c["find"]), k=c["find_k"], sid="problems").replace('class="lp-sec lp-split"', 'class="lp-sec lp-split uc-find"', 1)
    wf = "".join(f'<article class="wf"><div class="wf-txt"><span class="wf-tag">{t}</span><h3>{h}</h3><p>{p}</p></div>{ui}</article>' for t, h, p, ui in c["wf"])
    workflows = f'<section class="ent-sec" id="workflows"><div class="wrap">{E.head(c["wf_h"], c["wf_sub"])}<div class="wf-grid reveal">{wf}</div></div></section>'
    tl = "".join(f'<div class="tl-step"><i>{n}</i><h3>{t}</h3><p class="tl-p">{p}</p>{S.ul(li, "")}</div>' for n, t, p, li in c["tl"])
    tl_h = "So läuft es ab dem ersten&nbsp;Tag" if lang == "de" else "How it runs from day&nbsp;one"
    steps = f'<section class="ent-sec" id="stages"><div class="wrap">{E.head(tl_h)}<div class="tl reveal">{tl}</div><p class="tl-note">{c["tl_note"]}</p></div></section>'
    cta = (f'<section class="ent-sec"><div class="wrap"><div class="ent-cta reveal"><div><h2>{c["cta_h"]}</h2><p>{c["cta_p"]}</p></div>'
           f'<a href="#start" class="btn-hero" data-interest="{c["interest"]}">{c["btn"]}</a></div></div></section>')
    cmp = S.table(c["cmp_h"], c["cmp_head"], c["cmp"], k=c["cmp_k"])
    body = "\n\n".join([E.ENT_CSS, UC_CSS, find, workflows, proof(c, lang), steps, cta, cmp,
                        S.faq_section(lang, c["faq"], sec_id="faq"), "{LEAD}", interest_script(c["interest"])])
    action = (f'<a href="#start" class="btn-hero" data-interest="partner">{c["btn"]}</a>' if c["interest"] == "partner" else S.form(lang, c["btn"]))
    S.page(lang, key, c["title"], c["desc"], c["h1"], c["sub"], action, c["dare"], body,
           [S.offer_ld(lang), S.faq_ld(lang, c["faq"])], url(key, OTHER[lang]), hero_extra=E.hero_widgets(c))


def hub(lang):
    h = HUB[lang]
    m = MENU[lang]
    def card(k):
        c = UC[k][lang]
        rest = c["h1"].split('h1-rest">')[1].split("</span>")[0]
        title = rest[0].upper() + rest[1:]
        first = c["desc"].split(". ")[0].rstrip(".") + "."
        return (f'<a class="uc-card" href="{url(k, lang)}"><small>{m[k][0]}</small><b>{title}</b>'
                f'<p>{first}</p><em>{h["more"]}&nbsp;→</em></a>')
    cards = "".join(card(k) for k in ORDER)
    grid = f'<section class="ent-sec" id="use-cases"><div class="wrap"><div class="uc-hub reveal">{cards}</div></div></section>'
    body = "\n\n".join([E.ENT_CSS, UC_CSS, grid, proof(UC["startups"][lang] | {
        "stats_h": E.C[lang]["proof_h"], "stats": E.C[lang]["stats"]}, lang), "{LEAD}"])
    S.page(lang, "hub", h["title"], h["desc"], h["h1"], h["sub"], S.form(lang, h["btn"]), h["dare"], body, [S.offer_ld(lang)], url("hub", OTHER[lang]))


def sync_assets():
    """Use the asset versions of the live homepage (the shared builder still has older ones)."""
    home = (ROOT / "index.html").read_text()
    vers = dict(re.findall(r"/([\w.-]+\.(?:css|js))\?v=(\d+)", home))
    for key in ["hub"] + ORDER:
        for lang in ("en", "de"):
            p = ROOT / url(key, lang).strip("/") / "index.html"
            s = p.read_text()
            s = re.sub(r"/([\w.-]+\.(?:css|js))\?v=\d+", lambda m: f"/{m.group(1)}?v={vers[m.group(1)]}" if m.group(1) in vers else m.group(0), s)
            s = s.replace("<!-- generated by _tools/build_static_pages.py, edit the script, not this file -->",
                          "<!-- generated by _tools/usecase_pages.py, edit _tools/usecase_content.py, not this file -->")
            p.write_text(s)


def sitemap():
    p = ROOT / "sitemap.xml"
    s = p.read_text()
    add = ""
    for key in ["hub"] + ORDER:
        for lang in ("en", "de"):
            loc = S.SITE + url(key, lang)
            if f"<loc>{loc}</loc>" not in s:
                add += f"  <url><loc>{loc}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>\n"
    if add:
        p.write_text(s.replace("</urlset>", add + "</urlset>"))
    print("sitemap:", add.count("<url>"), "added")


if __name__ == "__main__":
    nav_usecases.apply(ROOT / "index.html")
    nav_usecases.apply(ROOT / "de" / "index.html")
    for key in ["hub"] + ORDER:
        S.PATHS[key] = {"en": url(key, "en"), "de": url(key, "de")}
    for lang in ("en", "de"):
        hub(lang)
        for key in ORDER:
            usecase(key, lang)
    sync_assets()
    sitemap()
    for p in sorted(ROOT.rglob("*.html")):
        if "angebot" not in p.parts:
            nav_usecases.apply(p)

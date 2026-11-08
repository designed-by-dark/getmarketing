#!/usr/bin/env python3
"""Case study pages (EN + DE): one page per case plus an overview, in the pricing/enterprise design.

Copy lives in _tools/case_data.py. Nav, footer and lead form come from the homepages via build_static_pages.
  python3 _tools/build_case_pages.py
Writes case-studies/<slug>/index.html, de/referenzen/<slug>/index.html and the two overview pages.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_static_pages as S
from case_data import CASES

BASE = {"en": "/case-studies/", "de": "/de/referenzen/"}
T = {
 "en": {"k_ch": "Starting point", "h_ch": "The challenge", "k_did": "What we did", "h_did": "What we built",
        "k_why": "Why it worked", "h_why": "How the system worked", "k_today": "With GetMarketing", "h_today": "How GetMarketing does this&nbsp;today",
        "today_link": '<p><a href="/#how-it-works">See how GetMarketing works&nbsp;→</a></p>',
        "more": "More case&nbsp;studies", "btn": "Get a free analysis of your&nbsp;website", "facts": "",
        "back": '<a href="/case-studies/">← All case&nbsp;studies</a>', "anon": "We don’t name clients. The numbers come from the respective project. First results typically showed after 3–6&nbsp;months.",
        "ov_title": "Case studies · GetMarketing", "ov_desc": "Real projects behind the GetMarketing method: B2B, e-commerce and local businesses, with the numbers from each project.",
        "ov_h1": '<span class="hl">Case studies:</span> <span class="h1-rest">what this method achieved in real&nbsp;projects</span>',
        "ov_sub": "GetMarketing is built on the approach Darya Kablash used for B2B, e-commerce and local clients. Every case shows the starting point, what was built and why it worked. SEO compounds: first results typically show after 3–6&nbsp;months.",
        "read": "Read the case&nbsp;→", "suffix": " · Case study · GetMarketing"},
 "de": {"k_ch": "Ausgangslage", "h_ch": "Die Herausforderung", "k_did": "Was wir gemacht haben", "h_did": "Was wir aufgebaut&nbsp;haben",
        "k_why": "Warum es funktioniert hat", "h_why": "Wie das System funktioniert&nbsp;hat", "k_today": "Mit GetMarketing", "h_today": "So macht GetMarketing das&nbsp;heute",
        "today_link": '<p><a href="/de/#so-funktionierts">So funktioniert GetMarketing&nbsp;→</a></p>',
        "more": "Weitere&nbsp;Referenzen", "btn": "Kostenlose Analyse deiner Website", "facts": "",
        "back": '<a href="/de/referenzen/">← Alle&nbsp;Referenzen</a>', "anon": "Wir nennen keine Kunden. Die Zahlen stammen aus dem jeweiligen Projekt. Erste Ergebnisse zeigten sich meist nach 3–6&nbsp;Monaten.",
        "ov_title": "Referenzen · GetMarketing", "ov_desc": "Echte Projekte hinter der GetMarketing-Methode: B2B, E-Commerce und lokale Anbieter, mit den Zahlen aus jedem Projekt.",
        "ov_h1": '<span class="hl">Referenzen:</span> <span class="h1-rest">was diese Methode in echten Projekten erreicht&nbsp;hat</span>',
        "ov_sub": "GetMarketing basiert auf dem Vorgehen, mit dem Darya Kablash B2B-, E-Commerce- und lokale Kunden betreut hat. Jeder Case zeigt die Ausgangslage, was gebaut wurde und warum es funktioniert hat. SEO wirkt mit Verzögerung: Erste Ergebnisse zeigen sich meist nach 3–6&nbsp;Monaten.",
        "read": "Zum Case&nbsp;→", "suffix": " · Referenz · GetMarketing"},
}

CSS = """<style>
  .cs-stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
  .cs-stat { background: #fff; border-radius: var(--r-card); padding: 28px 26px; box-shadow: var(--card-shadow); }
  .cs-stat:first-child { background: var(--forest); }
  .cs-stat b { display: block; font-size: clamp(32px, 3.4vw, 46px); font-weight: 700; letter-spacing: -0.04em; line-height: 1.05; color: var(--black); }
  .cs-stat:first-child b { color: var(--lime); }
  .cs-stat span { display: block; margin-top: 10px; font-size: 15px; line-height: 1.5; color: #4A504C; }
  .cs-stat:first-child span { color: rgba(255,255,255,.78); }
  .cs-tag { display: inline-block; margin-bottom: 10px; font-size: 13px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--lime); }
  .lp-split-head h2, .lp-sec .sec-head h2, .lp-hero h1 { hyphens: manual; -webkit-hyphens: manual; }
  .cs-anon { margin-top: 14px; font-size: 13px; color: #7A807C; }
  .cs-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }
  a.cs-card { display: flex; flex-direction: column; gap: 10px; padding: 28px 26px; background: #fff; border-radius: var(--r-card); box-shadow: var(--card-shadow); text-decoration: none; color: inherit; transition: transform .2s ease, box-shadow .2s ease; }
  a.cs-card:hover { transform: translateY(-3px); box-shadow: 0 24px 50px -28px rgba(13,29,21,.45); }
  a.cs-card small { font-size: 12px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--forest); }
  a.cs-card b { font-size: 34px; font-weight: 700; letter-spacing: -0.04em; line-height: 1.05; color: var(--black); }
  a.cs-card p { font-size: 15.5px; line-height: 1.55; color: #4A504C; flex: 1; }
  a.cs-card em { font-style: normal; font-weight: 600; color: var(--forest); }
  .lp-split-body .lp-checks li { font-size: 17px; }
  .cs-shot { margin: 22px auto 0; }
  .cs-shot img { display: block; width: 100%; height: auto; border-radius: 14px; box-shadow: var(--card-shadow); background: #fff; }
  .cs-shot figcaption { margin-top: 10px; font-size: 13px; color: #7A807C; text-align: center; }
  @media (max-width: 760px) { .cs-stats { grid-template-columns: 1fr; } }
</style>"""


SHOTS = {  # slug: (width, height, source tool)
 "special-machinery": (730, 500, "SISTRIX"), "b2b-software": (970, 314, "Google Search Console"),
 "first-aid-school": (980, 316, "Google Search Console"), "agency-lead-generation": (1000, 316, "Google Search Console"),
 "jewelry-online-shop": (934, 496, "Semrush"), "cooking-school": (516, 454, "Google Search Console"),
 "investment-school": (516, 454, "Google Search Console")}
SHOT_CAP = {"en": "Screenshot from {tool}, client details removed.", "de": "Screenshot aus {tool}, Kundendaten entfernt."}


def stats(items, lang, slug):
    c = "".join(f'<div class="cs-stat"><b>{n}</b><span>{l}</span></div>' for n, l in items)
    shot = ""
    if slug in SHOTS:
        w, h, tool = SHOTS[slug]
        shot = (f'<figure class="cs-shot reveal" style="max-width:{w}px"><img src="/case-studies/img/{slug}.jpg" width="{w}" height="{h}" '
                f'alt="{tool}" loading="lazy" decoding="async"><figcaption>{SHOT_CAP[lang].format(tool=tool)}</figcaption></figure>')
    return (f'<section class="lp-sec" style="padding-top:8px"><div class="wrap"><div class="cs-stats reveal">{c}</div>'
            f'{shot}<p class="cs-anon reveal">{T[lang]["anon"]}</p></div></section>')


def card_list(cases, lang):
    out = []
    for c in cases:
        n, l = c["stats"][lang][0]
        out.append(f'<a class="cs-card" href="{BASE[lang]}{c["slug"][lang]}/"><small>{c["tag"][lang]}</small><b>{n}</b>'
                   f'<p>{c["card"][lang]}</p><em>{T[lang]["read"]}</em></a>')
    return '<div class="cs-cards">' + "".join(out) + "</div>"


def more(case, lang):
    i = CASES.index(case)
    others = [CASES[(i + k) % len(CASES)] for k in (1, 2, 3)]
    return (f'<section class="lp-sec"><div class="wrap"><div class="sec-head reveal"><h2>{T[lang]["more"]}</h2></div>'
            f'<div class="lp-body reveal">{card_list(others, lang)}</div></div></section>')


def action(lang):
    t = T[lang]
    return f'<a href="#start" class="btn-hero">{t["btn"]}</a>'


def build():
    for lang in ("en", "de"):
        t = T[lang]; other = "de" if lang == "en" else "en"
        for c in CASES:
            key = "case-" + c["slug"]["en"]
            S.PATHS[key] = {l: BASE[l] + c["slug"][l] + "/" for l in ("en", "de")}
            body = "\n\n".join([
                CSS,
                stats(c["stats"][lang], lang, c["slug"]["en"]),
                S.split(t["h_ch"], f'<p>{c["challenge"][lang]}</p>', k=t["k_ch"]),
                S.split(t["h_did"], S.ul(c["did"][lang]), k=t["k_did"]),
                S.split(t["h_why"], "".join(f"<p>{p}</p>" for p in c["why"][lang]), k=t["k_why"], flip=True),
                S.split(t["h_today"], f'<p>{c["today"][lang]}</p>' + t["today_link"], k=t["k_today"]),
                more(c, lang),
                "{LEAD}"])
            plain_h1 = S.re.sub(r"<[^>]+>", "", c["h1"][lang])
            S.page(lang, key, plain_h1 + t["suffix"], S.re.sub(r"<[^>]+>|&nbsp;", " ", c["card"][lang]).strip(),
                   c["h1"][lang], f'<span class="cs-tag">{c["tag"][lang]}</span><br>' + c["sub"][lang],
                   action(lang), t["back"], body, [], S.PATHS[key][other])
        key = "cases"
        S.PATHS[key] = dict(BASE)
        body = "\n\n".join([CSS,
            f'<section class="lp-sec" style="padding-top:8px"><div class="wrap"><div class="lp-body reveal">{card_list(CASES, lang)}</div>'
            f'<p class="cs-anon reveal">{t["anon"]}</p></div></section>', "{LEAD}"])
        S.page(lang, key, t["ov_title"], t["ov_desc"], t["ov_h1"], t["ov_sub"], action(lang),
               "", body, [], BASE[other])


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""Topic pages (the 18 EN/DE pairs built from _content/) and the internal links between them.

One list feeds every place that links to the topic pages:
  - the "Solutions" / "Lösungen" block in the footer of every page (apply_footer)
  - the "Solutions" section at the end of every topic page (related_section, used by build_seo_pages.py)
  - the topic overview on the use-case hubs and the matching topics on each use-case page (usecase_pages.py)

  python3 _tools/topics.py            # put the footer block into every page (idempotent)
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (cluster, en_slug, en_label, de_slug, de_label)
TOPICS = [
    ("team", "ai-marketing-team", "AI marketing team", "ki-marketingteam", "KI-Marketingteam"),
    ("team", "ai-cmo", "AI CMO", "ki-cmo", "KI-CMO"),
    ("team", "virtual-cmo", "Virtual CMO", "virtueller-cmo", "Virtueller CMO"),
    ("team", "ai-marketing-manager", "AI marketing manager", "ki-marketing-manager", "KI-Marketing-Manager"),
    ("team", "ai-marketing-agency", "AI marketing agency", "ki-marketing-agentur", "KI-Marketing-Agentur"),
    ("team", "done-for-you-marketing", "Done-for-you marketing", "marketing-auslagern", "Marketing auslagern"),
    ("seo", "ai-seo-tool", "AI SEO tool", "ki-seo-tool", "KI-SEO-Tool"),
    ("seo", "automate-seo", "Automate SEO", "seo-automatisieren", "SEO automatisieren"),
    ("seo", "ai-blog-writing", "AI blog writing", "ki-blogartikel-schreiben", "KI-Blogartikel schreiben"),
    ("auto", "ai-marketing-automation", "AI marketing automation", "ki-marketing-automatisierung", "KI-Marketing-Automatisierung"),
    ("auto", "marketing-automation", "Marketing automation", "marketing-automatisierung", "Marketing-Automatisierung"),
    ("auto", "ai-in-marketing", "AI in marketing", "marketing-ki", "Marketing-KI"),
    ("leads", "b2b-lead-generation", "B2B lead generation", "b2b-leadgenerierung", "B2B-Leadgenerierung"),
    ("leads", "b2b-lead-generation-strategies", "B2B lead generation strategies", "b2b-leadgenerierung-strategien", "Strategien für B2B-Leadgenerierung"),
    ("leads", "b2b-linkedin-lead-generation", "LinkedIn lead generation", "linkedin-leadgenerierung-b2b", "LinkedIn-Leadgenerierung im B2B"),
    ("biz", "marketing-for-saas", "Marketing for SaaS", "saas-marketing", "SaaS-Marketing"),
    ("biz", "marketing-for-small-businesses", "Marketing for small businesses", "marketing-fuer-kleine-unternehmen", "Marketing für kleine Unternehmen"),
    ("biz", "marketing-plan-generator", "Marketing plan generator", "marketingplan-erstellen", "Marketingplan erstellen"),
]

CLUSTERS = {
    "en": {"team": "Your AI marketing team", "seo": "SEO and content", "auto": "Automation and AI", "leads": "B2B lead generation", "biz": "By company type"},
    "de": {"team": "Dein KI-Marketingteam", "seo": "SEO und Content", "auto": "Automatisierung und KI", "leads": "B2B-Leadgenerierung", "biz": "Nach Unternehmensart"},
}

# hand-picked neighbours from other clusters, so every page also links out of its own group
CROSS = {
    "team": ["automate-seo", "b2b-lead-generation"], "seo": ["ai-marketing-team", "ai-marketing-automation"],
    "auto": ["ai-marketing-team", "ai-seo-tool"], "leads": ["ai-cmo", "ai-blog-writing"],
    "biz": ["ai-marketing-team", "automate-seo"],
}

# use case (usecase_content.ORDER key) -> English topic slugs that fit it
USECASE_TOPICS = {
    "startups": ["marketing-for-saas", "ai-marketing-team", "ai-blog-writing", "ai-cmo"],
    "ecommerce": ["ai-seo-tool", "automate-seo", "ai-blog-writing", "marketing-for-small-businesses"],
    "agencies": ["ai-marketing-agency", "done-for-you-marketing", "ai-marketing-automation", "ai-seo-tool"],
    "b2b": ["b2b-lead-generation", "b2b-linkedin-lead-generation", "b2b-lead-generation-strategies", "virtual-cmo"],
}

T = {
    "en": dict(foot_h="Solutions", rel_k="Solutions", rel_h="More solutions for your&nbsp;marketing", hub_k="Solutions", hub_h="Solutions by&nbsp;task",
               uc_h="Matching&nbsp;solutions", more="Learn more", all_uc=("/use-cases/", "Use cases by company type"),
               cases=("/case-studies/", "Case studies with real numbers"), pricing=("/pricing/", "Pricing")),
    "de": dict(foot_h="Lösungen", rel_k="Lösungen", rel_h="Weitere Lösungen für dein&nbsp;Marketing", hub_k="Lösungen", hub_h="Lösungen nach&nbsp;Aufgabe",
               uc_h="Passende&nbsp;Lösungen", more="Mehr erfahren", all_uc=("/de/loesungen/", "Lösungen nach Unternehmensart"),
               cases=("/de/referenzen/", "Referenzen mit echten Zahlen"), pricing=("/de/preise/", "Preise")),
}

BY_SLUG = {}
for _c, _en, _el, _de, _dl in TOPICS:
    BY_SLUG[_en] = dict(cluster=_c, lang="en", slug=_en, label=_el, alt=_de)
    BY_SLUG[_de] = dict(cluster=_c, lang="de", slug=_de, label=_dl, alt=_en)


def topics(lang):
    """[(cluster, href, label)] in menu order"""
    return [(c, f"/{en if lang == 'en' else de}/", el if lang == "en" else dl) for c, en, el, de, dl in TOPICS]


def in_lang(en_slug, lang):
    t = BY_SLUG[en_slug]
    return t["slug"] if lang == "en" else t["alt"]


def related(slug, n=5):
    """Same-language neighbours of a topic page: its cluster first, then cross links."""
    me = BY_SLUG[slug]; lang = me["lang"]
    same = [s for c, s, _ in [(c, (en if lang == "en" else de), None) for c, en, _, de, _ in TOPICS] if c == me["cluster"] and s != slug]
    cross = [in_lang(s, lang) for s in CROSS[me["cluster"]] if in_lang(s, lang) != slug]
    out = []
    for s in same[:3] + cross + same[3:]:
        if s not in out: out.append(s)
    return [(f"/{s}/", BY_SLUG[s]["label"]) for s in out[:n]]


def related_section(slug):
    lang = BY_SLUG[slug]["lang"]; t = T[lang]
    links = related(slug) + [t["all_uc"], t["cases"]]
    items = "".join(f'<li><a href="{h}">{html.escape(l)}&nbsp;→</a></li>' for h, l in links)
    return (f'<section class="lp-sec lp-related" aria-labelledby="rel-h"><div class="wrap"><div class="sec-head reveal">'
            f'<span class="lp-k">{t["rel_k"]}</span><h2 id="rel-h">{t["rel_h"]}</h2></div>'
            f'<ul class="lp-rel-list reveal">{items}</ul></div></section>')


def hub_section(lang):
    """All topic pages of one language, grouped, for the use-case hub."""
    t = T[lang]
    groups = []
    for key, name in CLUSTERS[lang].items():
        li = "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for c, h, l in topics(lang) if c == key)
        groups.append(f'<div class="lp-topic-group"><h3>{name}</h3><ul>{li}</ul></div>')
    return (f'<section class="ent-sec lp-topics" id="topics" aria-labelledby="topics-h"><div class="wrap"><div class="sec-head reveal">'
            f'<span class="lp-k">{t["hub_k"]}</span><h2 id="topics-h">{t["hub_h"]}</h2></div>'
            f'<div class="lp-topic-grid reveal">{"".join(groups)}</div></div></section>')


def usecase_section(key, lang):
    t = T[lang]
    items = "".join(f'<li><a href="/{in_lang(s, lang)}/">{html.escape(BY_SLUG[in_lang(s, lang)]["label"])}&nbsp;→</a></li>' for s in USECASE_TOPICS[key])
    return (f'<section class="ent-sec lp-related" aria-labelledby="uc-topics-h"><div class="wrap"><div class="sec-head reveal">'
            f'<span class="lp-k">{t["hub_k"]}</span><h2 id="uc-topics-h">{t["uc_h"]}</h2></div>'
            f'<ul class="lp-rel-list reveal">{items}</ul></div></section>')


def footer_block(lang):
    t = T[lang]
    li = "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for _, h, l in topics(lang))
    return f'<div class="ft-topics"><h2 class="ft-h">{t["foot_h"]}</h2><ul class="ft-topics-list">{li}</ul></div>'


FOOT_RE = re.compile(r'\s*<div class="ft-topics">.*?</ul></div>', re.S)


def apply_footer(path):
    """Put the topic block between the footer grid and the bottom row. Idempotent."""
    p = pathlib.Path(path); s = p.read_text()
    if '<footer class="ft">' not in s: return False
    m = re.search(r'<html lang="(\w+)"', s); lang = "de" if m and m.group(1) == "de" else "en"
    n = FOOT_RE.sub("", s)
    n = n.replace('\n    <div class="ft-bottom">', "\n    " + footer_block(lang) + '\n    <div class="ft-bottom">', 1)
    if n != s: p.write_text(n); return True
    return False


def all_pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).parts
        if rel[0] in ("angebot", "intern", "_tools", "_content") or rel[0].startswith("."): continue
        yield p


if __name__ == "__main__":
    n = sum(apply_footer(p) for p in all_pages())
    print("footer solutions:", n, "pages updated")

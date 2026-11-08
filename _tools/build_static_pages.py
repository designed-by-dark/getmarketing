#!/usr/bin/env python3
"""Pricing and Enterprise pages (EN + DE), in the homepage design.

Nav, footer, pricing cards and the lead form are taken from index.html / de/index.html,
so a change there shows up here after the next run. The copy follows the offer structure
(getmarketing-research/angebot-struktur-de.md): only what really exists, prices with "from".
  python3 _tools/build_static_pages.py
Writes pricing/index.html, de/preise/index.html, enterprise/index.html, de/enterprise/index.html.
"""
import html, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from site_faq import FAQ, faq_section, faq_ld
from no_orphans import fix

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://getmarketing.team"
HOME = {"en": ROOT / "index.html", "de": ROOT / "de" / "index.html"}
HOME_URL = {"en": "/", "de": "/de/"}
PATHS = {"pricing": {"en": "/pricing/", "de": "/de/preise/"}, "enterprise": {"en": "/enterprise/", "de": "/de/enterprise/"}}


def home_parts(lang):
    s = HOME[lang].read_text()
    home = HOME_URL[lang]
    nav = re.search(r"<nav>.*?</nav>", s, re.S).group(0).replace('<a href="#" class="nav-logo">', f'<a href="{home}" class="nav-logo">')
    foot = re.search(r'<footer class="ft">.*?</footer>', s, re.S).group(0).replace('<a href="#" class="ft-logo">', f'<a href="{home}" class="ft-logo">')
    foot = re.sub(r'href="#(?!start)', f'href="{home}#', foot)
    offer = re.search(r'<section id="(?:pricing|preise)" class="offer-section">.*?</section>', s, re.S).group(0)
    offer = re.sub(r'<section id="(?:pricing|preise)"', '<section id="plans"', offer, count=1)
    offer = re.sub(r'\s*<a class="offer-more"[^>]*>.*?</a>', "", offer)  # already on the pricing page
    lead = re.search(r'<section id="start" class="lead-section">.*?</section>', s, re.S).group(0)
    return nav, foot, offer, lead


def ul(items, cls="lp-checks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def split(h2, body, k="", flip=False, sid=""):
    return (f'<section class="lp-sec lp-split{" lp-flip" if flip else ""}"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}><div class="wrap lp-split-grid">'
            f'<div class="lp-split-head reveal">{f"<span class={chr(34)}lp-k{chr(34)}>{k}</span>" if k else ""}<h2>{h2}</h2></div>'
            f'<div class="lp-split-body reveal">{body}</div></div></section>')


def cards(h2, items, k="", sub="", sid=""):
    c = "".join(f'<div class="lpc-card"><span class="lp-num">{n}</span><h3>{t}</h3><p>{p}</p></div>' for n, t, p in items)
    return (f'<section class="lp-sec"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}><div class="wrap"><div class="sec-head reveal">'
            f'{f"<span class={chr(34)}lp-k{chr(34)}>{k}</span>" if k else ""}<h2>{h2}</h2>{f"<p class={chr(34)}sec-sub{chr(34)}>{sub}</p>" if sub else ""}</div>'
            f'<div class="lp-body reveal"><div class="lpc-cards">{c}</div></div></div></section>')


def table(h2, head, rows, k="", after=""):
    th = "".join(f'<th{" class=" + chr(34) + "gm" + chr(34) if i == len(head) - 1 else ""}>{h}</th>' for i, h in enumerate(head))
    tr = "".join("<tr>" + "".join(f'<td{" class=" + chr(34) + "gm" + chr(34) if i == len(r) - 1 else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return (f'<section class="lp-sec lp-cmp"><div class="wrap"><div class="sec-head reveal">{f"<span class={chr(34)}lp-k{chr(34)}>{k}</span>" if k else ""}<h2>{h2}</h2></div>'
            f'<div class="lp-table reveal"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
            f'{f"<div class={chr(34)}lp-after reveal{chr(34)}><p>{after}</p></div>" if after else ""}</div></section>')


def steps(h2, items, k="", sub=""):
    li = "".join(f'<div class="lpc-card ent-step"><span class="lp-num">{n}</span><h3>{t}</h3><p class="ent-price">{price}</p>{ul(pts, "ent-pts")}</div>' for n, t, price, pts in items)
    return (f'<section class="lp-sec" id="stages"><div class="wrap"><div class="sec-head reveal">{f"<span class={chr(34)}lp-k{chr(34)}>{k}</span>" if k else ""}<h2>{h2}</h2>'
            f'{f"<p class={chr(34)}sec-sub{chr(34)}>{sub}</p>" if sub else ""}</div><div class="lp-body reveal"><div class="lpc-cards ent-steps">{li}</div></div></div></section>')


EXTRA_CSS = """<style>
  .lp-hero .hero-row .btn-hero { text-decoration: none; display: inline-block; }
  .ent-steps { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  @media (min-width: 1100px) { .ent-steps { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
  @media (max-width: 640px) { .ent-steps { grid-template-columns: 1fr; } }
  .ent-step .ent-price { font-size: 22px !important; font-weight: 700; letter-spacing: -.02em; color: var(--black) !important; }
  .ent-step:nth-child(4n+1) .ent-price { color: #fff !important; }
  .ent-pts { list-style: none; padding: 0; margin: 4px 0 0; display: grid; gap: 8px; font-size: 15px; line-height: 1.5; color: #4A504C; }
  .ent-pts li { position: relative; padding-left: 18px; }
  .ent-pts li::before { content: "✓"; position: absolute; left: 0; color: var(--forest); font-weight: 700; }
  .ent-step:nth-child(4n+1) .ent-pts li { color: rgba(255,255,255,.8); }
  .ent-step:nth-child(4n+1) .ent-pts li::before { color: var(--lime); }
  .lp-sec .sec-sub { margin-top: 14px; font-size: 17px; line-height: 1.6; color: #4A504C; }
  #plans { padding-top: 24px; }
  @media print { nav, footer, .lead-section, .lp-hero .hero-row, .hero-dare { display: none !important; } }
</style>"""


def page(lang, key, title, desc, h1, sub, action, dare, body, ld, alt_lang_url, hero_extra=""):
    nav, foot, offer, lead = home_parts(lang)
    url = SITE + PATHS[key][lang]
    other = "de" if lang == "en" else "en"
    nav = re.sub(r'(<a href=")[^"]*(" class="nav-lang")', lambda m: m.group(1) + alt_lang_url + m.group(2), nav, count=1)
    nav = nav.replace('id="switch-de"', 'id="switch-de"')
    body = body.replace("{OFFER}", offer).replace("{LEAD}", lead)
    hreflang = (f'<link rel="alternate" hreflang="{lang}" href="{url}" />\n'
                f'<link rel="alternate" hreflang="{other}" href="{SITE + PATHS[key][other]}" />\n'
                f'<link rel="alternate" hreflang="x-default" href="{SITE + PATHS[key]["en"]}" />')
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "GetMarketing", "item": SITE + HOME_URL[lang]},
        {"@type": "ListItem", "position": 2, "name": re.sub(r"\s*·.*", "", title), "item": url}]}
    lds = "\n".join(ld + ['<script type="application/ld+json">\n' + json.dumps(crumbs, ensure_ascii=False, indent=1) + "\n</script>"])
    t = html.escape(title, quote=True); d = html.escape(desc, quote=True)
    out = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{t}</title>
<meta name="description" content="{d}" />
<meta name="robots" content="index, follow" />
<link rel="canonical" href="{url}" />
{hreflang}
<meta property="og:type" content="website" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:image" content="{SITE}/og-home.jpg" />
<meta property="og:site_name" content="GetMarketing" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="/logo.jpg" />
<!-- Analytics (Google Analytics 4 + Amplitude EU) are loaded consent-gated via /analytics.js -->
{lds}
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400..800&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/home.css?v=1" />
<link rel="stylesheet" href="/home-hero.css?v=15" />
<link rel="stylesheet" href="/theme.css?v=25" />
<link rel="stylesheet" href="/landing.css?v=4" />
{EXTRA_CSS}
<script defer src="/site.js?v=1"></script>
<script defer src="/home.js?v=10"></script>
<script defer src="/analytics.js"></script>
<script defer src="/nav-menu.js?v=2"></script>
</head>
<body class="lp">
<!-- generated by _tools/build_static_pages.py, edit the script, not this file -->
{nav}

<header class="hero hero-light lp-hero">
  <div class="wrap">
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    <div class="hero-row">
      {action}
    </div>
    <p class="hero-dare">{dare}</p>
  </div>
  {hero_extra}
</header>

{body}

{foot}
</body>
</html>
'''
    path = ROOT / PATHS[key][lang].strip("/") / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(fix(out))
    print("page", path.relative_to(ROOT))


def form(lang, btn):
    ph = "yourcompany.com" if lang == "en" else "deinefirma.de"
    lbl = "Your website" if lang == "en" else "Deine Website"
    facts = "Too good to be true? Let us prove you&nbsp;wrong." if lang == "en" else "Zu gut, um wahr zu sein? Lass dich&nbsp;überzeugen."
    return (f'<form class="hero-url" action="#start" data-lead-prefill><input type="text" name="website" inputmode="url" autocomplete="url" placeholder="{ph}" aria-label="{lbl}">'
            f'<button type="submit" class="btn-hero">{btn}</button></form><p class="hero-facts">{facts}</p>')


def offer_ld(lang):
    en = lang == "en"
    data = {"@context": "https://schema.org", "@type": "Service", "name": "GetMarketing",
            "provider": {"@type": "Organization", "name": "GetMarketing", "url": SITE},
            "areaServed": ["DE", "AT", "CH"],
            "offers": [
                {"@type": "Offer", "name": "GetMarketing", "price": "249", "priceCurrency": "EUR",
                 "description": "Per domain and month, everything included" if en else "Pro Domain und Monat, alles inklusive"},
                {"@type": "Offer", "name": "GetMarketing, yearly" if en else "GetMarketing, jährlich", "price": "2490", "priceCurrency": "EUR",
                 "description": "Per domain and year, two months free" if en else "Pro Domain und Jahr, zwei Monate gratis"},
                {"@type": "Offer", "name": "Enterprise", "priceCurrency": "EUR",
                 "priceSpecification": {"@type": "PriceSpecification", "minPrice": "750", "priceCurrency": "EUR"},
                 "description": "Ongoing work from €750 a month per domain, foundation sprint from €990" if en else "Laufende Umsetzung ab 750 € im Monat pro Domain, Fundament-Sprint ab 990 €"}]}
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=1) + "\n</script>"


# ======================================================================
# PRICING
# ======================================================================
def pricing(lang):
    en = lang == "en"
    f = FAQ[lang]
    if en:
        faq_items = [
            ("I have several shops or brands. What do I pay?", "One plan per domain, all in one cockpit. Three shops cost 3 × €249 a month. There is no separate multi-brand&nbsp;plan."),
            ("Is there a setup fee?", "No. Onboarding is part of the first&nbsp;month."),
            f[8],
            ("What does Enterprise cost exactly?", "It starts with a free diagnosis. A foundation sprint costs from €990 one time, ongoing work from €750 a month per domain, with a minimum of 3 months and monthly after that. After the diagnosis you get a fixed offer. <a href=\"/enterprise/\">More about Enterprise</a>."),
            f[4], f[9], f[7]]
        body = "\n\n".join([
            "{OFFER}",
            split("What the €249 plan&nbsp;includes", ul([
                "<strong>A visibility check</strong> of your website with real search data: losses, brand share, technical errors and the demand you are not reaching",
                "<strong>A plan of actions</strong>: technical fixes, new pages and posts, each with the searches it can bring and a priority",
                "<strong>Technical fixes</strong> through your CMS: redirects, category pages, titles, meta descriptions, duplicates",
                "<strong>New pages and guides</strong>, written for you and published in your shop or CMS after you approve them",
                "<strong>Content for AI answers</strong> (GEO) and LinkedIn drafts for your management",
                "<strong>An alert</strong> as soon as your visibility drops, and a <strong>monthly report</strong>: what went live, what ranks, which enquiries came in",
                "<strong>Your part:</strong> approve. You write nothing yourself"]), k="Software"),
            table("GetMarketing or&nbsp;Enterprise?", ["", "GetMarketing", "Enterprise"], [
                ["Price", "€249 a month per domain, or €2,490 a year", "Sprint from €990, then from €750 a month per&nbsp;domain"],
                ["Who does the work", "The system. You approve", "The system plus a named person who owns the&nbsp;result"],
                ["Who checks the texts", "Automatic checks for facts, brand, SEO and compliance, plus spot checks", "A person checks every text before you&nbsp;approve"],
                ["Website changes", "Content and SEO settings through your CMS", "Also theme code, page speed and robots.txt"],
                ["Ads", "No", "Google Ads and Shopping as an&nbsp;add-on"],
                ["Contract", "Cancel monthly", "3 months minimum, then&nbsp;monthly"]], k="Compare",
                after="Not sure? Send us your website. The free analysis shows which of the two makes sense for&nbsp;you."),
            split("What GetMarketing deliberately does not&nbsp;do", ul([
                "<strong>Everything.</strong> We cover the most important 20%: Google, AI answers and LinkedIn. More channels would mean more decisions for you",
                "<strong>Video.</strong> No client has asked for it, and it stops working long before a page that ranks",
                "<strong>Paid ads in the software.</strong> That needs your ad budget and accounts. With Enterprise it is an add-on",
                "<strong>Theme code.</strong> You get a ready brief for your developer, or we do it with Enterprise",
                "<strong>Posting on LinkedIn for you.</strong> You copy the post and publish it yourself, so there is no bot risk"]), k="Honest scope", flip=True),
            cards("How the price&nbsp;compares", [
                ("€249", "Less than a part-time&nbsp;hire", "A marketer, even part time, costs more, and still needs you to decide what to do every&nbsp;week."),
                ("€2,000–7,000", "What an agency costs a&nbsp;month", "Agencies often hand the work to juniors, and the results are hard to trace. Enterprise starts at €750 with a named&nbsp;person."),
                ("€0", "No credits, no seat&nbsp;prices", "You pay per website. More users or more approvals don’t cost&nbsp;extra.")], k="Context"),
            faq_section(lang, faq_items, sec_id="pricing-faq"),
            "{LEAD}"])
        page(lang, "pricing", "Pricing · GetMarketing",
             "GetMarketing costs €249 a month per domain, everything included, or €2,490 a year. Enterprise with a named person starts from €750 a month. No credits, cancel monthly.",
             '<span class="hl">Pricing:</span> <span class="h1-rest">one plan per website, everything&nbsp;included</span>',
             "€249 a month per domain. No credits, no add-on maze, cancel monthly. If you would rather have it done for you, Enterprise starts with a free&nbsp;diagnosis.",
             form(lang, "Check my website for free"),
             'Want it done for you? <a href="/enterprise/">See Enterprise&nbsp;→</a>',
             body, [offer_ld(lang), faq_ld(lang, faq_items)], PATHS["pricing"]["de"])
    else:
        faq_items = [
            ("Ich habe mehrere Shops oder Marken. Was zahle ich?", "Ein Tarif pro Domain, alles in einem Cockpit. Drei Shops kosten 3 × 249 € im Monat. Einen eigenen Tarif für mehrere Marken gibt es&nbsp;nicht."),
            ("Gibt es eine Einrichtungsgebühr?", "Nein. Das Onboarding ist im ersten Monat&nbsp;enthalten."),
            f[8],
            ("Was kostet Enterprise genau?", "Es beginnt mit einer kostenlosen Diagnose. Ein Fundament-Sprint kostet einmalig ab 990 €, die laufende Umsetzung ab 750 € im Monat pro Domain, mit 3 Monaten Mindestlaufzeit und danach monatlich kündbar. Nach der Diagnose bekommst du ein festes Angebot. <a href=\"/de/enterprise/\">Mehr zu Enterprise</a>."),
            f[4], f[9], f[7]]
        body = "\n\n".join([
            "{OFFER}",
            split("Was im Tarif für 249 € drin&nbsp;ist", ul([
                "<strong>Ein Sichtbarkeits-Check</strong> deiner Website mit echten Suchdaten: Verluste, Anteil der Markensuchen, technische Fehler und die Nachfrage, die du nicht erreichst",
                "<strong>Ein Maßnahmenplan</strong>: technische Fixes, neue Seiten und Beiträge, jeweils mit den Suchen, die sie bringen können, und einer Priorität",
                "<strong>Technische Fixes</strong> über dein CMS: Weiterleitungen, Kategorieseiten, Titles, Meta-Beschreibungen, Dubletten",
                "<strong>Neue Seiten und Ratgeber</strong>, für dich geschrieben und nach deiner Freigabe in deinem Shop oder CMS veröffentlicht",
                "<strong>Inhalte für KI-Antworten</strong> (GEO) und LinkedIn-Entwürfe für die Geschäftsführung",
                "<strong>Ein Alarm</strong>, sobald deine Sichtbarkeit sinkt, und ein <strong>Monatsbericht</strong>: was live ging, was rankt, welche Anfragen kamen",
                "<strong>Dein Teil:</strong> freigeben. Du schreibst nichts selbst"]), k="Software"),
            table("GetMarketing oder&nbsp;Enterprise?", ["", "GetMarketing", "Enterprise"], [
                ["Preis", "249 € im Monat pro Domain, oder 2.490 € im Jahr", "Sprint ab 990 €, danach ab 750 € im Monat pro&nbsp;Domain"],
                ["Wer macht die Arbeit", "Das System. Du gibst frei", "Das System plus eine feste Person, die für das Ergebnis verantwortlich&nbsp;ist"],
                ["Wer prüft die Texte", "Automatische Prüfungen auf Fakten, Marke, SEO und Compliance, dazu Stichproben", "Ein Mensch prüft jeden Text, bevor du&nbsp;freigibst"],
                ["Änderungen an der Website", "Inhalte und SEO-Einstellungen über dein CMS", "Auch Theme-Code, Ladezeit und robots.txt"],
                ["Werbung", "Nein", "Google Ads und Shopping als&nbsp;Add-on"],
                ["Vertrag", "Monatlich kündbar", "3 Monate Mindestlaufzeit, danach&nbsp;monatlich"]], k="Vergleich",
                after="Unsicher? Schick uns deine Website. Die kostenlose Analyse zeigt, was von beidem für dich Sinn&nbsp;ergibt."),
            split("Was GetMarketing bewusst nicht&nbsp;macht", ul([
                "<strong>Alles.</strong> Wir machen die wichtigsten 20 %: Google, KI-Antworten und LinkedIn. Mehr Kanäle hießen mehr Entscheidungen für dich",
                "<strong>Video.</strong> Kein Kunde hat danach gefragt, und es wirkt viel kürzer als eine Seite, die rankt",
                "<strong>Werbung in der Software.</strong> Dafür braucht es dein Werbebudget und deine Konten. Bei Enterprise gibt es das als Add-on",
                "<strong>Theme-Code.</strong> Du bekommst eine fertige Anleitung für deinen Entwickler, oder wir setzen es bei Enterprise um",
                "<strong>Für dich auf LinkedIn posten.</strong> Du kopierst den Post und veröffentlichst ihn selbst, so gibt es kein Bot-Risiko"]), k="Ehrlicher Umfang", flip=True),
            cards("Was der Preis im Vergleich&nbsp;bedeutet", [
                ("249 €", "Weniger als ein&nbsp;Minijob", "Ein Minijob darf 2026 bis zu 603 € im Monat kosten, und auch dann musst du jede Woche entscheiden, was zu tun&nbsp;ist."),
                ("2.000–7.000 €", "Was eine Agentur im Monat&nbsp;kostet", "Agenturen geben die Arbeit oft an Junioren ab, und die Ergebnisse sind schwer nachzuvollziehen. Enterprise beginnt bei 750 € mit einer festen&nbsp;Person."),
                ("0 €", "Keine Credits, keine Preise pro&nbsp;Nutzer", "Du zahlst pro Website. Mehr Nutzer oder mehr Freigaben kosten nichts&nbsp;extra.")], k="Einordnung"),
            faq_section(lang, faq_items, sec_id="preise-faq"),
            "{LEAD}"])
        page(lang, "pricing", "Preise · GetMarketing",
             "GetMarketing kostet 249 € im Monat pro Domain, alles inklusive, oder 2.490 € im Jahr. Enterprise mit fester Ansprechperson ab 750 € im Monat. Keine Credits, monatlich kündbar.",
             '<span class="hl">Preise:</span> <span class="h1-rest">ein Tarif pro Website, alles&nbsp;drin</span>',
             "249 € im Monat pro Domain. Keine Credits, kein Add-on-Dschungel, monatlich kündbar. Wenn du es lieber machen lässt, beginnt Enterprise mit einer kostenlosen&nbsp;Diagnose.",
             form(lang, "Website kostenlos prüfen"),
             'Lieber machen lassen? <a href="/de/enterprise/">Enterprise ansehen&nbsp;→</a>',
             body, [offer_ld(lang), faq_ld(lang, faq_items)], PATHS["pricing"]["en"])


# ======================================================================
# ENTERPRISE
# ======================================================================
def enterprise(lang):
    en = lang == "en"
    pre = '<script>document.addEventListener("DOMContentLoaded",function(){var s=document.querySelector("#lead-form select[name=interest]");if(s)s.value="enterprise";});</script>'
    if en:
        faq_items = [
            ("How is Enterprise different from the €249 plan?", "It runs on the same system. With the software, the system does the work and checks quality automatically, and you approve. With Enterprise, a named person checks every text, takes on the technical work, including theme code and page speed, and is responsible for the&nbsp;result."),
            ("Do we have to commit for long?", "The foundation sprint is a one-time project. Ongoing work has a minimum of 3 months, after that you can cancel&nbsp;monthly."),
            ("What access do you need?", "For the diagnosis, read access to Google Search Console is enough. Write access to your CMS only comes later, when the first changes are approved. Everything is set up step by&nbsp;step."),
            ("Can you work with our developer or freelancer?", "Yes. We brief your own freelancer or developer, and they keep doing the parts they already&nbsp;do."),
            ("Do you also run ads?", "Yes, Google Ads and Google Shopping are available as an add-on in Enterprise. They are not part of the&nbsp;software."),
            ("Who is behind it?", "Darya Kablash, with more than 8 years in B2B marketing in the DACH region and over 55 completed projects. Every Enterprise client works with her directly, not with&nbsp;juniors.")]
        import enterprise_page
        enterprise_page.build(lang, faq_items, pre)
    else:
        faq_items = [
            ("Was ist bei Enterprise anders als im Tarif für 249 €?", "Es läuft auf demselben System. In der Software macht das System die Arbeit und prüft die Qualität automatisch, und du gibst frei. Bei Enterprise prüft eine feste Person jeden Text, übernimmt die technische Arbeit, auch Theme-Code und Ladezeit, und ist für das Ergebnis&nbsp;verantwortlich."),
            ("Müssen wir uns lange binden?", "Der Fundament-Sprint ist ein einmaliges Projekt. Die laufende Umsetzung hat 3 Monate Mindestlaufzeit, danach ist sie monatlich&nbsp;kündbar."),
            ("Welche Zugänge braucht ihr?", "Für die Diagnose reicht ein Lesezugriff auf die Google Search Console. Schreibzugriff auf dein CMS kommt erst später, wenn die ersten Änderungen freigegeben sind. Alles wird Schritt für Schritt&nbsp;eingerichtet."),
            ("Arbeitet ihr mit unserem Entwickler oder Freelancer zusammen?", "Ja. Wir briefen deinen eigenen Freelancer oder Entwickler, und er macht weiter, was er schon&nbsp;macht."),
            ("Schaltet ihr auch Werbung?", "Ja, Google Ads und Google Shopping gibt es bei Enterprise als Add-on. In der Software sind sie nicht&nbsp;enthalten."),
            ("Wer steckt dahinter?", "Darya Kablash, mit mehr als 8 Jahren B2B-Marketing im DACH-Raum und über 55 abgeschlossenen Projekten. Jeder Enterprise-Kunde arbeitet direkt mit ihr, nicht mit&nbsp;Junioren.")]
        import enterprise_page
        enterprise_page.build(lang, faq_items, pre)


if __name__ == "__main__":
    for lang in ("en", "de"):
        pricing(lang)
        enterprise(lang)

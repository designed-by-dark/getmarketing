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


def page(lang, key, title, desc, h1, sub, action, dare, body, ld, alt_lang_url):
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
        body = "\n\n".join([
            cards("What we have built for&nbsp;clients", [
                ("NEWS", "Law changes into three texts", "Every morning the system reads EU law sources, drops what creates no new obligation and turns each real change into a website article, a LinkedIn post and a newsletter item. After approval the article goes straight into&nbsp;TYPO3."),
                ("3 SHOPS", "Three online shops, one cockpit", "Visibility recovered after a domain move, duplicates between the shops resolved, new pages for wholesale and private label, and social posts for all three brands from one&nbsp;login."),
                ("SHOP", "~15 new SEO pages a month", "For a jewelry shop with a large range: category pages instead of filter URLs, clear product titles and a steady flow of new SEO pages. Today 383,943 organic visitors a&nbsp;month."),
                ("B2B", "Expert knowledge that AI cites", "For an industry association: existing expertise turned into articles that Google and AI answers use as a source, plus LinkedIn posts for the&nbsp;board."),
                ("AMAZON", "Own shop next to Amazon", "A lean shop, Google Shopping set up once and SEO running every month, so a product sold on Amazon gets a second channel that it&nbsp;owns."),
                ("AGENCY", "White label for an agency", "The agency sets the positioning. The system produces articles, posts and landing pages, and clients see it all in a portal with the agency’s&nbsp;brand.")],
                k="Workflows", sub="Every company works differently, so we build the workflow around yours. A few examples from projects and offers, without client&nbsp;names."),
            split("Fully automated, and it still doesn’t sound like&nbsp;AI", ul([
                "<strong>Every text starts from a real source:</strong> your documents, the original law text, real search data. Not from what a chatbot happens to know",
                "<strong>It sounds like you.</strong> The system knows your past texts, your terms and your no-gos, so nobody has to explain them again",
                "<strong>A named person reads every text</strong> before you see it, and fixes what doesn’t sound right",
                "<strong>Built to be found and quoted:</strong> the answer in the first two sentences, deadlines and facts at a glance, a link to the right page of yours",
                "<strong>It learns from your corrections.</strong> What you change once stays changed",
                "<strong>No mass content.</strong> Pages only where people actually search, so Google has no reason to see it as&nbsp;spam"]), k="Quality", flip=True),
            steps("From diagnosis to&nbsp;results", [
                ("STEP 0", "Visibility diagnosis", "Free", [
                    "Analysis of your domain with SISTRIX, Semrush, DataForSEO and Search Console",
                    "What lost visibility costs you, as one number",
                    "A ranked list of the levers that bring enquiries"]),
                ("STEP 1", "Foundation sprint", "from €990, one time", [
                    "Technical clean-up: redirects, categories instead of filter URLs, duplicates, titles and H1",
                    "GA4 and Search Console connected",
                    "Strategy and page plan",
                    "Your cockpit, for several brands if you need it"]),
                ("STEP 2", "Ongoing work", "from €750 a month", [
                    "Finished pages live in your shop or CMS: category pages, guides, pages for AI answers",
                    "LinkedIn drafts for the company and management",
                    "A monthly report in business language",
                    "A named person who checks every text before you approve"]),
                ("STEP 3", "Custom workflows", "Per project", [
                    "Automation built for your processes, like the examples above",
                    "Handed over with support, or run and maintained by us for a monthly fee"])],
                k="How it works", sub="It always starts with the diagnosis. After that we suggest what fits, with a fixed price. Ongoing work is per domain, with a minimum of 3 months and monthly after&nbsp;that."),
            split("One page for your&nbsp;IT", ul([
                "<strong>Read-only first, step by step.</strong> The diagnosis needs only read access to Search Console. CMS access comes later, once the first changes are approved",
                "<strong>Every change can be undone.</strong> Each change is logged as before and after and can be rolled back with one click",
                "<strong>Content and SEO settings through your CMS.</strong> Theme code only when agreed with you, and documented",
                "<strong>Hosting in Germany</strong> at Hetzner, GDPR-compliant",
                "<strong>Nothing goes live without approval</strong>, and nothing is posted on LinkedIn automatically",
                "<strong>No lock-in.</strong> Content belongs to you and stays online after you&nbsp;cancel"]) +
                '<p><a href="javascript:window.print()">Print this page for your IT&nbsp;team</a></p>', k="Security", flip=True, sid="it"),
            table("Compared with an agency, a freelancer or a&nbsp;consultant", ["", "What clients told us bothers them", "GetMarketing Enterprise"], [
                ["Agency, €2,000–7,000 a month", "Expensive, juniors do the work, results are hard to trace", "From €750 a month, the founder checks the work&nbsp;herself"],
                ["Freelancers", "They keep changing, nobody checks them", "One system with fixed responsibility. We brief your freelancer&nbsp;too"],
                ["Consultant, about €7,000 one time", "Expensive, a concept without execution", "The diagnosis is free, execution is&nbsp;included"]], k="Compare"),
            cards("What this method achieved in real&nbsp;projects", [
                ("55+", "Completed projects", "More than 8 years of B2B marketing in the DACH&nbsp;region."),
                ("383,000", "Organic visitors a month", "One online shop, without ad&nbsp;budget."),
                ("+96%", "Visibility", "Special machinery, SISTRIX&nbsp;index."),
                ("~200", "Courses sold a month", "A first-aid school, via&nbsp;Google.")], k="Results", sub="We don’t name clients. The numbers come from the respective&nbsp;projects."),
            faq_section(lang, faq_items, sec_id="enterprise-faq"),
            "{LEAD}", pre])
        page(lang, "enterprise", "Enterprise · GetMarketing",
             "Your entire marketing automated, built around your workflows, and it still doesn't sound like AI. A named person checks every text and owns the result.",
             '<span class="hl">Enterprise:</span> <span class="h1-rest">your entire marketing automated, and it still doesn’t sound like&nbsp;AI</span>',
             "We build the system around how your company works: fixes, pages, LinkedIn, newsletters, custom workflows. A named person checks every text and owns the&nbsp;result.",
             '<a href="#start" class="btn-hero" data-interest="enterprise">Book a free diagnosis</a>',
             'Prefer the software? <a href="/pricing/">See pricing&nbsp;→</a>',
             body, [faq_ld(lang, faq_items)], PATHS["enterprise"]["de"])
    else:
        faq_items = [
            ("Was ist bei Enterprise anders als im Tarif für 249 €?", "Es läuft auf demselben System. In der Software macht das System die Arbeit und prüft die Qualität automatisch, und du gibst frei. Bei Enterprise prüft eine feste Person jeden Text, übernimmt die technische Arbeit, auch Theme-Code und Ladezeit, und ist für das Ergebnis&nbsp;verantwortlich."),
            ("Müssen wir uns lange binden?", "Der Fundament-Sprint ist ein einmaliges Projekt. Die laufende Umsetzung hat 3 Monate Mindestlaufzeit, danach ist sie monatlich&nbsp;kündbar."),
            ("Welche Zugänge braucht ihr?", "Für die Diagnose reicht ein Lesezugriff auf die Google Search Console. Schreibzugriff auf dein CMS kommt erst später, wenn die ersten Änderungen freigegeben sind. Alles wird Schritt für Schritt&nbsp;eingerichtet."),
            ("Arbeitet ihr mit unserem Entwickler oder Freelancer zusammen?", "Ja. Wir briefen deinen eigenen Freelancer oder Entwickler, und er macht weiter, was er schon&nbsp;macht."),
            ("Schaltet ihr auch Werbung?", "Ja, Google Ads und Google Shopping gibt es bei Enterprise als Add-on. In der Software sind sie nicht&nbsp;enthalten."),
            ("Wer steckt dahinter?", "Darya Kablash, mit mehr als 8 Jahren B2B-Marketing im DACH-Raum und über 55 abgeschlossenen Projekten. Jeder Enterprise-Kunde arbeitet direkt mit ihr, nicht mit&nbsp;Junioren.")]
        body = "\n\n".join([
            cards("Was wir für Kunden gebaut&nbsp;haben", [
                ("NEWS", "Aus Gesetzesänderungen werden drei Texte", "Jeden Morgen liest das System EU-Rechtsquellen, sortiert aus, was keine neue Pflicht bedeutet, und macht aus jeder echten Änderung einen Fachtext, einen LinkedIn-Post und einen Newsletter-Beitrag. Nach der Freigabe geht der Fachtext direkt in&nbsp;TYPO3."),
                ("3 SHOPS", "Drei Onlineshops, ein Cockpit", "Sichtbarkeit nach einem Domain-Umzug zurückgeholt, Dubletten zwischen den Shops aufgelöst, neue Seiten für Großhandel und Private Label und Social-Posts für alle drei Marken aus einem&nbsp;Login."),
                ("SHOP", "~15 neue SEO-Seiten im Monat", "Für einen Schmuckshop mit großem Sortiment: Kategorieseiten statt Filter-URLs, klare Produkttitel und ein fester Rhythmus neuer SEO-Seiten. Heute 383.943 organische Besucher im&nbsp;Monat."),
                ("B2B", "Fachwissen, das KI zitiert", "Für einen Industrieverband: vorhandenes Fachwissen als Beiträge, die Google und KI-Antworten als Quelle nutzen, dazu LinkedIn-Posts für den&nbsp;Vorstand."),
                ("AMAZON", "Eigener Shop neben Amazon", "Ein schlanker Shop, Google Shopping einmal sauber eingerichtet und SEO jeden Monat. So bekommt ein Amazon-Produkt einen zweiten Kanal, der dem Händler&nbsp;gehört."),
                ("AGENTUR", "White Label für eine Agentur", "Die Agentur gibt die Positionierung vor. Das System erstellt Artikel, Posts und Landingpages, und die Kunden sehen alles in einem Portal mit der Marke der&nbsp;Agentur.")],
                k="Workflows", sub="Jedes Unternehmen arbeitet anders, deshalb bauen wir den Workflow um deine Abläufe herum. Ein paar Beispiele aus Projekten und Angeboten, ohne&nbsp;Kundennamen."),
            split("Komplett automatisiert, und es klingt trotzdem nicht nach&nbsp;KI", ul([
                "<strong>Jeder Text beginnt mit einer echten Quelle:</strong> deinen Unterlagen, dem Originaltext des Gesetzes, echten Suchdaten. Nicht mit dem, was ein Chatbot zufällig weiß",
                "<strong>Er klingt nach dir.</strong> Das System kennt deine bisherigen Texte, deine Fachbegriffe und deine No-Gos, niemand muss sie neu erklären",
                "<strong>Eine feste Person liest jeden Text</strong>, bevor du ihn siehst, und korrigiert, was nicht passt",
                "<strong>Gebaut, um gefunden und zitiert zu werden:</strong> die Antwort in den ersten zwei Sätzen, Fristen und Fakten auf einen Blick, ein Link auf deine passende Seite",
                "<strong>Es lernt aus deinen Korrekturen.</strong> Was du einmal änderst, bleibt geändert",
                "<strong>Keine Massenware.</strong> Seiten nur dort, wo wirklich gesucht wird, damit Google keinen Grund hat, sie als Spam zu&nbsp;sehen"]), k="Qualität", flip=True),
            steps("Von der Diagnose zum&nbsp;Ergebnis", [
                ("STUFE 0", "Sichtbarkeits-Diagnose", "Kostenlos", [
                    "Analyse deiner Domain mit SISTRIX, Semrush, DataForSEO und Search Console",
                    "Was dich verlorene Sichtbarkeit kostet, als eine Zahl",
                    "Eine priorisierte Liste der Hebel, die Anfragen bringen"]),
                ("STUFE 1", "Fundament-Sprint", "ab 990 €, einmalig", [
                    "Technik aufräumen: Weiterleitungen, Kategorien statt Filter-URLs, Dubletten, Titles und H1",
                    "GA4 und Search Console angebunden",
                    "Strategie und Seitenplan",
                    "Dein Cockpit, bei Bedarf für mehrere Marken"]),
                ("STUFE 2", "Laufende Umsetzung", "ab 750 € im Monat", [
                    "Fertige Seiten live in deinem Shop oder CMS: Kategorieseiten, Ratgeber, Seiten für KI-Antworten",
                    "LinkedIn-Entwürfe für Unternehmen und Geschäftsführung",
                    "Ein Monatsbericht in Business-Sprache",
                    "Eine feste Person, die jeden Text prüft, bevor du freigibst"]),
                ("STUFE 3", "Eigene Workflows", "Pro Projekt", [
                    "Automatisierung für deine Abläufe, wie die Beispiele oben",
                    "Übergabe mit Betreuung, oder von uns betrieben und gepflegt gegen eine Monatsgebühr"])],
                k="So läuft es", sub="Es beginnt immer mit der Diagnose. Danach schlagen wir vor, was passt, mit festem Preis. Die laufende Umsetzung gilt pro Domain, mit 3 Monaten Mindestlaufzeit und danach monatlich&nbsp;kündbar."),
            split("Eine Seite für deine&nbsp;IT", ul([
                "<strong>Erst nur lesend, Schritt für Schritt.</strong> Für die Diagnose reicht ein Lesezugriff auf die Search Console. Der Zugang zum CMS kommt später, wenn die ersten Änderungen freigegeben sind",
                "<strong>Jede Änderung lässt sich zurücknehmen.</strong> Jede Änderung wird mit vorher und nachher protokolliert und lässt sich mit einem Klick rückgängig machen",
                "<strong>Inhalte und SEO-Einstellungen über dein CMS.</strong> Theme-Code nur nach Absprache mit dir und dokumentiert",
                "<strong>Hosting in Deutschland</strong> bei Hetzner, DSGVO-konform",
                "<strong>Nichts geht ohne Freigabe live</strong>, und auf LinkedIn wird nichts automatisch gepostet",
                "<strong>Kein Lock-in.</strong> Die Inhalte gehören dir und bleiben nach der Kündigung&nbsp;online"]) +
                '<p><a href="javascript:window.print()">Diese Seite für deine IT&nbsp;drucken</a></p>', k="Sicherheit", flip=True, sid="it"),
            table("Im Vergleich zu Agentur, Freelancer oder&nbsp;Berater", ["", "Was Kunden daran stört", "GetMarketing Enterprise"], [
                ["Agentur, 2.000–7.000 € im Monat", "Teuer, Junioren machen die Arbeit, Ergebnisse sind nicht nachvollziehbar", "Ab 750 € im Monat, die Gründerin prüft&nbsp;selbst"],
                ["Freelancer", "Wechseln ständig, niemand kontrolliert sie", "Ein System mit fester Verantwortung. Deinen Freelancer briefen wir&nbsp;mit"],
                ["Berater, ca. 7.000 € einmalig", "Teuer, Konzept ohne Umsetzung", "Die Diagnose ist kostenlos, die Umsetzung ist&nbsp;enthalten"]], k="Vergleich"),
            cards("Was diese Methode in echten Projekten erreicht&nbsp;hat", [
                ("55+", "Abgeschlossene Projekte", "Mehr als 8 Jahre B2B-Marketing im&nbsp;DACH-Raum."),
                ("383.000", "Organische Besucher im Monat", "Ein Onlineshop, ohne&nbsp;Werbebudget."),
                ("+96 %", "Sichtbarkeit", "Sondermaschinenbau,&nbsp;SISTRIX-Index."),
                ("~200", "Verkaufte Kurse im Monat", "Eine Erste-Hilfe-Schule, über&nbsp;Google.")], k="Ergebnisse", sub="Wir nennen keine Kunden. Die Zahlen stammen aus den jeweiligen&nbsp;Projekten."),
            faq_section(lang, faq_items, sec_id="enterprise-faq"),
            "{LEAD}", pre])
        page(lang, "enterprise", "Enterprise · GetMarketing",
             "Dein ganzes Marketing automatisiert, um deine Abläufe herum gebaut, und es klingt trotzdem nicht nach KI. Eine feste Person prüft jeden Text und ist für das Ergebnis verantwortlich.",
             '<span class="hl">Enterprise:</span> <span class="h1-rest">dein ganzes Marketing automatisiert, und es klingt trotzdem nicht nach&nbsp;KI</span>',
             "Wir bauen das System um die Abläufe deines Unternehmens herum: Fixes, Seiten, LinkedIn, Newsletter, eigene Workflows. Eine feste Person prüft jeden Text und ist für das Ergebnis&nbsp;verantwortlich.",
             '<a href="#start" class="btn-hero" data-interest="enterprise">Kostenlose Diagnose anfragen</a>',
             'Lieber die Software? <a href="/de/preise/">Preise ansehen&nbsp;→</a>',
             body, [faq_ld(lang, faq_items)], PATHS["enterprise"]["en"])


if __name__ == "__main__":
    for lang in ("en", "de"):
        pricing(lang)
        enterprise(lang)

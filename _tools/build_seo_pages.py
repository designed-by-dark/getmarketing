#!/usr/bin/env python3
"""Build the topic pages from _content/*.md.

  python3 _tools/build_seo_pages.py

- Every markdown file becomes /<slug>/index.html (slug = file name).
- marketing-plan-generator.md and marketingplan-erstellen.md are tool pages that already exist:
  their text goes into the page's SEO section, and title/description are updated.
- Also writes sitemap.xml and robots.txt.
Markdown format: first lines "TITLE: ..." and "DESCRIPTION: ...", then "# H1", intro, "[ Button ]" lines.
"""
import html, json, re, pathlib, datetime, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from no_orphans import fix as no_orphans

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

# ---------- Landing page template: homepage design, homepage sales sections ----------
HOME_FILE = {"en": ROOT / "index.html", "de": ROOT / "de" / "index.html"}
# homepage sections every landing page carries after its own content (in this order)
HOME_SECTIONS = ["offer-section", "lead-section"]
LP = {
 "en": dict(facts="Free demo and website analysis · reply within 3 working days", ph="yourcompany.com", btn="Check my website for free",
            dare='Prefer to start on your own? <a href="/marketing-plan-generator/">Generate your marketing plan in seconds&nbsp;→</a>',
            mid_h="Rather have it done for you?", mid_p="Send us your website. Within 3 working days you know what is costing you enquiries, and what to do about it.",
            mid_btn="Get my free analysis", app="https://app.getmarketing.team", tool_btn="Generate my marketing plan", tool_facts="Free · ready in seconds", tool_dare='Rather have it done for you? <a href="#start">Get a free website analysis&nbsp;→</a>', faq_k="FAQ", how_k="How it works", cmp_k="Comparison", who_k="Who it is for"),
 "de": dict(facts="Kostenlose Demo und Website-Analyse · Antwort in 3 Werktagen", ph="deinefirma.de", btn="Website kostenlos prüfen",
            dare='Lieber erst selbst loslegen? <a href="/marketingplan-erstellen/">Erstelle deinen Marketingplan in Sekunden&nbsp;→</a>',
            mid_h="Lieber machen lassen?", mid_p="Schick uns deine Website. In 3 Werktagen weißt du, was dich Anfragen kostet, und was dagegen hilft.",
            mid_btn="Kostenlose Analyse anfordern", app="https://app.getmarketing.team", tool_btn="Marketingplan erstellen", tool_facts="Kostenlos · in Sekunden fertig", tool_dare='Lieber machen lassen? <a href="#start">Kostenlose Website-Analyse anfordern&nbsp;→</a>', faq_k="FAQ", how_k="So läuft es", cmp_k="Vergleich", who_k="Für wen"),
}
_HOME = {}

def home_parts(lang):
    if lang in _HOME: return _HOME[lang]
    s = HOME_FILE[lang].read_text()
    home = T[lang]["home"]
    nav = re.search(r"<nav>.*?</nav>", s, re.S).group(0)
    nav = nav.replace('class="nav-logo"', 'class="nav-logo"', 1).replace('<a href="#" class="nav-logo">', f'<a href="{home}" class="nav-logo">')
    dash = re.search(r'(<div class="dash" id="ccal".*?)\n  </div>\n</header>', s, re.S).group(1)
    secs = []
    for key in HOME_SECTIONS:
        m = re.search(r'<section[^>]*' + (key if "=" in key else f'class="{key}"') + r'[^>]*>.*?</section>', s, re.S)
        assert m, (lang, key); secs.append(m.group(0))
    foot = re.search(r'<footer class="ft">.*?</footer>', s, re.S).group(0).replace('<a href="#" class="ft-logo">', f'<a href="{home}" class="ft-logo">')
    _HOME[lang] = dict(nav=nav, dash=dash, sections="\n\n".join(secs), footer=foot)
    return _HOME[lang]

def nav_for(lang, alt):
    nav = home_parts(lang)["nav"]
    return re.sub(r'(<a href=")[^"]*(" class="nav-lang")', lambda m: m.group(1) + alt + m.group(2), nav, count=1)

def h1_html(h1, short):
    """Put the page keyword in the lime box, like the homepage headline."""
    txt = inline(h1)
    m = re.match(r"^(.{3,40}?):\s+(.+)$", txt)
    if m: return f'<span class="hl">{m.group(1)}</span> <span class="h1-rest">{m.group(2)}</span>'
    for key in sorted({short, re.sub(r"^(The|Der|Die|Das|Dein|Your|An|Ein)\s+", "", short)}, key=len, reverse=True):
        k = re.search(re.escape(key), txt, re.I)
        if k and len(key) >= 5: return txt[:k.start()] + f'<span class="hl">{txt[k.start():k.end()]}</span>' + txt[k.end():]
    return txt

def short_title(title, h1):
    s = re.split(r"\s[|:–—]\s|:\s", title)[0].strip()
    return s if len(s) <= 48 else plain(h1)[:48].rsplit(" ", 1)[0]

def is_faq(h2, lang): return any(w in h2.lower() for w in T[lang]["faq_words"])

def sections_of(body):
    out, cur = [], None
    for k, v in body:
        if k == "h2": cur = [v, []]; out.append(cur)
        elif cur is None: cur = ["", [(k, v)]]; out.append(cur)
        else: cur[1].append((k, v))
    return out

BOLD_LEAD = re.compile(r"^\*\*(.+?)\*\*[:.]?\s*(.*)$")

def card_items(items):
    """['**Title:** text', ...] -> [(title, text)] when every item starts bold, else None"""
    out = []
    for x in items:
        m = BOLD_LEAD.match(x)
        if not m: return None
        out.append((m.group(1).rstrip(":."), m.group(2)))
    return out

def step_paras(blocks):
    """paragraphs like '**1. Diagnosis.** text' -> [(title, text)]"""
    out = []
    for k, v in blocks:
        if k != "p": continue
        m = re.match(r"^\*\*(?:\d+\.|Step \d+:|Schritt \d+:)\s*(.+?)\*\*\s*(.*)$", " ".join(v))
        if m: out.append((m.group(1).rstrip(":."), m.group(2)))
    return out

BOLT = '<svg viewBox="0 0 100 150" aria-hidden="true"><path d="M62 0 8 86h36L30 150 92 58H56z"/></svg>'

def render_section(h2, blocks, lang, faq, idx):
    """One H2 section of the markdown as a landing-page block."""
    L = LP[lang]; head = f'<h2>{inline(h2)}</h2>' if h2 else ""
    kinds = [k for k, _ in blocks]
    # FAQ
    if h2 and is_faq(h2, lang):
        pairs = faq_pairs(blocks)
        if pairs:
            faq.extend(pairs)
            items = "".join(f'<details{" open" if i == 0 else ""}><summary>{inline(q)}</summary>' + "".join(f"<p>{inline(a)}</p>" for a in ans) + "</details>" for i, (q, ans) in enumerate(pairs))
            return f'<section class="lp-sec lp-faq"><div class="wrap lp-faq-grid"><div class="lp-faq-head reveal"><span class="lp-k">{L["faq_k"]}</span>{head}</div><div class="lp-faq-list">{items}</div></div></section>'
    steps = step_paras(blocks)
    paras = [b for b in blocks if b[0] == "p" and not step_paras([b])]
    lists = [b for b in blocks if b[0] in ("ul", "ol")]
    tables = [b for b in blocks if b[0] == "table"]
    def text_html(bs):
        out = []
        for k, v in bs:
            if k == "p" and BOLD_LEAD.match(" ".join(v)) and len(" ".join(v)) < 600:
                m = BOLD_LEAD.match(" ".join(v)); item = f'<div class="lp-def"><b>{inline(m.group(1).rstrip(":."))}</b><p>{inline(m.group(2))}</p></div>'
                if out and out[-1].startswith('<div class="lp-defs">'): out[-1] = out[-1][:-6] + item + "</div>"
                else: out.append(f'<div class="lp-defs">{item}</div>')
                continue
            if k == "p":
                t = " ".join(v)
                q = re.match(r'^[„"“](.+?)[“"”]\s*(.*)$', t)
                if q and len(t) < 300: out.append(f'<blockquote class="lp-quote"><p>{"„" if lang == "de" else "“"}{inline(q.group(1))}{"“" if lang == "de" else "”"}</p><cite>{inline(q.group(2))}</cite></blockquote>')
                else: out.append(f"<p>{inline(t)}</p>")
            elif k == "h3": out.append(f"<h3>{inline(v)}</h3>")
            elif k == "cta":
                b, n = cta_buttons(v, lang); out.append(f'<div class="lp-inline-cta">{b[0]}</div>')
        return "".join(out)
    def list_html(k, items):
        cards = card_items(items)
        if cards and k == "ol":
            step_w = "Schritt" if lang == "de" else "Step"
            return f'<div class="lpc-steps" style="--n:{min(len(cards), 5)}">' + "".join(f'<div class="lpc-step reveal"><span class="lpc-chip"><span class="bolt-badge">{BOLT}</span>{step_w} {i + 1}</span><h3>{inline(a)}</h3><p>{inline(b)}</p></div>' for i, (a, b) in enumerate(cards)) + "</div>"
        if cards:
            cls = "lpc-cards"
            return f'<div class="{cls}">' + "".join(f'<div class="lpc-card reveal">{f"<span class=lp-num>{i + 1:02d}</span>" if k == "ol" else ""}<h3>{inline(a)}</h3><p>{inline(b)}</p></div>' for i, (a, b) in enumerate(cards)) + "</div>"
        if k == "ol":
            return '<ol class="lp-olist">' + "".join(f"<li><span>{i + 1}</span><p>{inline(x)}</p></li>" for i, x in enumerate(items)) + "</ol>"
        return '<ul class="lp-checks">' + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"
    # comparison table
    if tables:
        head_row, *rows = tables[0][1]
        gm = next((i for i, c in enumerate(head_row) if "getmarketing" in c.lower()), None)
        def td(i, c, tag="td"): return f'<{tag}{" class=gm" if i == gm else ""}>{inline(c)}</{tag}>'
        tbl = '<div class="lp-table reveal"><table><thead><tr>' + "".join(td(i, c, "th") for i, c in enumerate(head_row)) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(td(i, c) for i, c in enumerate(r)) + "</tr>" for r in rows) + "</tbody></table></div>"
        rest = [b for b in blocks if b[0] != "table"]
        before = []; after = []; seen = False
        for b in blocks:
            if b[0] == "table": seen = True; continue
            (after if seen else before).append(b)
        def mix(bs): return "".join(list_html(k, v) if k in ("ul", "ol") else text_html([(k, v)]) for k, v in bs)
        return f'<section class="lp-sec lp-cmp"><div class="wrap"><div class="sec-head reveal"><span class="lp-k">{L["cmp_k"]}</span>{head}<div class="lp-lead">{mix(before)}</div></div>{tbl}<div class="lp-after">{mix(after)}</div></div></section>'
    # numbered steps written as bold paragraphs
    if len(steps) >= 3:
        step_w = "Schritt" if lang == "de" else "Step"
        cards = "".join(f'<div class="lpc-step reveal"><span class="lpc-chip"><span class="bolt-badge">{BOLT}</span>{step_w} {i + 1}</span><h3>{inline(a)}</h3><p>{inline(b)}</p></div>' for i, (a, b) in enumerate(steps))
        return f'<section class="lp-sec lpc-steps-sec"><div class="wrap"><div class="sec-head reveal"><span class="lp-k">{L["how_k"]}</span>{head}<div class="lp-lead">{text_html(paras)}</div></div><div class="lpc-steps" style="--n:{min(len(steps), 5)}">{cards}</div></div></section>'
    # list-led section: cards or checks next to the text
    if lists:
        body_bits = []
        for k, v in blocks:
            body_bits.append(list_html(k, v) if k in ("ul", "ol") else text_html([(k, v)]))
        has_cards = any(card_items(v) for _, v in lists)
        if has_cards or lists[0][0] == "ol":
            return f'<section class="lp-sec"><div class="wrap"><div class="sec-head reveal">{head}</div><div class="lp-body">{"".join(body_bits)}</div></div></section>'
        return f'<section class="lp-sec lp-split{" lp-flip" if idx % 3 == 1 else ""}"><div class="wrap lp-split-grid"><div class="lp-split-head reveal">{head}</div><div class="lp-split-body reveal">{"".join(body_bits)}</div></div></section>'
    # quote-only section
    if paras and all(re.match(r'^[„"“]', " ".join(v)) for _, v in paras):
        return f'<section class="lp-sec lp-quote-sec"><div class="wrap reveal">{text_html(blocks)}</div></section>'
    # text-only section
    return f'<section class="lp-sec lp-split{" lp-flip" if idx % 3 == 1 else ""}"><div class="wrap lp-split-grid"><div class="lp-split-head reveal">{head}</div><div class="lp-split-body lp-prose reveal">{text_html(blocks)}</div></div></section>'

def mid_cta(lang):
    L = LP[lang]; t = T[lang]
    return f'<section class="lp-mid"><div class="wrap reveal"><div><h2>{L["mid_h"]}</h2><p>{L["mid_p"]}</p></div><a href="#start" class="btn-hero">{L["mid_btn"]} →</a></div></section>'

MKT = {
 "en": dict(tag="Market scan", ex="Example", site="yourcompany.com", region="Germany", scanning="Scanning your market",
   steps=[("Search demand in your niche", "1,240 queries"), ("Competitors on Google", "8 companies"),
          ("Mentions in AI answers", "ChatGPT · Perplexity · Gemini"), ("Gaps competitors leave open", "23 topics")],
   opp="Biggest opportunities", cols=("Search query", "per month", "Competition"),
   rows=[("commercial cleaning Munich", "880", "low"), ("office cleaning company", "1,300", "medium"),
         ("cost of commercial cleaning", "590", "low"), ("eco cleaning for businesses", "320", "low")],
   vis="Visibility in your market", bars=[("Competitor A", 64), ("Competitor B", 41), ("You", 9)],
   done="Plan ready: 3 priorities for the next 90 days"),
 "de": dict(tag="Marktanalyse", ex="Beispiel", site="deinefirma.de", region="Deutschland", scanning="Dein Markt wird analysiert",
   steps=[("Suchnachfrage in deiner Nische", "1.240 Suchanfragen"), ("Wettbewerber bei Google", "8 Unternehmen"),
          ("Nennungen in KI-Antworten", "ChatGPT · Perplexity · Gemini"), ("Lücken, die Wettbewerber offen lassen", "23 Themen")],
   opp="Größte Chancen", cols=("Suchanfrage", "pro Monat", "Wettbewerb"),
   rows=[("Gebäudereinigung München", "880", "gering"), ("Büroreinigung Firma", "1.300", "mittel"),
         ("Gebäudereinigung Kosten", "590", "gering"), ("nachhaltige Reinigung Unternehmen", "320", "gering")],
   vis="Sichtbarkeit in deinem Markt", bars=[("Wettbewerber A", 64), ("Wettbewerber B", 41), ("Du", 9)],
   done="Plan fertig: 3 Prioritäten für die nächsten 90 Tage"),
}

def market_demo(lang):
    M = MKT[lang]; d = 0.0
    def nd():
        nonlocal d; d += 0.35; return f"{d:.2f}s"
    steps = "".join(f'<li class="mk-in" style="--d:{nd()}"><span class="mk-ok">✓</span><span>{esc(a)}</span><b>{esc(b)}</b></li>' for a, b in M["steps"])
    rows = "".join(f'<tr class="mk-in" style="--d:{nd()}"><td>{esc(q)}</td><td>{esc(v)}</td><td><span class="mk-lvl mk-{"lo" if c in ("low", "gering") else "mid"}">{esc(c)}</span></td></tr>' for q, v, c in M["rows"])
    bars = "".join(f'<div class="mk-bar mk-in{" mk-you" if i == len(M["bars"]) - 1 else ""}" style="--d:{nd()};--w:{w}%"><span>{esc(n)}</span><i><em></em></i><b>{w}%</b></div>' for i, (n, w) in enumerate(M["bars"]))
    return f'''<div class="mkt-demo" aria-label="{esc(M["tag"])} ({esc(M["ex"])})">
      <div class="mk-top"><span class="mk-tag">{esc(M["tag"])}</span><span class="mk-search"><svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="9" cy="9" r="6"/><path d="m14 14 4 4"/></svg>{esc(M["site"])} · {esc(M["region"])}</span><span class="mk-ex">{esc(M["ex"])}</span></div>
      <div class="mk-grid">
        <div class="mk-col"><p class="mk-h">{esc(M["scanning"])}</p><div class="mk-prog"><i></i></div><ul class="mk-steps">{steps}</ul>
          <p class="mk-h mk-h2">{esc(M["vis"])}</p>{bars}</div>
        <div class="mk-col mk-panel"><p class="mk-h">{esc(M["opp"])}</p><table class="mk-table"><thead><tr><th>{esc(M["cols"][0])}</th><th>{esc(M["cols"][1])}</th><th>{esc(M["cols"][2])}</th></tr></thead><tbody>{rows}</tbody></table>
          <p class="mk-done mk-in" style="--d:{nd()}"><span class="bolt-badge">{BOLT}</span>{esc(M["done"])}</p></div>
      </div>
    </div>'''

def build_page(p, pages):
    lang, t, L = p["lang"], T[p["lang"]], LP[p["lang"]]
    h1, intro, hero_cta, body, closing = split_page(p["blocks"])
    notes = cta_buttons(hero_cta, lang)[1] if hero_cta else []
    labels = re.findall(r"\[\s*([^\]]+?)\s*\]", hero_cta or "")
    btn = labels[0] if labels and "plan" not in labels[0].lower() else L["btn"]
    # proof line right after the hero CTA ("55+ projects · 383,000 ...")
    proof = ""
    if body and body[0][0] == "p" and "·" in " ".join(body[0][1]) and re.search(r"\d", " ".join(body[0][1])):
        proof = "".join(f"<li>{inline(x.strip())}</li>" for x in " ".join(body[0][1]).split("·")); body = body[1:]
    sents = re.split(r"(?<=[.!?])\s+", " ".join(intro))
    hero_txt, n = sents[0], 1
    while n < len(sents) and len(hero_txt) + len(sents[n]) <= 260: hero_txt += " " + sents[n]; n += 1
    intro_html = inline(hero_txt)
    faq = []
    secs = sections_of(body)
    if n < len(sents):
        lead = ("p", [" ".join(sents[n:])])
        if secs and not secs[0][0]: secs[0][1].insert(0, lead)
        elif secs: secs[0][1].insert(0, lead)
    close_p = t["band_p"]
    if closing is None and secs and secs[-1][0] and not is_faq(secs[-1][0], lang) and all(k in ("p", "cta") for k, _ in secs[-1][1]):
        txt = " ".join(" ".join(v) if k == "p" else v for k, v in secs[-1][1])
        if "[" in txt:
            closing = (secs[-1][0], ""); secs = secs[:-1]
            rest = re.sub(r"\[[^\]]*\]", "", txt).strip(" ·")
            if rest: close_p = inline(rest)
    blocks_html = []
    for i, (h2, bs) in enumerate(secs):
        blocks_html.append(render_section(h2, bs, lang, faq, i))
        if len(secs) >= 7 and i == len(secs) // 2 - 1: blocks_html.append(mid_cta(lang))
    url = f'{SITE}/{p["slug"]}/'
    alt = "/" + ALT[p["slug"]] + "/"
    de_s, en_s = (p["slug"], ALT[p["slug"]]) if lang == "de" else (ALT[p["slug"]], p["slug"])
    hreflang = (f'<link rel="alternate" hreflang="de" href="{SITE}/{de_s}/" />\n<link rel="alternate" hreflang="en" href="{SITE}/{en_s}/" />\n'
                f'<link rel="alternate" hreflang="x-default" href="{SITE}/{en_s}/" />')
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": p["title"], "description": p["desc"], "url": url, "inLanguage": lang,
           "dateModified": TODAY, "publisher": {"@type": "Organization", "name": "GetMarketing", "url": SITE, "logo": SITE + "/logo.jpg"}}]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(" ".join(a))}} for q, a in faq]})
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    facts = L["facts"]
    H = home_parts(lang)
    tool = p["slug"] in TOOL_PAGES
    form = f'<form class="hero-url" action="#start" data-lead-prefill><input type="text" name="website" inputmode="url" autocomplete="url" placeholder="{L["ph"]}" aria-label="Website"><button type="submit" class="btn-hero">{esc(btn)}</button></form>'
    app_btn = f'<a href="{L["app"]}" class="btn-hero lp-app-btn">{esc(L["tool_btn"])} →</a>'
    hero_action = app_btn if tool else form
    dare = L["tool_dare"] if tool else L["dare"]
    if tool: facts = L["tool_facts"]
    closing_html = ""
    if closing:
        closing_html = f'<section class="lp-close"><div class="wrap reveal"><h2>{inline(closing[0])}</h2><p>{close_p}</p>{app_btn if tool else form}</div></section>'
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
<link rel="stylesheet" href="/home.css?v=1" />
<link rel="stylesheet" href="/home-hero.css?v=14" />
<link rel="stylesheet" href="/theme.css?v=20" />
<link rel="stylesheet" href="/landing.css?v=4" />
{ld_html}
<script defer src="/content-calendar.js?v=9"></script>
<script defer src="/dash-demo.js?v=1"></script>
<script defer src="/site.js?v=1"></script>
<script defer src="/home.js?v=10"></script>
<script defer src="/analytics.js"></script>
<script defer src="/nav-menu.js?v=2"></script>
</head>
<body class="lp">
<!-- generated from _content/{p["file"]} by _tools/build_seo_pages.py, edit the markdown, not this file -->
{nav_for(lang, alt)}

<header class="hero hero-light lp-hero">
  <div class="wrap">
    <h1>{h1_html(h1, p["short"])}</h1>
    <p class="sub">{intro_html}</p>
    <div class="hero-row">
      {hero_action}<p class="hero-facts">{esc(facts)}</p>
    </div>
    <p class="hero-dare">{dare}</p>
    {f'<ul class="lp-proof">{proof}</ul>' if proof else ""}
    {market_demo(lang) if tool else H["dash"]}
  </div>
</header>

{"".join(blocks_html)}

{closing_html}

{H["sections"]}

{H["footer"]}
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
    path.write_text(no_orphans(s))

def main():
    pages = []
    for f in sorted(SRC.glob("*.md")):
        meta, blocks = parse(f.read_text())
        slug = f.stem; lang = "de" if slug in DE_SLUGS else "en"
        h1 = next(v for k, v in blocks if k == "h1")
        pages.append(dict(file=f.name, slug=slug, lang=lang, blocks=blocks, title=meta.get("title", plain(h1)), desc=meta.get("description", ""), short=SHORT.get(slug) or short_title(meta.get("title", h1), h1)))
    for p in pages:
        html_out = build_page(p, pages)
        if p["slug"] in TOOL_PAGES: html_out = html_out.replace(f'href="{T[p["lang"]]["plan"]}" class="btn-lime"', f'href="{LP[p["lang"]]["app"]}" class="btn-lime"')
        out = ROOT / p["slug"] / "index.html"; out.parent.mkdir(exist_ok=True); out.write_text(no_orphans(html_out)); print("page", p["slug"])
    urls = ["/", "/de/", "/partners/", "/press/", "/de/presse/", "/de/partners/"] + [f'/{p["slug"]}/' for p in pages]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(len(urls), "urls in sitemap")

if __name__ == "__main__":
    main()

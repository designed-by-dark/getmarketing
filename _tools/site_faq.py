"""FAQ copy shared by the homepage and the pricing page (EN + DE).

Answers come from the offer structure (getmarketing-research/angebot-struktur-de.md, sections 2, 5 and 8).
Only describe what really exists. Edit here, then run:
  python3 _tools/apply_faq.py && python3 _tools/build_static_pages.py && python3 _tools/build_seo_pages.py
"""
import html, json, re

FAQ = {
 "en": [
  ("Do I have to write the content myself, or do I just get a plan?",
   "You write nothing yourself. GetMarketing writes the pages and posts, checks every draft automatically for facts, brand and SEO, and puts it in front of you. You approve with one click and the page goes live in your&nbsp;CMS."),
  ("Why not just use ChatGPT or Claude?",
   "ChatGPT answers what you ask. You still have to know what to do and set aside time for it every week, and that is usually what is missing. GetMarketing decides from real search data what comes next, does it on a schedule, publishes in your CMS, measures the result, warns you when visibility drops and learns from your&nbsp;corrections."),
  ("Is this all of my marketing?",
   "No, and on purpose. We cover the channels that proved to be the most important 20% in our projects: Google, AI answers and LinkedIn. More channels would mean more decisions and more approvals for you, the opposite of the relief you want from&nbsp;us."),
  ("Do you make videos?",
   "No. No client has asked for it, AI video is exactly the generic output people complain about, and a video stops working long before a page that ranks. LinkedIn posts come with image&nbsp;suggestions."),
  ("Do you run paid ads?",
   "Not in the software, because that means responsibility for your ad budget and access to your ad accounts. With <a href=\"/enterprise/\">Enterprise</a>, Google Ads and Google Shopping are available as an&nbsp;add-on."),
  ("Does it change code on my website, or only text?",
   "We change content and SEO settings through your CMS, not your theme code: new pages and posts, titles, meta descriptions, headings, alt texts, redirects and schema markup on new pages. Every change shows before and after and can be undone with one click. Theme code, page speed and robots.txt come as a ready brief for your developer, or we do it for you with&nbsp;Enterprise."),
  ("Which systems does it work with?",
   "WordPress and Shopify at launch, with direct publishing. TYPO3 and Webflow follow later. For any other CMS you get every page as HTML or Markdown to paste in. Data comes from Google Search Console. LinkedIn posts you copy and post yourself, nothing is posted&nbsp;automatically."),
  ("When will I see results?",
   "The analysis and the first fixes come right away. More traffic and enquiries from new pages usually take 3 to 6 months, because Google needs time to trust new pages. The monthly report shows what is live, what ranks and which enquiries came in, so you see early what&nbsp;works."),
  ("Is there a cheaper plan for small companies or startups?",
   "No. €249 a month per domain, or €2,490 a year with two months free. Our costs depend on domains and pages, not on headcount, so there is no plan by company size. If you have no revenue yet, start with the free <a href=\"/marketing-plan-generator/\">marketing plan generator</a>."),
  ("Can I cancel, and what happens to my content?",
   "You can cancel monthly. Everything that was published belongs to you and stays&nbsp;online."),
 ],
 "de": [
  ("Muss ich den Content selbst schreiben, oder bekomme ich nur einen Plan?",
   "Du schreibst nichts selbst. GetMarketing schreibt die Seiten und Beiträge, prüft jeden Entwurf automatisch auf Fakten, Marke und SEO und legt ihn dir vor. Du gibst mit einem Klick frei, und die Seite geht in deinem CMS&nbsp;live."),
  ("Warum nicht einfach selbst mit ChatGPT oder Claude?",
   "ChatGPT beantwortet, was du fragst. Du musst trotzdem wissen, was zu tun ist, und dir jede Woche Zeit dafür nehmen, und genau das fehlt meistens. GetMarketing entscheidet anhand echter Suchdaten, was als Nächstes dran ist, macht es regelmäßig, veröffentlicht in deinem CMS, misst das Ergebnis, warnt bei Sichtbarkeitsverlust und lernt aus deinen&nbsp;Korrekturen."),
  ("Ist das mein komplettes Marketing?",
   "Nein, und das mit Absicht. Wir machen die Kanäle, die sich in unseren Projekten als die wichtigsten 20 % erwiesen haben: Google, KI-Antworten und LinkedIn. Mehr Kanäle hießen mehr Entscheidungen und mehr Freigaben für dich, also das Gegenteil der Entlastung, die du von uns&nbsp;willst."),
  ("Macht ihr auch Videos?",
   "Nein. Kein Kunde hat danach gefragt, KI-Video ist genau der generische Output, über den sich alle beschweren, und ein Video wirkt viel kürzer als eine Seite, die rankt. Zu LinkedIn-Posts gibt es&nbsp;Bildvorschläge."),
  ("Schaltet ihr auch Werbung?",
   "Nicht in der Software, denn das hieße Verantwortung für dein Werbebudget und Zugriff auf deine Werbekonten. Bei <a href=\"/de/enterprise/\">Enterprise</a> gibt es Google Ads und Google Shopping als&nbsp;Add-on."),
  ("Ändert ihr Code auf meiner Website oder nur Texte?",
   "Wir ändern Inhalte und SEO-Einstellungen über dein CMS, nicht den Code deines Themes: neue Seiten und Beiträge, Titles, Meta-Beschreibungen, Überschriften, Alt-Texte, Weiterleitungen und Schema-Markup in neuen Seiten. Jede Änderung zeigt vorher und nachher und lässt sich mit einem Klick zurücknehmen. Theme-Code, Ladezeit und robots.txt kommen als fertige Anleitung für deinen Entwickler, oder wir setzen es bei Enterprise für dich&nbsp;um."),
  ("Mit welchen Systemen funktioniert das?",
   "Zum Start WordPress und Shopify, mit direkter Veröffentlichung. TYPO3 und Webflow folgen später. Für jedes andere CMS bekommst du jede Seite als HTML oder Markdown zum Einfügen. Die Daten kommen aus der Google Search Console. LinkedIn-Posts kopierst und postest du selbst, automatisch gepostet wird&nbsp;nichts."),
  ("Wann sehe ich Ergebnisse?",
   "Die Analyse und die ersten Fixes kommen sofort. Mehr Traffic und Anfragen über neue Seiten dauern meist 3 bis 6 Monate, weil Google neuen Seiten erst vertrauen muss. Der Monatsbericht zeigt, was live ist, was rankt und welche Anfragen kamen, so siehst du früh, was&nbsp;wirkt."),
  ("Gibt es einen günstigeren Tarif für kleine Firmen oder Startups?",
   "Nein. 249 € im Monat pro Domain, oder 2.490 € im Jahr mit zwei Monaten gratis. Unsere Kosten hängen von Domains und Seiten ab, nicht von der Zahl der Mitarbeitenden, deshalb gibt es keinen Tarif nach Größe. Wenn du noch keinen Umsatz hast, starte mit dem kostenlosen <a href=\"/marketingplan-erstellen/\">Marketingplan-Generator</a>."),
  ("Kann ich kündigen, und was passiert mit meinen Inhalten?",
   "Du kannst monatlich kündigen. Alles, was veröffentlicht wurde, gehört dir und bleibt&nbsp;online."),
 ],
}

HEAD = {
 "en": ("FAQ", "Questions we hear&nbsp;most"),
 "de": ("FAQ", "Die häufigsten&nbsp;Fragen"),
}


def _plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).replace("\xa0", " ")


def faq_section(lang, items=None, sec_id="faq"):
    items = items or FAQ[lang]
    k, h2 = HEAD[lang]
    det = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(items))
    return (f'<section class="lp-sec lp-faq" id="{sec_id}"><div class="wrap lp-faq-grid"><div class="lp-faq-head reveal">'
            f'<span class="lp-k">{k}</span><h2>{h2}</h2></div><div class="lp-faq-list">{det}</div></div></section>')


def faq_ld(lang, items=None):
    items = items or FAQ[lang]
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": _plain(q), "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}} for q, a in items]}
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=1) + "\n</script>"

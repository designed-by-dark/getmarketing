"""Enterprise page (EN + DE), built with the homepage design language.

Called from build_static_pages.enterprise(lang). Copy lives here, layout CSS in ENT_CSS.
"""
import re
import build_static_pages as S

ENT_CSS = """<style>
  /* hero: floating widgets around the headline (Adwise-style) */
  .lp-hero { position: relative; }
  .hx { position: absolute; z-index: 2; width: 210px; border-radius: 16px; padding: 14px 16px; font-size: 12.5px; text-align: left;
        background: radial-gradient(140px 100px at 90% 0%, rgba(82,183,136,.30), transparent 70%), #141A16; color: #fff;
        box-shadow: 0 24px 48px -24px rgba(0,0,0,.7), inset 0 0 0 1px rgba(255,255,255,.06); }
  .hx small { display: block; font-size: 11px; color: rgba(255,255,255,.55); }
  .hx b { display: block; margin-top: 4px; font-size: 24px; font-weight: 500; letter-spacing: -.03em; }
  .hx p { margin-top: 6px; font-size: 12.5px; line-height: 1.4; color: rgba(255,255,255,.88); }
  .hx em { display: inline-block; margin-top: 8px; font-style: normal; font-size: 10.5px; font-weight: 700; color: var(--lime-ink); background: var(--lime); border-radius: 6px; padding: 3px 7px; }
  .hx .cs-bars { height: 42px; margin-top: 10px; }
  .hx-chk { display: grid; gap: 5px; margin-top: 8px; }
  .hx-chk span { display: flex; justify-content: space-between; color: rgba(255,255,255,.8); }
  .hx-chk span::after { content: "✓"; color: var(--lime); font-weight: 700; }
  .hx-vis { width: 150px; height: 64px; margin-top: 8px; border-radius: 10px; background: linear-gradient(135deg, #1B4332, #52B788 60%, #C6F25A); }
  .hx-1 { left: max(24px, calc(50% - 690px)); top: 200px; transform: rotate(-4deg); }
  .hx-2 { right: max(24px, calc(50% - 690px)); top: 150px; transform: rotate(3deg); }
  .hx-3 { left: max(24px, calc(50% - 650px)); bottom: 44px; transform: rotate(2deg); }
  .hx-4 { right: max(24px, calc(50% - 660px)); bottom: 70px; transform: rotate(-3deg); }
  @media (max-width: 1380px) { .hx { display: none; } }

  /* section heads */
  .ent-head { max-width: 780px; margin: 0 auto 44px; text-align: center; }
  .ent-head h2 { font-weight: 600; font-size: clamp(32px, 4.2vw, 56px); letter-spacing: -0.04em; line-height: 1.05; color: #111; }
  .ent-head h2 em { font-style: normal; background: var(--lime); color: var(--lime-ink); padding: 0 .2em .04em; border-radius: 6px; display: inline-block; transform: rotate(-1.2deg); }
  .ent-head p { margin-top: 16px; font-size: 17px; line-height: 1.6; color: #4A504C; }
  .ent-sec { padding: 96px 0 0; }

  /* workflow cards: text left, product mockup bleeding off the right */
  .wf-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .wf { position: relative; overflow: hidden; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 250px); gap: 20px; align-items: end;
        min-height: 320px; background: #fff; border-radius: 24px; padding: 34px 0 0 34px; box-shadow: var(--card-shadow); }
  .wf-txt { align-self: start; padding-bottom: 34px; }
  .wf-tag { display: inline-block; font-size: 11.5px; font-weight: 700; letter-spacing: .08em; color: var(--forest); background: #E3F1E8; border-radius: 999px; padding: 5px 11px; }
  .wf h3 { margin-top: 16px; font-weight: 500; font-size: clamp(25px, 2.4vw, 34px); letter-spacing: -0.035em; line-height: 1.08; color: #111; }
  .wf p { margin-top: 14px; font-size: 15.5px; line-height: 1.6; color: #555; }
  .wf-ui { align-self: end; border-radius: 18px 0 0 0; padding: 18px 18px 20px; font-size: 12.5px; min-height: 230px; }
  .wf-ui small { display: block; font-size: 11.5px; font-weight: 600; }
  .wf-dark { background: radial-gradient(160px 120px at 85% 0%, rgba(82,183,136,.35), transparent 70%), #121614; color: #fff; }
  .wf-dark small { color: rgba(255,255,255,.6); }
  .wf-light { background: linear-gradient(160deg, #EAF6EE, #F5FAF6); box-shadow: inset 1px 1px 0 rgba(27,67,50,.08); color: #1B2B22; }
  .wf-light small { color: var(--forest); }
  .wf-rows { list-style: none; margin: 12px 0 0; padding: 0; display: grid; gap: 7px; }
  .wf-rows li { display: flex; align-items: center; justify-content: space-between; gap: 8px; border-radius: 10px; padding: 8px 10px; line-height: 1.3; }
  .wf-dark .wf-rows li { background: rgba(255,255,255,.06); color: rgba(255,255,255,.9); }
  .wf-light .wf-rows li { background: #fff; box-shadow: 0 6px 16px -10px rgba(27,67,50,.35); }
  .wf-rows em { font-style: normal; font-size: 10.5px; font-weight: 700; border-radius: 6px; padding: 3px 7px; flex-shrink: 0; }
  .ok { color: var(--lime-ink); background: var(--lime); }
  .off { color: rgba(255,255,255,.55); background: rgba(255,255,255,.08); }
  .gr { color: var(--forest); background: #E3F1E8; }
  .wf-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
  .wf-chips span { font-size: 11px; font-weight: 600; border-radius: 999px; padding: 4px 9px; background: rgba(198,242,90,.14); color: var(--lime); }
  .wf-light .wf-chips span { background: #fff; color: var(--forest); box-shadow: 0 4px 10px -6px rgba(27,67,50,.4); }
  .wf-ui > b { display: block; margin-top: 6px; font-size: 30px; font-weight: 500; letter-spacing: -0.03em; line-height: 1; }
  .wf-ui .cs-bars { height: 96px; margin-top: 18px; }
  .wf-ai { margin-top: 10px; background: #fff; border-radius: 12px; padding: 12px; line-height: 1.45; box-shadow: 0 6px 16px -10px rgba(27,67,50,.35); }
  .wf-ai mark { background: #E3F1E8; color: var(--forest); font-weight: 600; padding: 0 3px; border-radius: 3px; }
  .wf-prod { margin-top: 10px; display: grid; grid-template-columns: 54px 1fr; gap: 10px; align-items: center; background: #fff; border-radius: 12px; padding: 10px; box-shadow: 0 6px 16px -10px rgba(27,67,50,.35); }
  .wf-prod i { width: 54px; height: 54px; border-radius: 8px; background: linear-gradient(135deg, #DDEBE2, #B7D9C4); }
  .wf-prod b { display: block; font-size: 12.5px; }
  .wf-prod span { display: block; font-size: 11.5px; color: #5C635F; margin-top: 2px; }
  .wf-tabs { display: flex; gap: 5px; margin-top: 10px; flex-wrap: wrap; }
  .wf-tabs span { font-size: 10.5px; padding: 4px 8px; border-radius: 6px; background: rgba(255,255,255,.08); color: rgba(255,255,255,.7); }
  .wf-tabs span.on { background: var(--lime); color: var(--lime-ink); font-weight: 700; }
  .wf-logo { display: inline-flex; align-items: center; gap: 7px; font-weight: 700; font-size: 13px; }
  .wf-logo::before { content: ""; width: 18px; height: 18px; border-radius: 5px; background: linear-gradient(135deg, #C6F25A, #52B788); }

  /* "doesn't sound like AI": side-by-side */
  .ai-cmp { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .ai-card { border-radius: 24px; padding: 32px; }
  .ai-bad { background: #ECECE8; color: #6B706C; }
  .ai-good { background: radial-gradient(420px 220px at 100% 0%, rgba(82,183,136,.35), transparent 70%), var(--deep); color: #fff; box-shadow: 0 30px 60px -36px rgba(13,29,21,.55); }
  .ai-card small { display: block; font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
  .ai-bad small { color: #8A8F8B; }
  .ai-good small { color: var(--lime); }
  .ai-card blockquote { margin: 16px 0 0; font-size: clamp(18px, 1.7vw, 22px); line-height: 1.45; letter-spacing: -0.01em; }
  .ai-bad blockquote { text-decoration: line-through; text-decoration-color: rgba(107,112,108,.45); }
  .ai-good blockquote { color: #fff; }
  .ai-flags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; }
  .ai-flags span { font-size: 12px; font-weight: 600; border-radius: 999px; padding: 5px 11px; }
  .ai-bad .ai-flags span { background: #fff; color: #9A4A3C; }
  .ai-good .ai-flags span { background: rgba(198,242,90,.14); color: var(--lime); }
  .ai-pts { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; margin-top: 20px; }
  .ai-pt { background: #fff; border-radius: 20px; padding: 24px 22px; box-shadow: var(--card-shadow); }
  .ai-pt b { display: block; font-size: 17px; font-weight: 650; letter-spacing: -0.02em; color: #111; }
  .ai-pt span { display: block; margin-top: 8px; font-size: 14.5px; line-height: 1.55; color: #555; }

  /* steps as a timeline */
  .tl { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; counter-reset: tl; }
  .tl-step { position: relative; background: #fff; border-radius: 22px; padding: 28px 24px; box-shadow: var(--card-shadow); }
  .tl-step:first-child { background: var(--forest); color: #fff; }
  .tl-step i { font-style: normal; display: inline-grid; place-items: center; width: 34px; height: 34px; border-radius: 10px; background: var(--lime); color: var(--lime-ink); font-weight: 800; font-size: 15px; }
  .tl-step h3 { margin-top: 18px; font-size: 21px; font-weight: 650; letter-spacing: -0.02em; color: #111; }
  .tl-step:first-child h3 { color: #fff; }
  .tl-step .tl-p { margin-top: 6px; font-size: 15px; font-weight: 700; color: var(--forest); }
  .tl-step:first-child .tl-p { color: var(--lime); }
  .tl-step ul { list-style: none; margin: 14px 0 0; padding: 0; display: grid; gap: 7px; font-size: 14.5px; line-height: 1.5; color: #555; }
  .tl-step:first-child ul { color: rgba(255,255,255,.8); }
  .tl-step li { padding-left: 18px; position: relative; }
  .tl-step li::before { content: "✓"; position: absolute; left: 0; color: var(--forest); font-weight: 700; }
  .tl-step:first-child li::before { color: var(--lime); }
  .tl-note { margin-top: 18px; text-align: center; font-size: 14.5px; color: #6B706C; }

  /* dark CTA band */
  .ent-cta { display: flex; align-items: center; justify-content: space-between; gap: 24px 40px; flex-wrap: wrap; border-radius: 28px; padding: clamp(32px, 5vw, 56px);
             background: radial-gradient(600px 300px at 100% 0%, rgba(198,242,90,.16), transparent 70%), radial-gradient(500px 260px at 0% 100%, rgba(82,183,136,.22), transparent 70%), var(--deep); color: #fff; box-shadow: 0 30px 60px -36px rgba(13,29,21,.55); }
  .ent-cta h2 { max-width: 20ch; font-weight: 600; font-size: clamp(28px, 3.4vw, 44px); letter-spacing: -0.035em; line-height: 1.08; color: #fff; }
  .ent-cta p { margin-top: 10px; color: rgba(255,255,255,.72); font-size: 16px; }
  .ent-cta .btn-hero { text-decoration: none; }
  .ent-proof { padding-top: 96px; }
  .ent-proof .rv-band { margin-top: 20px; }
  .ent-proof .g-head { max-width: 760px; }
  @media (min-width: 1001px) { .ent-proof .g-stats { grid-template-columns: repeat(4, minmax(0, 1fr)); max-width: 1000px; } }

  @media (max-width: 1000px) {
    .wf-grid, .ai-cmp { grid-template-columns: 1fr; }
    .ai-pts, .tl { grid-template-columns: 1fr 1fr; }
  }
  @media (max-width: 600px) {
    .ent-sec, .ent-proof { padding-top: 64px; }
    .wf { grid-template-columns: 1fr; padding: 28px 0 0 24px; min-height: 0; }
    .wf-txt { padding: 0 24px 0 0; }
    .wf-ui { margin-left: 18%; min-height: 0; }
    .ai-pts, .tl { grid-template-columns: 1fr; }
    .ai-card { padding: 26px 22px; }
  }
</style>"""

BARS = '<div class="cs-bars">' + "".join(f'<i style="height:{h}%"></i>' for h in (30, 36, 42, 48, 55, 62, 70, 80, 92)) + "</div>"

C = {
 "en": dict(
  title="Enterprise · GetMarketing",
  desc="Your entire marketing automated, built around your workflows, and it still doesn't sound like AI. A named person checks every text and owns the result.",
  h1='<span class="hl">Enterprise:</span> <span class="h1-rest">your entire marketing automated, and it still doesn’t sound like&nbsp;AI</span>',
  sub="We build the system around how your company works: fixes, pages, LinkedIn, newsletters, custom workflows. A named person checks every text and owns the&nbsp;result.",
  btn="Book a free diagnosis", dare='Prefer the software? <a href="/pricing/">See pricing&nbsp;→</a>',
  hx=[("Visibility", "+96%", "SISTRIX index, special machinery"), ("LinkedIn post", "Ready to post", ""), ("Draft check", "", ""), ("Website article", "Live in TYPO3", "")],
  hx_chk=["Facts", "Brand voice", "SEO"],
  proof_h='Built on <em>55+ projects</em>, not on&nbsp;prompts',
  proof_sub='Every Enterprise client works directly with Darya Kablash. We don’t name clients; the numbers come from the respective&nbsp;projects. <a class="cs-all" href="/case-studies/">All case studies&nbsp;→</a>',
  stats=[("55+", "Completed projects in B2B and e-commerce"), ("383,943", "Organic visitors a month, one online shop"), ("+96%", "Visibility, special machinery"), ("~200", "Courses sold a month via Google")],
  wf_h='Workflows we have <em>built</em> for&nbsp;clients',
  wf_sub="Every company works differently, so we build the workflow around yours. A few examples from projects and offers, without client&nbsp;names.",
  wf=[
   ("NEWS SYSTEM", "Law changes become three texts", "Every morning the system reads EU law sources, drops what creates no new obligation and turns each real change into a website article, a LinkedIn post and a newsletter item. After approval the article goes straight into&nbsp;TYPO3.",
    '<div class="wf-ui wf-dark"><small>Sources today · 14 read · 1 taken</small><ul class="wf-rows"><li>EUR-Lex · Battery passport<em class="ok">Taken</em></li><li>Trade media · Interview<em class="off">Dropped</em></li><li>Register · Notice<em class="off">Old</em></li></ul><div class="wf-chips"><span>Website</span><span>LinkedIn</span><span>Newsletter</span></div></div>'),
   ("3 BRANDS", "Three online shops, one cockpit", "Visibility recovered after a domain move, duplicates between the shops resolved, new pages for wholesale and private label, and social posts for all three brands from one&nbsp;login.",
    '<div class="wf-ui wf-light"><small>Cockpit · switch brand</small><div class="wf-chips"><span>Brand A</span><span>Brand B</span><span>Brand C</span></div><ul class="wf-rows"><li>Old URLs redirected<em class="gr">Done</em></li><li>Duplicates resolved<em class="gr">Done</em></li><li>Private label page<em class="gr">Live</em></li></ul></div>'),
   ("E-COMMERCE", "~15 new SEO pages a month", "For a jewelry shop with a large range: category pages instead of filter URLs, clear product titles and a steady flow of new pages, checked every month for what&nbsp;ranks.",
    f'<div class="wf-ui wf-dark"><small>Organic visitors</small><b>383,943</b><small>per month</small>{BARS}</div>'),
   ("B2B EXPERTISE", "Expert knowledge that AI cites", "For an industry association: existing expertise turned into articles that Google and AI answers use as a source, plus LinkedIn posts for the&nbsp;board.",
    '<div class="wf-ui wf-light"><small>AI answer</small><div class="wf-ai">Who is affected by the new rule? According to <mark>your-site.com</mark>, all manufacturers that …</div><div class="wf-chips"><span>Cited as source</span><span>Google AI Overview</span></div></div>'),
   ("SHOPPING", "Your own shop next to Amazon", "A lean shop, Google Shopping set up once and SEO running every month, so a product sold on Amazon gets a second channel that the brand&nbsp;owns.",
    '<div class="wf-ui wf-light"><small>Google Shopping</small><div class="wf-prod"><i></i><div><b>Your product</b><span>€9.95 · yourshop.com</span></div></div><ul class="wf-rows"><li>Product feed<em class="gr">Live</em></li><li>Category pages<em class="gr">Ranking</em></li></ul></div>'),
   ("WHITE LABEL", "A portal for an agency’s clients", "The agency sets the positioning. The system produces articles, posts and landing pages, and the clients see everything in a portal with the agency’s&nbsp;brand.",
    '<div class="wf-ui wf-dark"><span class="wf-logo">Your agency</span><div class="wf-tabs"><span class="on">Plan</span><span>Content</span><span>Approvals</span><span>Report</span></div><ul class="wf-rows"><li>Guide · main keyword<em class="ok">Review</em></li><li>LinkedIn post<em class="off">Planned</em></li><li>Landing page<em class="ok">Live</em></li></ul></div>')],
  ai_h='Fully automated. Still doesn’t sound like&nbsp;<em>AI</em>.',
  ai_sub="The same news, written twice. On the left, what a chatbot writes from a prompt. On the right, what the system writes from the original source, in the client’s&nbsp;voice.",
  bad=("Generic AI", "In today’s fast-paced regulatory landscape, staying compliant is more important than ever. Let’s dive into what the new battery rules mean for your business.", ["No source", "Says nothing", "Sounds like everyone"]),
  good=("Your system", "From 18 February 2027, every industrial battery over 2&nbsp;kWh needs a digital battery passport. The data comes from your suppliers, so start collecting it&nbsp;now.", ["Source: Art.&nbsp;77, EU&nbsp;2023/1542", "Your terms", "Checked by a person"]),
  pts=[("A real source", "Every text starts from your documents, the original law text or real search data, never from what a chatbot happens to know."),
       ("Your voice", "The system knows your past texts, your terms and your no-gos, so nobody has to explain them again."),
       ("A named person", "Someone reads every text before you see it and fixes what doesn’t sound right."),
       ("It learns", "What you correct once stays corrected. No mass content, only pages people actually search for.")],
  tl_h='From diagnosis to a running <em>system</em>',
  tl=[("1", "Visibility diagnosis", "Free", ["Your domain in SISTRIX, Semrush and Search Console", "What lost visibility costs you, as one number", "The levers that bring enquiries, ranked"]),
      ("2", "Foundation sprint", "from €990, one time", ["Technical clean-up: redirects, categories, duplicates", "GA4 and Search Console connected", "Strategy, page plan and your cockpit"]),
      ("3", "Ongoing work", "from €750 a month", ["Pages live in your shop or CMS", "LinkedIn posts with visuals, newsletters", "Monthly report in enquiries"]),
      ("4", "Custom workflows", "Per project", ["Built around your processes", "Like the examples above", "Run and maintained by us"])],
  tl_note="Per domain, minimum 3 months, then monthly. After the diagnosis you get a fixed&nbsp;offer.",
  cta_h="Let’s see what your marketing could run on its&nbsp;own.", cta_p="30 minutes, your real data, a concrete&nbsp;proposal.",
  it_h="One page for your&nbsp;IT", it_k="Security",
  it=["<strong>Read-only first, step by step.</strong> The diagnosis needs only read access to Search Console. CMS access comes later, once the first changes are approved",
      "<strong>Every change can be undone.</strong> Each change is logged as before and after and can be rolled back with one click",
      "<strong>Content and SEO settings through your CMS.</strong> Theme code only when agreed with you, and documented",
      "<strong>Hosting in Germany</strong> at Hetzner, GDPR-compliant",
      "<strong>Nothing goes live without approval</strong>, and nothing is posted on LinkedIn automatically",
      "<strong>No lock-in.</strong> Content belongs to you and stays online after you&nbsp;cancel"],
  print_="Print this page for your IT&nbsp;team",
  cmp_h="Compared with an agency, a freelancer or a&nbsp;consultant", cmp_k="Compare",
  cmp_head=["", "What clients told us bothers them", "GetMarketing Enterprise"],
  cmp=[["Agency, €2,000–7,000 a month", "Expensive, juniors do the work, results are hard to trace", "From €750 a month, the founder checks the work&nbsp;herself"],
       ["Freelancers", "They keep changing, nobody checks them", "One system with fixed responsibility. We brief your freelancer&nbsp;too"],
       ["Consultant, about €7,000 one time", "Expensive, a concept without execution", "The diagnosis is free, execution is&nbsp;included"]],
 ),
 "de": dict(
  title="Enterprise · GetMarketing",
  desc="Dein ganzes Marketing automatisiert, um deine Abläufe herum gebaut, und es klingt trotzdem nicht nach KI. Eine feste Person prüft jeden Text und ist für das Ergebnis verantwortlich.",
  h1='<span class="hl">Enterprise:</span> <span class="h1-rest">dein ganzes Marketing automatisiert, und es klingt trotzdem nicht nach&nbsp;KI</span>',
  sub="Wir bauen das System um die Abläufe deines Unternehmens herum: Fixes, Seiten, LinkedIn, Newsletter, eigene Workflows. Eine feste Person prüft jeden Text und ist für das Ergebnis&nbsp;verantwortlich.",
  btn="Kostenlose Diagnose anfragen", dare='Lieber die Software? <a href="/de/preise/">Preise ansehen&nbsp;→</a>',
  hx=[("Sichtbarkeit", "+96 %", "SISTRIX-Index, Sondermaschinenbau"), ("LinkedIn-Post", "Bereit zum Posten", ""), ("Entwurf geprüft", "", ""), ("Fachartikel", "Live in TYPO3", "")],
  hx_chk=["Fakten", "Markenstimme", "SEO"],
  proof_h='Gebaut auf <em>55+ Projekten</em>, nicht auf&nbsp;Prompts',
  proof_sub='Jeder Enterprise-Kunde arbeitet direkt mit Darya Kablash. Kundennamen nennen wir nicht, die Zahlen stammen aus den jeweiligen&nbsp;Projekten. <a class="cs-all" href="/de/referenzen/">Alle Referenzen&nbsp;→</a>',
  stats=[("55+", "Abgeschlossene Projekte in B2B und E-Commerce"), ("383.943", "Organische Besucher im Monat, ein Onlineshop"), ("+96 %", "Sichtbarkeit, Sondermaschinenbau"), ("~200", "Verkaufte Kurse im Monat über Google")],
  wf_h='Workflows, die wir für Kunden <em>gebaut</em>&nbsp;haben',
  wf_sub="Jedes Unternehmen arbeitet anders, deshalb bauen wir den Workflow um deine Abläufe herum. Ein paar Beispiele aus Projekten und Angeboten, ohne&nbsp;Kundennamen.",
  wf=[
   ("NEWS-SYSTEM", "Aus Gesetzesänderungen werden drei Texte", "Jeden Morgen liest das System EU-Rechtsquellen, sortiert aus, was keine neue Pflicht bedeutet, und macht aus jeder echten Änderung einen Fachtext, einen LinkedIn-Post und einen Newsletter-Beitrag. Nach der Freigabe geht der Fachtext direkt in&nbsp;TYPO3.",
    '<div class="wf-ui wf-dark"><small>Quellen heute · 14 gelesen · 1 übernommen</small><ul class="wf-rows"><li>EUR-Lex · Batteriepass<em class="ok">Übernommen</em></li><li>Fachmedium · Interview<em class="off">Aussortiert</em></li><li>Register · Hinweis<em class="off">Alt</em></li></ul><div class="wf-chips"><span>Website</span><span>LinkedIn</span><span>Newsletter</span></div></div>'),
   ("3 MARKEN", "Drei Onlineshops, ein Cockpit", "Sichtbarkeit nach einem Domain-Umzug zurückgeholt, Dubletten zwischen den Shops aufgelöst, neue Seiten für Großhandel und Private Label und Social-Posts für alle drei Marken aus einem&nbsp;Login.",
    '<div class="wf-ui wf-light"><small>Cockpit · Marke wechseln</small><div class="wf-chips"><span>Marke A</span><span>Marke B</span><span>Marke C</span></div><ul class="wf-rows"><li>Alte URLs umgeleitet<em class="gr">Erledigt</em></li><li>Dubletten aufgelöst<em class="gr">Erledigt</em></li><li>Private-Label-Seite<em class="gr">Live</em></li></ul></div>'),
   ("E-COMMERCE", "~15 neue SEO-Seiten im Monat", "Für einen Schmuckshop mit großem Sortiment: Kategorieseiten statt Filter-URLs, klare Produkttitel und ein fester Rhythmus neuer Seiten, jeden Monat geprüft, was&nbsp;rankt.",
    f'<div class="wf-ui wf-dark"><small>Organische Besucher</small><b>383.943</b><small>pro Monat</small>{BARS}</div>'),
   ("B2B-FACHWISSEN", "Fachwissen, das KI zitiert", "Für einen Industrieverband: vorhandenes Fachwissen als Beiträge, die Google und KI-Antworten als Quelle nutzen, dazu LinkedIn-Posts für den&nbsp;Vorstand.",
    '<div class="wf-ui wf-light"><small>KI-Antwort</small><div class="wf-ai">Wer ist von der neuen Regel betroffen? Laut <mark>deine-seite.de</mark> alle Hersteller, die …</div><div class="wf-chips"><span>Als Quelle zitiert</span><span>Google KI-Übersicht</span></div></div>'),
   ("SHOPPING", "Eigener Shop neben Amazon", "Ein schlanker Shop, Google Shopping einmal sauber eingerichtet und SEO jeden Monat. So bekommt ein Amazon-Produkt einen zweiten Kanal, der der Marke&nbsp;gehört.",
    '<div class="wf-ui wf-light"><small>Google Shopping</small><div class="wf-prod"><i></i><div><b>Dein Produkt</b><span>9,95 € · deinshop.de</span></div></div><ul class="wf-rows"><li>Produkt-Feed<em class="gr">Live</em></li><li>Kategorieseiten<em class="gr">Rankt</em></li></ul></div>'),
   ("WHITE LABEL", "Ein Portal für die Kunden einer Agentur", "Die Agentur gibt die Positionierung vor. Das System erstellt Artikel, Posts und Landingpages, und die Kunden sehen alles in einem Portal mit der Marke der&nbsp;Agentur.",
    '<div class="wf-ui wf-dark"><span class="wf-logo">Deine Agentur</span><div class="wf-tabs"><span class="on">Plan</span><span>Inhalte</span><span>Freigaben</span><span>Report</span></div><ul class="wf-rows"><li>Ratgeber · Hauptkeyword<em class="ok">Prüfen</em></li><li>LinkedIn-Post<em class="off">Geplant</em></li><li>Landingpage<em class="ok">Live</em></li></ul></div>')],
  ai_h='Komplett automatisiert. Klingt trotzdem nicht nach&nbsp;<em>KI</em>.',
  ai_sub="Dieselbe Meldung, zweimal geschrieben. Links, was ein Chatbot aus einem Prompt macht. Rechts, was das System aus der Originalquelle schreibt, in der Sprache des&nbsp;Kunden.",
  bad=("Generische KI", "In der heutigen schnelllebigen regulatorischen Landschaft ist Compliance wichtiger denn je. Tauchen wir ein in die Frage, was die neuen Batterieregeln für dein Unternehmen bedeuten.", ["Keine Quelle", "Sagt nichts", "Klingt wie alle"]),
  good=("Dein System", "Ab dem 18. Februar 2027 braucht jede Industriebatterie über 2&nbsp;kWh einen digitalen Batteriepass. Die Daten kommen von euren Zulieferern, also fangt jetzt an, sie zu&nbsp;sammeln.", ["Quelle: Art.&nbsp;77, EU&nbsp;2023/1542", "Eure Begriffe", "Von einem Menschen geprüft"]),
  pts=[("Eine echte Quelle", "Jeder Text beginnt mit deinen Unterlagen, dem Originaltext des Gesetzes oder echten Suchdaten, nie mit dem, was ein Chatbot zufällig weiß."),
       ("Deine Sprache", "Das System kennt deine bisherigen Texte, deine Fachbegriffe und deine No-Gos. Niemand muss sie neu erklären."),
       ("Eine feste Person", "Jemand liest jeden Text, bevor du ihn siehst, und korrigiert, was nicht passt."),
       ("Es lernt dazu", "Was du einmal korrigierst, bleibt korrigiert. Keine Massenware, nur Seiten, nach denen wirklich gesucht wird.")],
  tl_h='Von der Diagnose zum laufenden <em>System</em>',
  tl=[("1", "Sichtbarkeits-Diagnose", "Kostenlos", ["Deine Domain in SISTRIX, Semrush und Search Console", "Was dich verlorene Sichtbarkeit kostet, als eine Zahl", "Die Hebel, die Anfragen bringen, priorisiert"]),
      ("2", "Fundament-Sprint", "ab 990 €, einmalig", ["Technik aufräumen: Weiterleitungen, Kategorien, Dubletten", "GA4 und Search Console angebunden", "Strategie, Seitenplan und dein Cockpit"]),
      ("3", "Laufende Umsetzung", "ab 750 € im Monat", ["Seiten live in deinem Shop oder CMS", "LinkedIn-Posts mit Visual, Newsletter", "Monatsbericht in Anfragen"]),
      ("4", "Eigene Workflows", "Pro Projekt", ["Um deine Abläufe herum gebaut", "Wie die Beispiele oben", "Von uns betrieben und gepflegt"])],
  tl_note="Pro Domain, 3 Monate Mindestlaufzeit, danach monatlich kündbar. Nach der Diagnose bekommst du ein festes&nbsp;Angebot.",
  cta_h="Schauen wir, was dein Marketing allein erledigen&nbsp;könnte.", cta_p="30 Minuten, deine echten Daten, ein konkreter&nbsp;Vorschlag.",
  it_h="Eine Seite für deine&nbsp;IT", it_k="Sicherheit",
  it=["<strong>Erst nur lesend, Schritt für Schritt.</strong> Für die Diagnose reicht ein Lesezugriff auf die Search Console. Der Zugang zum CMS kommt später, wenn die ersten Änderungen freigegeben sind",
      "<strong>Jede Änderung lässt sich zurücknehmen.</strong> Jede Änderung wird mit vorher und nachher protokolliert und lässt sich mit einem Klick rückgängig machen",
      "<strong>Inhalte und SEO-Einstellungen über dein CMS.</strong> Theme-Code nur nach Absprache mit dir und dokumentiert",
      "<strong>Hosting in Deutschland</strong> bei Hetzner, DSGVO-konform",
      "<strong>Nichts geht ohne Freigabe live</strong>, und auf LinkedIn wird nichts automatisch gepostet",
      "<strong>Kein Lock-in.</strong> Die Inhalte gehören dir und bleiben nach der Kündigung&nbsp;online"],
  print_="Diese Seite für deine IT&nbsp;drucken",
  cmp_h="Im Vergleich zu Agentur, Freelancer oder&nbsp;Berater", cmp_k="Vergleich",
  cmp_head=["", "Was Kunden daran stört", "GetMarketing Enterprise"],
  cmp=[["Agentur, 2.000–7.000 € im Monat", "Teuer, Junioren machen die Arbeit, Ergebnisse sind nicht nachvollziehbar", "Ab 750 € im Monat, die Gründerin prüft&nbsp;selbst"],
       ["Freelancer", "Wechseln ständig, niemand kontrolliert sie", "Ein System mit fester Verantwortung. Deinen Freelancer briefen wir&nbsp;mit"],
       ["Berater, ca. 7.000 € einmalig", "Teuer, Konzept ohne Umsetzung", "Die Diagnose ist kostenlos, die Umsetzung ist&nbsp;enthalten"]],
 ),
}


def head(h2, sub=""):
    return f'<div class="ent-head reveal"><h2>{h2}</h2>{f"<p>{sub}</p>" if sub else ""}</div>'


def hero_widgets(c):
    (l1, v1, s1), (l2, v2, _), (l3, _, _), (l4, v4, _) = c["hx"]
    chk = "".join(f"<span>{x}</span>" for x in c["hx_chk"])
    return (f'<div class="hx hx-1" aria-hidden="true"><small>{l1}</small><b>{v1}</b>{BARS}<p>{s1}</p></div>'
            f'<div class="hx hx-2" aria-hidden="true"><small>{l2}</small><div class="hx-vis"></div><em>{v2}</em></div>'
            f'<div class="hx hx-3" aria-hidden="true"><small>{l3}</small><div class="hx-chk">{chk}</div></div>'
            f'<div class="hx hx-4" aria-hidden="true"><small>{l4}</small><em>{v4}</em></div>')


def reviews(lang):
    s = S.HOME[lang].read_text()
    m = re.search(r'<div class="rv-band reveal">.*?</figure></div></div></div>', s, re.S)
    return m.group(0) if m else ""


def build(lang, faq_items, pre):
    c = C[lang]
    stats = "".join(f"<div><b>{n}</b><span>{l}</span></div>" for n, l in c["stats"])
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="360"/>' for x in range(0, 1001, 91))
    proof = (f'<section class="cs-section ent-proof"><div class="wrap"><div class="growth reveal"><div class="g-head"><h2>{c["proof_h"].replace("<em>", "<em>")}</h2>'
             f'<p class="sec-sub">{c["proof_sub"]}</p></div><div class="g-stats">{stats}</div>'
             '<svg class="g-curve" viewBox="0 0 1000 360" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="gFillE" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#52B788" stop-opacity=".22"/><stop offset="1" stop-color="#52B788" stop-opacity="0"/></linearGradient></defs>'
             f'<g class="g-grid">{grid}</g><path class="g-area" d="M0 340 C 420 335, 720 260, 1000 12 L1000 360 L0 360 Z" fill="url(#gFillE)"/>'
             '<path class="g-line" pathLength="1" d="M0 340 C 420 335, 720 260, 1000 12" fill="none"/></svg></div>'
             f'{reviews(lang)}</div></section>')
    wf = "".join(f'<article class="wf"><div class="wf-txt"><span class="wf-tag">{t}</span><h3>{h}</h3><p>{p}</p></div>{ui}</article>' for t, h, p, ui in c["wf"])
    workflows = f'<section class="ent-sec" id="workflows"><div class="wrap">{head(c["wf_h"], c["wf_sub"])}<div class="wf-grid reveal">{wf}</div></div></section>'
    def card(cls, d):
        lab, txt, flags = d
        return f'<div class="ai-card {cls}"><small>{lab}</small><blockquote>{txt}</blockquote><div class="ai-flags">{"".join(f"<span>{x}</span>" for x in flags)}</div></div>'
    pts = "".join(f'<div class="ai-pt"><b>{b}</b><span>{t}</span></div>' for b, t in c["pts"])
    quality = (f'<section class="ent-sec" id="quality"><div class="wrap">{head(c["ai_h"], c["ai_sub"])}'
               f'<div class="ai-cmp reveal">{card("ai-bad", c["bad"])}{card("ai-good", c["good"])}</div><div class="ai-pts reveal">{pts}</div></div></section>')
    tl = "".join(f'<div class="tl-step"><i>{n}</i><h3>{t}</h3><p class="tl-p">{p}</p>{S.ul(li, "")}</div>' for n, t, p, li in c["tl"])
    steps = f'<section class="ent-sec" id="stages"><div class="wrap">{head(c["tl_h"])}<div class="tl reveal">{tl}</div><p class="tl-note">{c["tl_note"]}</p></div></section>'
    cta = (f'<section class="ent-sec"><div class="wrap"><div class="ent-cta reveal"><div><h2>{c["cta_h"]}</h2><p>{c["cta_p"]}</p></div>'
           f'<a href="#start" class="btn-hero" data-interest="enterprise">{c["btn"]}</a></div></div></section>')
    it = S.split(c["it_h"], S.ul(c["it"]) + f'<p><a href="javascript:window.print()">{c["print_"]}</a></p>', k=c["it_k"], flip=True, sid="it")
    cmp = S.table(c["cmp_h"], c["cmp_head"], c["cmp"], k=c["cmp_k"])
    body = "\n\n".join([ENT_CSS, workflows, quality, proof, steps, cta,
                        '<div style="height:40px"></div>', it, cmp,
                        S.faq_section(lang, faq_items, sec_id="enterprise-faq"), "{LEAD}", pre])
    other = "de" if lang == "en" else "en"
    S.page(lang, "enterprise", c["title"], c["desc"], c["h1"], c["sub"],
           f'<a href="#start" class="btn-hero" data-interest="enterprise">{c["btn"]}</a>',
           c["dare"], body, [S.faq_ld(lang, faq_items)], S.PATHS["enterprise"][other], hero_extra=hero_widgets(c))

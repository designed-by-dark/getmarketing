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
  .wf h3 { margin-top: 16px; font-weight: 500; font-size: clamp(24px, 2.1vw, 30px); letter-spacing: -0.035em; line-height: 1.1; color: #111; }
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
  desc="We look at how your company works, pick the marketing work that eats your time and automate it. A named person checks every text, so it still sounds like you.",
  h1='<span class="hl">Enterprise:</span> <span class="h1-rest">marketing automation built around your&nbsp;company</span>',
  sub="We look at your setup, find the marketing work that eats your team’s time and automate it. A named person checks every text, so it still sounds like&nbsp;you.",
  btn="Book a free diagnosis", dare='Prefer the software? <a href="/pricing/">See pricing&nbsp;→</a>',
  hx=[("Visibility", "+96%", "One B2B client, SISTRIX index"), ("LinkedIn post", "Ready to post", ""), ("Draft check", "", ""), ("New article", "Live in your CMS", "")],
  hx_chk=["Facts", "Your voice", "SEO"],
  proof_h='Built on <em>55+ projects</em>, not on&nbsp;prompts',
  proof_sub='Every Enterprise client works directly with Darya Kablash. We don’t name clients; the numbers come from the respective&nbsp;projects. <a class="cs-all" href="/case-studies/">All case studies&nbsp;→</a>',
  stats=[("55+", "Completed projects in B2B and e-commerce"), ("383,943", "Organic visitors a month, one online shop"), ("+96%", "Visibility, one B2B client"), ("~200", "Courses sold a month via Google")],
  wf_h='What we could <em>automate</em> for&nbsp;you',
  wf_sub="A few ideas to start with. After the diagnosis we decide together what makes sense for your&nbsp;company.",
  wf=[
   ("CONTENT", "Your expertise becomes content", "Articles and guides from what your team already knows: documents, presentations, sales&nbsp;calls.",
    '<div class="wf-ui wf-dark"><small>Input → drafts</small><ul class="wf-rows"><li>Sales call notes<em class="ok">3 topics</em></li><li>Product sheet<em class="ok">1 guide</em></li><li>FAQ from support<em class="off">Queued</em></li></ul><div class="wf-chips"><span>Website</span><span>LinkedIn</span><span>Newsletter</span></div></div>'),
   ("LINKEDIN", "LinkedIn for management", "Posts with a finished visual every week, in the voice of your managing&nbsp;director.",
    '<div class="wf-ui wf-light"><small>This week</small><div class="wf-prod"><i></i><div><b>Post + visual</b><span>Managing director</span></div></div><ul class="wf-rows"><li>Tue · Lesson from a project<em class="gr">Ready</em></li><li>Thu · Customer question<em class="gr">Draft</em></li></ul></div>'),
   ("NEWSLETTER", "A newsletter that writes itself", "What went live this month, collected and drafted, ready to&nbsp;send.",
    '<div class="wf-ui wf-dark"><small>Newsletter · November</small><ul class="wf-rows"><li>2 new guides<em class="ok">Added</em></li><li>1 customer story<em class="ok">Added</em></li><li>Subject line<em class="off">3 options</em></li></ul></div>'),
   ("MONITORING", "Industry news, turned into posts", "The system watches your sources and turns what matters to your customers into&nbsp;content.",
    '<div class="wf-ui wf-light"><small>Sources today · 14 read · 1 taken</small><ul class="wf-rows"><li>Industry news<em class="gr">Taken</em></li><li>Competitor blog<em class="gr">Noted</em></li><li>Press release<em class="gr">Skipped</em></li></ul></div>'),
   ("SHOPS", "Many brands, one cockpit", "Several shops or brands, each with its own plan, run from one&nbsp;login.",
    '<div class="wf-ui wf-light"><small>Cockpit · switch brand</small><div class="wf-chips"><span>Brand A</span><span>Brand B</span><span>Brand C</span></div><ul class="wf-rows"><li>Category pages<em class="gr">Live</em></li><li>Social posts<em class="gr">Planned</em></li></ul></div>'),
   ("REPORTING", "Reports in enquiries, not clicks", "Every month one page: what went live, what ranks, which enquiries came&nbsp;in.",
    f'<div class="wf-ui wf-dark"><small>Organic visitors</small><b>+38%</b><small>this quarter, example</small>{BARS}</div>')],
  ai_h='Fully automated. Still doesn’t sound like&nbsp;<em>AI</em>.',
  ai_sub="The same LinkedIn post, written twice. On the left, what a chatbot writes from a prompt. On the right, what the system writes from your own&nbsp;material.",
  bad=("Generic AI", "In today’s fast-paced world, customer experience is more important than ever. Here are 5 tips to take your service to the next level 🚀", ["No source", "Says nothing", "Sounds like everyone"]),
  good=("Your system", "Three customers asked us the same question last month: how long does delivery really take? Here is the honest answer, and what we changed because of&nbsp;it.", ["From your sales calls", "Your tone", "Checked by a person"]),
  pts=[("Your material", "Every text starts from what you already have, not from what a chatbot happens to know."),
       ("Your voice", "The system learns your terms and your no-gos, so nobody has to explain them again."),
       ("A named person", "Someone reads every text before you see it and fixes what doesn’t sound right."),
       ("It learns", "What you correct once stays corrected.")],
  tl_h='How we <em>automate</em> your marketing',
  tl=[("1", "We look at your setup", "Free", ["Your website, tools and team", "Where time goes today", "What would bring the most enquiries"]),
      ("2", "We pick together", "Fixed offer", ["The first automations", "What stays with your team", "Clear scope and price"]),
      ("3", "We build it", "from €990 sprint", ["Connected to your CMS and data", "Trained on your material", "Tested before it runs"]),
      ("4", "It runs", "from €750 a month", ["A person checks every text", "You approve with one click", "Monthly report in enquiries"])],
  tl_note="Per domain, minimum 3 months, then monthly. More automations can be added any&nbsp;time.",
  cta_h="Let’s look at your&nbsp;setup.", cta_p="30 minutes. We show you what could run on its&nbsp;own.",
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
  desc="Wir schauen uns an, wie dein Unternehmen arbeitet, wählen die Marketingarbeit aus, die euch Zeit kostet, und automatisieren sie. Eine feste Person prüft jeden Text, damit er nach dir klingt.",
  h1='<span class="hl">Enterprise:</span> <span class="h1-rest">Marketing-Automatisierung, gebaut um dein&nbsp;Unternehmen</span>',
  sub="Wir schauen uns euer Setup an, finden die Marketingarbeit, die eurem Team Zeit kostet, und automatisieren sie. Eine feste Person prüft jeden Text, damit er weiter nach dir&nbsp;klingt.",
  btn="Kostenlose Diagnose anfragen", dare='Lieber die Software? <a href="/de/preise/">Preise ansehen&nbsp;→</a>',
  hx=[("Sichtbarkeit", "+96 %", "Ein B2B-Kunde, SISTRIX-Index"), ("LinkedIn-Post", "Bereit zum Posten", ""), ("Entwurf geprüft", "", ""), ("Neuer Artikel", "Live im CMS", "")],
  hx_chk=["Fakten", "Deine Sprache", "SEO"],
  proof_h='Gebaut auf <em>55+ Projekten</em>, nicht auf&nbsp;Prompts',
  proof_sub='Jeder Enterprise-Kunde arbeitet direkt mit Darya Kablash. Kundennamen nennen wir nicht, die Zahlen stammen aus den jeweiligen&nbsp;Projekten. <a class="cs-all" href="/de/referenzen/">Alle Referenzen&nbsp;→</a>',
  stats=[("55+", "Abgeschlossene Projekte in B2B und E-Commerce"), ("383.943", "Organische Besucher im Monat, ein Onlineshop"), ("+96 %", "Sichtbarkeit, ein B2B-Kunde"), ("~200", "Verkaufte Kurse im Monat über Google")],
  wf_h='Was wir für dich <em>automatisieren</em>&nbsp;könnten',
  wf_sub="Ein paar Ideen für den Anfang. Nach der Diagnose entscheiden wir gemeinsam, was für dein Unternehmen Sinn&nbsp;ergibt.",
  wf=[
   ("CONTENT", "Aus Fachwissen wird Content", "Artikel und Ratgeber aus dem, was dein Team schon weiß: Unterlagen, Präsentationen,&nbsp;Vertriebsgespräche.",
    '<div class="wf-ui wf-dark"><small>Input → Entwürfe</small><ul class="wf-rows"><li>Notizen aus dem Vertrieb<em class="ok">3 Themen</em></li><li>Produktblatt<em class="ok">1 Ratgeber</em></li><li>FAQ aus dem Support<em class="off">Geplant</em></li></ul><div class="wf-chips"><span>Website</span><span>LinkedIn</span><span>Newsletter</span></div></div>'),
   ("LINKEDIN", "LinkedIn für die Geschäftsführung", "Jede Woche Posts mit fertigem Visual, in der Sprache eurer&nbsp;Geschäftsführung.",
    '<div class="wf-ui wf-light"><small>Diese Woche</small><div class="wf-prod"><i></i><div><b>Post + Visual</b><span>Geschäftsführung</span></div></div><ul class="wf-rows"><li>Di · Learning aus einem Projekt<em class="gr">Fertig</em></li><li>Do · Kundenfrage<em class="gr">Entwurf</em></li></ul></div>'),
   ("NEWSLETTER", "Ein Newsletter, der sich selbst schreibt", "Was diesen Monat live gegangen ist, gesammelt und vorgeschrieben, bereit zum&nbsp;Versand.",
    '<div class="wf-ui wf-dark"><small>Newsletter · November</small><ul class="wf-rows"><li>2 neue Ratgeber<em class="ok">Drin</em></li><li>1 Kundengeschichte<em class="ok">Drin</em></li><li>Betreffzeile<em class="off">3 Vorschläge</em></li></ul></div>'),
   ("MONITORING", "Branchen-News werden zu Posts", "Das System beobachtet eure Quellen und macht aus dem, was eure Kunden betrifft,&nbsp;Content.",
    '<div class="wf-ui wf-light"><small>Quellen heute · 14 gelesen · 1 übernommen</small><ul class="wf-rows"><li>Branchen-News<em class="gr">Übernommen</em></li><li>Blog der Konkurrenz<em class="gr">Notiert</em></li><li>Pressemitteilung<em class="gr">Aussortiert</em></li></ul></div>'),
   ("SHOPS", "Viele Marken, ein Cockpit", "Mehrere Shops oder Marken, jede mit eigenem Plan, aus einem&nbsp;Login.",
    '<div class="wf-ui wf-light"><small>Cockpit · Marke wechseln</small><div class="wf-chips"><span>Marke A</span><span>Marke B</span><span>Marke C</span></div><ul class="wf-rows"><li>Kategorieseiten<em class="gr">Live</em></li><li>Social-Posts<em class="gr">Geplant</em></li></ul></div>'),
   ("REPORTING", "Reports in Anfragen, nicht in Klicks", "Jeden Monat eine Seite: was live ist, was rankt, welche Anfragen&nbsp;kamen.",
    f'<div class="wf-ui wf-dark"><small>Organische Besucher</small><b>+38 %</b><small>dieses Quartal, Beispiel</small>{BARS}</div>')],
  ai_h='Komplett automatisiert. Klingt trotzdem nicht nach&nbsp;<em>KI</em>.',
  ai_sub="Derselbe LinkedIn-Post, zweimal geschrieben. Links, was ein Chatbot aus einem Prompt macht. Rechts, was das System aus deinem eigenen Material&nbsp;schreibt.",
  bad=("Generische KI", "In der heutigen schnelllebigen Welt ist Kundenerlebnis wichtiger denn je. Hier sind 5 Tipps, wie du deinen Service aufs nächste Level bringst 🚀", ["Keine Quelle", "Sagt nichts", "Klingt wie alle"]),
  good=("Dein System", "Drei Kunden haben uns letzten Monat dieselbe Frage gestellt: Wie lange dauert die Lieferung wirklich? Hier die ehrliche Antwort, und was wir deshalb geändert&nbsp;haben.", ["Aus euren Vertriebsgesprächen", "Euer Ton", "Von einem Menschen geprüft"]),
  pts=[("Dein Material", "Jeder Text beginnt mit dem, was ihr schon habt, nicht mit dem, was ein Chatbot zufällig weiß."),
       ("Deine Sprache", "Das System lernt eure Begriffe und No-Gos. Niemand muss sie neu erklären."),
       ("Eine feste Person", "Jemand liest jeden Text, bevor du ihn siehst, und korrigiert, was nicht passt."),
       ("Es lernt dazu", "Was du einmal korrigierst, bleibt korrigiert.")],
  tl_h='So <em>automatisieren</em> wir dein Marketing',
  tl=[("1", "Wir schauen uns euer Setup an", "Kostenlos", ["Website, Tools und Team", "Wo heute die Zeit hingeht", "Was die meisten Anfragen bringt"]),
      ("2", "Wir wählen gemeinsam aus", "Festes Angebot", ["Die ersten Automatisierungen", "Was beim Team bleibt", "Klarer Umfang und Preis"]),
      ("3", "Wir bauen es", "Sprint ab 990 €", ["Angebunden an CMS und Daten", "Trainiert auf euer Material", "Getestet, bevor es läuft"]),
      ("4", "Es läuft", "ab 750 € im Monat", ["Eine Person prüft jeden Text", "Du gibst mit einem Klick frei", "Monatsbericht in Anfragen"])],
  tl_note="Pro Domain, 3 Monate Mindestlaufzeit, danach monatlich kündbar. Weitere Automatisierungen lassen sich jederzeit&nbsp;ergänzen.",
  cta_h="Schauen wir uns euer Setup&nbsp;an.", cta_p="30 Minuten. Wir zeigen dir, was allein laufen&nbsp;könnte.",
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

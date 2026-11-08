/* Clickable dashboard demo in the homepage hero (EN + DE).
   Turns the sidebar of #ccal into navigation: each item swaps the main area for an example screen,
   and the guide column on the right explains what that part of GetMarketing does.
   The calendar view itself stays in content-calendar.js. All numbers in the other views are example data. */
(function () {
  var root = document.getElementById('ccal');
  if (!root) return;
  var en = root.getAttribute('data-lang') === 'en';
  function t(e, d) { return en ? e : d; }

  var EX = '<span class="dv-ex">' + t('Example data', 'Beispieldaten') + '</span>';
  function head(title) { return '<div class="dash-h"><b>' + title + '</b>' + EX + '</div>'; }
  function kpis(rows) {
    return '<div class="dv-kpis">' + rows.map(function (r) {
      return '<div><span class="k">' + r[0] + '</span><b>' + r[1] + '</b>' + (r[2] ? '<small class="' + (r[3] || 'up') + '">' + r[2] + '</small>' : '') + '</div>';
    }).join('') + '</div>';
  }
  function ch(type) {
    var names = { blog: t('Blog', 'Blog'), li: 'LinkedIn', ig: 'Instagram', rep: t('Report', 'Report') };
    return '<i class="dv-ch ' + type + '">' + names[type] + '</i>';
  }
  function table(cols, rows) {
    return '<div class="dv-tbl"><table><thead><tr>' + cols.map(function (c) { return '<th>' + c + '</th>'; }).join('') + '</tr></thead><tbody>' +
      rows.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>';
  }

  // Order matches the sidebar items in index.html / de/index.html
  var VIEWS = [
    {
      id: 'home', name: t('Home', 'Start'),
      lead: t('Your starting point. You see what the agents did this week, what is waiting for you and how marketing is doing, without opening five different tools.',
              'Dein Startpunkt. Du siehst, was die Agenten diese Woche erledigt haben, was auf dich wartet und wie das Marketing läuft, ohne fünf Tools zu öffnen.'),
      pts: [t('A live feed of every step the agents take', 'Ein Verlauf jedes Schritts der Agenten'),
            t('Open approvals at a glance', 'Offene Freigaben auf einen Blick'),
            t('Visitors and inquiries from GA4 and Search Console', 'Besucher und Anfragen aus GA4 und Search Console')],
      html: function () {
        var feed = [
          ['SA', t('Strategy Agent', 'Strategie-Agent'), t('planned 4 pieces for week 46', 'hat 4 Beiträge für KW 46 geplant'), t('Mon 08:00', 'Mo 08:00')],
          ['SEO', t('SEO Agent', 'SEO-Agent'), t('compared 38 keywords and picked “cnc fräsen” (22,200 searches/month)', 'hat 38 Keywords verglichen und „cnc fräsen“ gewählt (22.200 Suchen/Monat)'), t('Mon 09:12', 'Mo 09:12')],
          ['CA', t('Content Agent', 'Content-Agent'), t('finished the draft “CNC milling: process and costs”', 'hat den Entwurf „CNC-Fräsen: Verfahren und Kosten“ fertiggestellt'), t('Tue 14:30', 'Di 14:30')],
          ['QC', t('Quality check', 'Qualitätsprüfung'), t('checked facts, brand and SEO: score green, sent to you for approval', 'hat Fakten, Marke und SEO geprüft: Score grün, zur Freigabe an dich'), t('Wed 10:05', 'Mi 10:05')],
          ['WP', t('Publishing', 'Veröffentlichung'), t('put the approved guide live in WordPress', 'hat den freigegebenen Ratgeber in WordPress live gestellt'), t('Thu 08:30', 'Do 08:30')],
          ['RP', t('Reporting', 'Reporting'), t('sent the weekly report', 'hat den Wochenreport verschickt'), t('Fri 16:00', 'Fr 16:00')]
        ];
        return head(t('This week at a glance', 'Diese Woche auf einen Blick')) +
          kpis([[t('Published', 'Veröffentlicht'), '4', t('on plan', 'nach Plan'), 'flat'], [t('Waiting for you', 'Wartet auf dich'), '<span data-dv-count>3</span>', t('approvals', 'Freigaben'), 'flat'],
                [t('Organic visitors', 'Organische Besucher'), en ? '4,820' : '4.820', '+18 %'], [t('Inquiries', 'Anfragen'), '31', '+6']]) +
          '<h5 class="dv-sub">' + t('Agent activity', 'Aktivität der Agenten') + '</h5><ul class="dv-feed">' +
          feed.map(function (f) { return '<li><i>' + f[0] + '</i><div><b>' + f[1] + '</b> ' + f[2] + '</div><small>' + f[3] + '</small></li>'; }).join('') + '</ul>';
      }
    },
    {
      id: 'calendar', name: t('Calendar', 'Kalender'),
      lead: t('Every piece planned for the month: articles, LinkedIn posts and the weekly report. Each topic is tied to a real keyword and its monthly searches.',
              'Jeder geplante Beitrag des Monats: Artikel, LinkedIn-Posts und der Wochenreport. Jedes Thema hängt an einem echten Keyword und seinem Suchvolumen.'),
      pts: [t('Switch industries above the calendar to see other example plans', 'Wechsle oben die Branche für weitere Beispielpläne'),
            t('Enter your own deal value to see the revenue estimate', 'Trag deinen Auftragswert ein für die Umsatzschätzung'),
            t('Search volumes are real values for Germany', 'Suchvolumen sind echte Werte für Deutschland')]
    },
    {
      id: 'plan', name: t('4-Week Plan', '4-Wochen-Plan'),
      lead: t('The Strategy Agent turns your goals into a plan for the next four weeks: one theme per week, each piece with a clear job. It re-plans every week based on what worked.',
              'Der Strategie-Agent macht aus deinen Zielen einen Plan für vier Wochen: ein Thema pro Woche, jeder Beitrag mit klarer Aufgabe. Jede Woche wird anhand der Ergebnisse neu geplant.'),
      pts: [t('Built from your brand, offer and market', 'Aufgebaut aus Marke, Angebot und Markt'),
            t('Articles bring search traffic, posts build trust', 'Artikel bringen Suchtraffic, Posts schaffen Vertrauen'),
            t('You set the goals, the plan follows', 'Du setzt die Ziele, der Plan folgt')],
      html: function () {
        var W = [
          [t('Week 46 · Nov 2–6', 'KW 46 · 2.–6.11.'), t('Core capabilities', 'Kernkompetenzen'), t('Rank for “cnc fräsen”', 'Ranking für „cnc fräsen“'),
            [['li', t('How we find skilled workers', 'Wie wir Fachkräfte finden')], ['blog', t('CNC milling: process and costs', 'CNC-Fräsen: Verfahren und Kosten')], ['li', t('Training machinists in-house', 'Ausbildung zum Zerspanungsmechaniker')], ['blog', t('ISO 9001 in a machine shop', 'ISO 9001 im Fertigungsbetrieb')]]],
          [t('Week 47 · Nov 9–13', 'KW 47 · 9.–13.11.'), t('Quality', 'Qualität'), t('Trust with buyers', 'Vertrauen bei Einkäufern'),
            [['li', t('What lean management changed for us', 'Was Lean Management verändert hat')], ['blog', t('Powder coating: process and durability', 'Pulverbeschichtung: Ablauf und Haltbarkeit')], ['li', t('Measuring quality, not just checking it', 'Qualität messen statt nur prüfen')], ['blog', t('Laser cutting: materials and limits', 'Laserschneiden: Materialien und Grenzen')]]],
          [t('Week 48 · Nov 16–20', 'KW 48 · 16.–20.11.'), t('Modern production', 'Moderne Fertigung'), t('Reach technical leads', 'Technische Leiter erreichen'),
            [['li', t('Industry 4.0 for mid-sized firms', 'Industrie 4.0 im Mittelstand')], ['blog', t('Sheet metal work from one supplier', 'Blechbearbeitung aus einer Hand')], ['li', t('Planning maintenance before things break', 'Wartung planen, bevor etwas ausfällt')], ['blog', t('Rapid prototyping for small batches', 'Rapid Prototyping für Kleinserien')]]],
          [t('Week 49 · Nov 23–27', 'KW 49 · 23.–27.11.'), t('Buying decisions', 'Kaufentscheidung'), t('Turn readers into inquiries', 'Leser zu Anfragen machen'),
            [['li', t('Keeping supply chains short', 'Lieferketten kurz halten')], ['blog', t('Contract manufacturing: what buyers check', 'Lohnfertigung: worauf Einkäufer achten')], ['li', t('Assembling complete modules', 'Montage ganzer Baugruppen')], ['blog', t('CNC turning vs. milling', 'CNC-Drehen oder Fräsen im Vergleich')]]]
        ];
        return head(t('4-week plan · November 2026', '4-Wochen-Plan · November 2026')) + '<div class="dv-weeks">' + W.map(function (w, i) {
          return '<div class="dv-wk' + (i === 0 ? ' now' : '') + '"><span class="k">' + w[0] + '</span><b>' + w[1] + '</b><p class="dv-goal">' + t('Goal: ', 'Ziel: ') + w[2] + '</p><ul>' +
            w[3].map(function (p) { return '<li>' + ch(p[0]) + p[1] + '</li>'; }).join('') + '</ul></div>';
        }).join('') + '</div>';
      }
    },
    {
      id: 'review', name: t('Content Review', 'Content-Prüfung'),
      lead: t('You write nothing yourself, you only approve. Every draft first passes automatic checks for facts, brand and SEO. Then you read it and approve it with one click. Pages go live in your CMS, LinkedIn posts you copy and post yourself.',
              'Du schreibst nichts selbst, du gibst nur frei. Jeder Entwurf läuft zuerst durch automatische Prüfungen für Fakten, Marke und SEO. Dann liest du ihn und gibst ihn mit einem Klick frei. Seiten gehen in deinem CMS live, LinkedIn-Posts kopierst und postest du selbst.'),
      pts: [t('Try it: approve the drafts on the left', 'Probier es aus: Gib die Entwürfe frei'),
            t('Ask for changes in plain words, the system revises and learns from it', 'Änderungen in normalen Worten, das System überarbeitet und lernt daraus'),
            t('Nothing is posted on LinkedIn automatically', 'Auf LinkedIn wird nichts automatisch gepostet')],
      html: function () {
        var R = [
          ['blog', t('CNC milling: process and costs', 'CNC-Fräsen: Verfahren und Kosten'), t('What drives the price of a milled part, how long a batch takes and when turning is the better choice. With a cost table for typical materials.', 'Was den Preis eines Frästeils bestimmt, wie lange eine Serie dauert und wann Drehen die bessere Wahl ist. Mit Kostentabelle für typische Werkstoffe.'), t('Tue 09:00', 'Di 09:00')],
          ['li', t('How we find skilled workers', 'Wie wir Fachkräfte finden'), t('Three years ago we had four open positions and no applicants. Today we train six apprentices. Here is what changed …', 'Vor drei Jahren hatten wir vier offene Stellen und keine Bewerber. Heute bilden wir sechs Azubis aus. Das hat sich geändert …'), t('Mon 08:30', 'Mo 08:30')],
          ['li', t('Training machinists in-house', 'Ausbildung zum Zerspanungsmechaniker'), t('Our apprentices run their first CNC job in week three. A look at how we structure the training …', 'Unsere Azubis fahren ihren ersten CNC-Auftrag in Woche drei. So ist unsere Ausbildung aufgebaut …'), t('Wed 08:30', 'Mi 08:30')]
        ];
        return head(t('Content review · 3 waiting', 'Content-Prüfung · 3 offen').replace('3', '<span data-dv-count>3</span>')) + '<div class="dv-rvs">' + R.map(function (r) {
          return '<div class="dv-rv"><div class="dv-rv-h">' + ch(r[0]) + '<span class="dv-ok">✓ ' + t('Quality check passed', 'Qualitätsprüfung bestanden') + '</span></div><b>' + r[1] + '</b><p>' + r[2] + '</p>' +
            '<div class="dv-rv-a"><button type="button" class="dv-approve" data-when="' + r[3] + '">' + t('Approve', 'Freigeben') + '</button><button type="button" class="dv-change">' + t('Request changes', 'Änderung anfragen') + '</button></div>' +
            '<p class="dv-rv-note" hidden>' + t('In the app you write what to change, for example “shorter intro”. The system revises the draft and remembers it for next time.', 'In der App schreibst du, was sich ändern soll, zum Beispiel „kürzere Einleitung“. Das System überarbeitet den Entwurf und merkt es sich für das nächste Mal.') + '</p></div>';
        }).join('') + '</div><p class="dv-empty" hidden>' + t('All caught up. The next drafts arrive on Monday.', 'Alles erledigt. Die nächsten Entwürfe kommen am Montag.') + '</p>';
      }
    },
    {
      id: 'analytics', name: 'Analytics',
      lead: t('GA4 and Search Console in one view. For every piece you see whether it went live, how many people it reached and which inquiries it brought.',
              'GA4 und Search Console in einer Ansicht. Für jeden Beitrag siehst du, ob er live ist, wie viele Menschen er erreicht hat und welche Anfragen er gebracht hat.'),
      pts: [t('Results per piece, not just per website', 'Ergebnisse pro Beitrag, nicht nur pro Website'),
            t('A short weekly report every Friday', 'Jeden Freitag ein kurzer Wochenreport'),
            t('The numbers feed next week’s plan', 'Die Zahlen fließen in den Plan der nächsten Woche')],
      html: function () {
        var pts = [1900, 2050, 2010, 2300, 2480, 2420, 2900, 3150, 3400, 3720, 4310, 4820], max = 5200, n = pts.length;
        var line = pts.map(function (v, i) { return (i * 600 / (n - 1)).toFixed(1) + ',' + (150 - v / max * 140).toFixed(1); }).join(' ');
        var nf = function (s) { return en ? s : s.replace(',', '.'); };
        return head(t('Analytics · last 12 weeks', 'Analytics · letzte 12 Wochen')) +
          kpis([[t('Organic visitors', 'Organische Besucher'), nf('4,820'), '+18 %'], [t('Inquiries', 'Anfragen'), '31', '+6'], [t('Avg. position', 'Ø Position'), en ? '14.2' : '14,2', t('up 3.1', '3,1 besser')], [t('Pages ranking', 'Seiten im Ranking'), '27', '+5']]) +
          '<div class="dv-chart"><svg viewBox="0 0 600 150" preserveAspectRatio="none" aria-hidden="true"><polygon points="0,150 ' + line + ' 600,150" /><polyline points="' + line + '" /></svg><div class="dv-axis"><span>' + t('Aug', 'Aug.') + '</span><span>' + t('Sep', 'Sep.') + '</span><span>' + t('Oct', 'Okt.') + '</span><span>' + t('Nov', 'Nov.') + '</span></div></div>' +
          table([t('Top pieces', 'Top-Beiträge'), t('Visitors', 'Besucher'), t('Inquiries', 'Anfragen')], [
            [t('CNC milling: process and costs', 'CNC-Fräsen: Verfahren und Kosten'), nf('1,240'), '9'],
            [t('Contract manufacturing: what buyers check', 'Lohnfertigung: worauf Einkäufer achten'), '610', '7'],
            [t('ISO 9001 in a machine shop', 'ISO 9001 im Fertigungsbetrieb'), '880', '3']]);
      }
    },
    {
      id: 'funnel', name: 'Funnel',
      lead: t('From first visit to signed customer, step by step. You see where people drop off, and the agents focus on the weakest step instead of just producing more content.',
              'Vom ersten Besuch bis zum Kunden, Schritt für Schritt. Du siehst, wo Menschen abspringen, und die Agenten setzen am schwächsten Schritt an, statt nur mehr Content zu produzieren.'),
      pts: [t('Each step with its conversion rate', 'Jeder Schritt mit Conversion-Rate'),
            t('Leads matched to the piece they came from', 'Leads dem Beitrag zugeordnet, über den sie kamen'),
            t('Clear next action for the biggest drop', 'Klare nächste Maßnahme für den größten Abbruch')],
      html: function () {
        var S = [[t('Visitors', 'Besucher'), en ? '4,820' : '4.820', 100], [t('Engaged (2+ pages)', 'Interessiert (2+ Seiten)'), en ? '1,930' : '1.930', 40], [t('Inquiries', 'Anfragen'), '31', 14], [t('Qualified', 'Qualifiziert'), '14', 8], [t('Customers', 'Kunden'), '3', 4]];
        var rates = ['40 %', en ? '1.6 %' : '1,6 %', '45 %', '21 %'];
        return head(t('Funnel · October', 'Funnel · Oktober')) + '<div class="dv-fun">' + S.map(function (s, i) {
          return (i ? '<div class="dv-rate' + (i === 2 ? ' weak' : '') + '">↓ ' + rates[i - 1] + '</div>' : '') + '<div class="dv-step"><span>' + s[0] + '</span><div class="dv-bar"><i style="width:' + s[2] + '%"></i></div><b>' + s[1] + '</b></div>';
        }).join('') + '</div><div class="dv-tip"><b>' + t('Biggest drop: engaged → inquiry', 'Größter Abbruch: interessiert → Anfrage') + '</b>' +
          t('Next plan: a guide on CNC costs with a price range, linked from the CNC pages.', 'Nächster Plan: ein Ratgeber zu CNC-Kosten mit Preisspanne, verlinkt von den CNC-Seiten.') + '</div>';
      }
    },
    {
      id: 'seo', name: t('SEO Insights', 'SEO-Insights'),
      lead: t('Where you rank on Google and where the quick wins are. The SEO Agent spots pages close to page one and topics your buyers search for that you have not covered yet.',
              'Wo du bei Google rankst und wo schnelle Gewinne liegen. Der SEO-Agent findet Seiten kurz vor Seite eins und Themen, nach denen deine Kunden suchen, die du noch nicht abdeckst.'),
      pts: [t('Rankings from Search Console', 'Rankings aus der Search Console'),
            t('Real search volumes per keyword', 'Echte Suchvolumen pro Keyword'),
            t('Updates old articles before writing new ones', 'Aktualisiert alte Artikel, bevor neue entstehen')],
      html: function () {
        var up = function (n) { return '<span class="dv-up">▲ ' + n + '</span>'; };
        return head(t('SEO insights · keywords', 'SEO-Insights · Keywords')) +
          table(['Keyword', t('Searches/mo', 'Suchen/Monat'), 'Position', t('Change', 'Veränderung')], [
            ['cnc fräsen', en ? '22,200' : '22.200', '8', up(5)], ['lohnfertigung', '880', '3', up(2)], ['laserschneiden', en ? '3,600' : '3.600', '14', up(9)],
            ['blechbearbeitung', en ? '1,600' : '1.600', '6', '<span class="dv-down">▼ 1</span>'], ['pulverbeschichtung', en ? '12,100' : '12.100', '21', '<span class="dv-new">' + t('new', 'neu') + '</span>']]) +
          '<div class="dv-tip"><b>' + t('Quick win', 'Schneller Gewinn') + '</b>' + t('“cnc drehen” (720 searches/month) sits at position 11. Updating the existing article could move it to page one.', '„cnc drehen“ (720 Suchen/Monat) steht auf Position 11. Eine Aktualisierung des bestehenden Artikels könnte es auf Seite eins bringen.') + '</div>';
      }
    },
    {
      id: 'research', name: t('Research', 'Recherche'),
      lead: t('The Research Agent watches your market: what competitors publish, what buyers ask and which topics are growing. The findings go straight into the next plan.',
              'Der Recherche-Agent beobachtet deinen Markt: was Wettbewerber veröffentlichen, was Kunden fragen und welche Themen wachsen. Die Erkenntnisse fließen direkt in den nächsten Plan.'),
      pts: [t('Competitor content and positioning', 'Inhalte und Positionierung der Wettbewerber'),
            t('Real questions from search data', 'Echte Fragen aus Suchdaten'),
            t('Trends before they get crowded', 'Trends, bevor sie überlaufen sind')],
      html: function () {
        var C = [
          [t('Competitors', 'Wettbewerber'), t('2 competitors published about ISO 9001 this month. Neither covers costs or timelines, which is the gap your article fills.', '2 Wettbewerber haben diesen Monat über ISO 9001 geschrieben. Keiner nennt Kosten oder Dauer, genau diese Lücke füllt dein Artikel.')],
          [t('Buyer questions', 'Fragen von Käufern'), t('“How long does powder coating last?” is one of the most searched questions in your field. Added as a section to week 47.', '„Wie lange hält Pulverbeschichtung?“ gehört zu den meistgesuchten Fragen deiner Branche. Als Abschnitt in KW 47 eingeplant.')],
          [t('Growing topic', 'Wachsendes Thema'), t('Searches for predictive maintenance keep rising. Planned as a LinkedIn post in week 48.', 'Suchen nach Predictive Maintenance steigen weiter. Als LinkedIn-Post in KW 48 eingeplant.')]
        ];
        return head(t('Research · this week', 'Recherche · diese Woche')) + '<div class="dv-cards">' + C.map(function (c) { return '<div class="dv-card"><span class="k">' + c[0] + '</span><p>' + c[1] + '</p></div>'; }).join('') + '</div>';
      }
    },
    {
      id: 'changes', name: t('Website changes', 'Website-Änderungen'),
      lead: t('What GetMarketing changes on your website, and how. New pages, titles, meta descriptions, headings, alt texts and redirects go in through your CMS, never through your theme code. Every change shows before and after and can be undone with one click.',
              'Was GetMarketing an deiner Website ändert, und wie. Neue Seiten, Titles, Meta-Beschreibungen, Überschriften, Alt-Texte und Weiterleitungen laufen über dein CMS, nie über den Code deines Themes. Jede Änderung zeigt vorher und nachher und lässt sich mit einem Klick zurücknehmen.'),
      pts: [t('WordPress and Shopify at launch, other systems via HTML or Markdown export', 'WordPress und Shopify zum Start, andere Systeme per HTML- oder Markdown-Export'),
            t('Theme code, page speed, robots.txt: a ready brief for your developer', 'Theme-Code, Ladezeit, robots.txt: eine fertige Anleitung für deinen Entwickler'),
            t('Nothing changes without your approval', 'Nichts ändert sich ohne deine Freigabe')],
      html: function () {
        var undo = '<button type="button" class="dv-undo">' + t('Undo', 'Zurücknehmen') + '</button>';
        var ba = function (b, a) { return '<span class="dv-before">' + b + '</span> → <b>' + a + '</b>'; };
        return head(t('Website changes · WordPress', 'Website-Änderungen · WordPress')) +
          table([t('Page', 'Seite'), t('Change', 'Änderung'), t('Before → after', 'Vorher → nachher'), 'Status'], [
            ['/cnc-fraesen', 'Title', ba('CNC Fräsen – Müller', t('CNC milling from one piece | Müller Metal Works', 'CNC-Fräsen ab Stückzahl 1 | Müller Metallbau')), '<span class="dv-up">Live</span> ' + undo],
            ['/lohnfertigung', t('Meta description', 'Meta-Beschreibung'), ba(t('empty', 'leer'), t('Contract manufacturing in 5 days …', 'Lohnfertigung in 5 Tagen …')), '<span class="dv-up">Live</span> ' + undo],
            ['/laser-alt', t('301 redirect', '301-Weiterleitung'), ba('404', '/laserschneiden'), '<span class="dv-up">Live</span> ' + undo],
            [t('/guide/powder-coating', '/ratgeber/pulverbeschichtung'), t('New page', 'Neue Seite'), ba('–', t('Powder coating: process and durability', 'Pulverbeschichtung: Ablauf und Haltbarkeit')), '<span class="dv-new">' + t('Waiting for you', 'Wartet auf dich') + '</span>']]) +
          '<div class="dv-tip"><b>' + t('For your developer', 'Für deinen Entwickler') + '</b>' + t('Page speed: 3 images are larger than 1 MB. GetMarketing does not touch your theme code, so this arrives as a short brief. With Enterprise we fix it for you.', 'Ladezeit: 3 Bilder sind größer als 1 MB. GetMarketing fasst den Code deines Themes nicht an, deshalb kommt das als kurze Anleitung. Bei Enterprise beheben wir es für dich.') + '</div>';
      }
    }
  ];

  var side = root.querySelector('.dash-side'), main = root.querySelector('.dash-main');
  var items = Array.prototype.slice.call(side.querySelectorAll('li'));
  if (items.length !== VIEWS.length) return;
  var badge = items[3].querySelector('em');

  // Wrap the existing calendar content as its own view, add one container per other view
  var panes = {}, cal = document.createElement('div');
  cal.className = 'dv';
  while (main.firstChild) cal.appendChild(main.firstChild);
  main.appendChild(cal);
  panes.calendar = cal;

  var guide = document.createElement('aside');
  guide.className = 'dash-guide';
  guide.setAttribute('aria-live', 'polite');
  root.appendChild(guide);
  side.setAttribute('aria-label', t('Dashboard sections', 'Bereiche im Dashboard'));

  var cur = 1, touched = false, pending = 3;
  function setCount() {
    Array.prototype.forEach.call(root.querySelectorAll('[data-dv-count]'), function (c) { c.textContent = pending; });
    if (badge) { badge.textContent = pending; badge.hidden = !pending; }
  }
  function renderGuide(i) {
    var v = VIEWS[i], next = VIEWS[(i + 1) % VIEWS.length];
    guide.innerHTML = '<p class="dg-tag"><span></span>' + t('Interactive demo', 'Interaktive Demo') + '</p>' +
      '<h4>' + v.name + '</h4><p class="dg-lead">' + v.lead + '</p><ul class="dg-pts">' + v.pts.map(function (p) { return '<li>' + p + '</li>'; }).join('') + '</ul>' +
      (touched ? '' : '<p class="dg-hint"><span class="dg-wide">← ' + t('Click any section in the menu to explore it.', 'Klick auf einen Bereich im Menü, um ihn zu erkunden.') + '</span><span class="dg-narrow">↑ ' + t('Tap a section above to explore it.', 'Tipp oben auf einen Bereich, um ihn zu erkunden.') + '</span></p>') +
      '<div class="dg-foot"><small>' + (i + 1) + ' / ' + VIEWS.length + '</small><button type="button" class="dg-next">' + t('Next', 'Weiter') + ': ' + next.name + ' →</button></div>';
  }
  function show(i, fromUser) {
    var v = VIEWS[i];
    // Keep the box from jumping when leaving the calendar (desktop only, the mobile calendar is a long list)
    if (cur === 1 && i !== 1 && cal.offsetHeight && window.innerWidth > 900) main.style.minHeight = main.offsetHeight + 'px';
    if (!panes[v.id]) {
      var p = document.createElement('div');
      p.className = 'dv';
      p.innerHTML = v.html();
      main.appendChild(p);
      panes[v.id] = p;
    }
    Object.keys(panes).forEach(function (k) { panes[k].hidden = k !== v.id; });
    panes[v.id].classList.remove('dv-in'); void panes[v.id].offsetWidth; panes[v.id].classList.add('dv-in');
    items.forEach(function (li, j) { li.classList.toggle('on', j === i); if (j === i) li.setAttribute('aria-current', 'page'); else li.removeAttribute('aria-current'); });
    cur = i;
    if (fromUser) touched = true;
    setCount();
    renderGuide(i);
    if (fromUser && window.innerWidth <= 900) items[i].scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
    if (fromUser) {
      try {
        if (window.amplitude && typeof window.amplitude.track === 'function') window.amplitude.track('Demo Section Viewed', { section: v.id, lang: en ? 'en' : 'de' });
        if (typeof window.gtag === 'function') window.gtag('event', 'demo_section_view', { section: v.id });
      } catch (e) {}
    }
  }

  items.forEach(function (li, i) {
    li.setAttribute('role', 'button');
    li.tabIndex = 0;
    li.addEventListener('click', function () { show(i, true); });
    li.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(i, true); } });
  });
  window.addEventListener('resize', function () { main.style.minHeight = ''; });
  guide.addEventListener('click', function (e) { if (e.target.closest('.dg-next')) show((cur + 1) % VIEWS.length, true); });
  main.addEventListener('click', function (e) {
    var a = e.target.closest('.dv-approve'), c = e.target.closest('.dv-change'), u = e.target.closest('.dv-undo');
    if (u) {
      u.parentNode.innerHTML = '<span class="dv-down">' + t('Undone', 'Zurückgenommen') + '</span>';
    } else if (a) {
      var card = a.closest('.dv-rv');
      card.classList.add('done');
      var when = a.getAttribute('data-when');
      card.querySelector('.dv-rv-a').innerHTML = '<span class="dv-done">✓ ' + (when ? t('Approved · goes live ', 'Freigegeben · geht live ') + when : t('Approved · ready to copy and post', 'Freigegeben · bereit zum Kopieren und Posten')) + '</span>';
      card.querySelector('.dv-rv-note').hidden = true;
      pending = Math.max(0, pending - 1);
      setCount();
      if (!pending) root.querySelector('.dv-empty').hidden = false;
    } else if (c) {
      var note = c.closest('.dv-rv').querySelector('.dv-rv-note');
      note.hidden = !note.hidden;
    }
  });

  show(1, false);
})();

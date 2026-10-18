/* Content calendar demo under the homepage hero.
   Keywords and monthly search volumes are real: Google Ads via DataForSEO, Germany, fetched 18 Oct 2026.
   Titles are example topics. The estimate strip uses stated assumptions (CTR, inquiry rate, close rate, editable deal value).
   Language comes from data-lang="de|en" on #ccal. */
(function () {
  var root = document.getElementById('ccal');
  if (!root) return;
  var lang = root.getAttribute('data-lang') === 'en' ? 'en' : 'de';
  var T = {
    de: { days: ['Mo', 'Di', 'Mi', 'Do', 'Fr'], date: function (d) { return d + '.11.'; }, week: 'Wochenreport', weekSub: 'GA4 und Search Console', month: 'Monatsreport und Dezemberplan' },
    en: { days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], date: function (d) { return 'Nov ' + d; }, week: 'Weekly report', weekSub: 'GA4 and Search Console', month: 'Monthly report and December plan' }
  }[lang];

  // [type, title DE, title EN, keyword, volume]; reports are added per week on Fridays
  var PLANS = {
    industrie: [
      ['li', 'Wie wir Fachkräfte finden', 'How we find skilled workers', 'fachkräftemangel', 22200],
      ['blog', 'CNC-Fräsen: Verfahren und Kosten', 'CNC milling: process and costs', 'cnc fräsen', 22200],
      ['li', 'Ausbildung zum Zerspanungsmechaniker', 'Training machinists in-house', 'zerspanungsmechaniker', 22200],
      ['blog', 'ISO 9001 im Fertigungsbetrieb', 'ISO 9001 in a machine shop', 'iso 9001', 18100],
      ['li', 'Was Lean Management verändert hat', 'What lean management changed for us', 'lean management', 12100],
      ['blog', 'Pulverbeschichtung: Ablauf und Haltbarkeit', 'Powder coating: process and durability', 'pulverbeschichtung', 12100],
      ['li', 'Qualität messen statt nur prüfen', 'Measuring quality, not just checking it', 'qualitätsmanagement', 12100],
      ['blog', 'Laserschneiden: Materialien und Grenzen', 'Laser cutting: materials and limits', 'laserschneiden', 3600],
      ['li', 'Industrie 4.0 im Mittelstand', 'Industry 4.0 for mid-sized firms', 'industrie 4.0', 5400],
      ['blog', 'Blechbearbeitung aus einer Hand', 'Sheet metal work from one supplier', 'blechbearbeitung', 1600],
      ['li', 'Wartung planen, bevor etwas ausfällt', 'Planning maintenance before things break', 'predictive maintenance', 2900],
      ['blog', 'Rapid Prototyping für Kleinserien', 'Rapid prototyping for small batches', 'rapid prototyping', 1300],
      ['li', 'Lieferketten kurz halten', 'Keeping supply chains short', 'lieferkette', 1600],
      ['blog', 'Lohnfertigung: worauf Einkäufer achten', 'Contract manufacturing: what buyers check', 'lohnfertigung', 880],
      ['li', 'Montage ganzer Baugruppen', 'Assembling complete modules', 'baugruppenmontage', 390],
      ['blog', 'CNC-Drehen oder Fräsen im Vergleich', 'CNC turning vs. milling', 'cnc drehen', 720]
    ],
    kanzlei: [
      ['li', 'Gewerbesteuer kurz erklärt', 'Trade tax in a nutshell', 'gewerbesteuer', 9900],
      ['blog', 'Kleinunternehmerregelung: Grenzen und Folgen', 'Small business rule: limits and effects', 'kleinunternehmerregelung', 14800],
      ['li', 'Erbschaftsteuer bei der Firmenübergabe', 'Inheritance tax when handing over a firm', 'erbschaftssteuer', 60500],
      ['blog', 'E-Rechnung: Pflichten für Unternehmen', 'E-invoicing: what companies must do', 'e-rechnung pflicht', 9900],
      ['li', 'Nachfolge früh planen', 'Plan your succession early', 'unternehmensnachfolge', 2400],
      ['blog', 'Umsatzsteuervoranmeldung Schritt für Schritt', 'VAT pre-return step by step', 'umsatzsteuervoranmeldung', 8100],
      ['li', 'Lohnbuchhaltung auslagern', 'Outsourcing payroll', 'lohnbuchhaltung', 2400],
      ['blog', 'Reisekostenabrechnung richtig machen', 'Getting travel expenses right', 'reisekostenabrechnung', 6600],
      ['li', 'Gut vorbereitet in die Betriebsprüfung', 'Preparing for a tax audit', 'betriebsprüfung', 1900],
      ['blog', 'Jahresabschluss: Ablauf und Fristen', 'Annual accounts: process and deadlines', 'jahresabschluss', 5400],
      ['li', 'Steuererklärung als Selbstständiger', 'Tax returns for the self-employed', 'steuererklärung selbstständige', 1000],
      ['blog', 'Was ein Steuerberater kostet', 'What a tax advisor costs', 'steuerberater kosten', 5400],
      ['li', 'Laptop abschreiben: so geht es', 'Depreciating a laptop', 'abschreibung laptop', 590],
      ['blog', 'GmbH gründen: Kosten und Ablauf', 'Founding a GmbH: costs and steps', 'gmbh gründen', 3600],
      ['li', 'Belege digital statt im Ordner', 'Receipts in the cloud, not in folders', 'digitale buchhaltung', 320],
      ['blog', 'Holding gründen: wann es sich lohnt', 'When a holding company pays off', 'holding gründen', 1600]
    ],
    shop: [
      ['li', 'Ein Tag in unserer Rösterei', 'A day in our roastery', 'kaffeerösterei', 27100],
      ['blog', 'Kaffeebohnen kaufen: so erkennst du Qualität', 'Buying coffee beans: how to spot quality', 'kaffeebohnen', 33100],
      ['li', 'Latte Art für Anfänger', 'Latte art for beginners', 'latte art', 6600],
      ['blog', 'Kaffeemühle: Kegel oder Scheibe?', 'Coffee grinders: conical or flat burr?', 'kaffeemühle', 33100],
      ['li', 'Was Fair Trade beim Kaffee bedeutet', 'What fair trade means for coffee', 'fair trade kaffee', 390],
      ['blog', 'French Press: Anleitung und Mahlgrad', 'French press: guide and grind size', 'french press', 33100],
      ['li', 'Espresso richtig zubereiten', 'Brewing espresso properly', 'espresso zubereiten', 720],
      ['blog', 'Cold Brew selber machen', 'Making cold brew at home', 'cold brew', 12100],
      ['li', 'Filterkaffee ist zurück', 'Filter coffee is back', 'filterkaffee', 6600],
      ['blog', 'Die richtigen Espressobohnen finden', 'Finding the right espresso beans', 'espresso bohnen', 2900],
      ['li', 'Kaffee richtig lagern', 'Storing coffee properly', 'kaffee lagern', 140],
      ['blog', 'Kaffeevollautomat entkalken', 'Descaling a bean-to-cup machine', 'kaffeevollautomat entkalken', 3600],
      ['li', 'Unsere Lieferkette erklärt', 'Our supply chain explained', 'nachhaltiger kaffee', 90],
      ['blog', 'Milchschaum wie im Café', 'Café-style milk foam', 'milchschaum', 1600],
      ['li', 'So funktioniert unser Kaffee-Abo', 'How our coffee subscription works', 'kaffee abo', 590],
      ['blog', 'Siebträgermaschine kaufen: Ratgeber', 'Buying an espresso machine: a guide', 'siebträgermaschine', 110000]
    ],
    saas: [
      ['li', 'Hybrides Arbeiten, das funktioniert', 'Hybrid work that actually works', 'hybrides arbeiten', 3600],
      ['blog', 'Gantt-Diagramm erstellen mit Vorlage', 'Building a Gantt chart, with template', 'gantt diagramm', 22200],
      ['li', 'Was New Work im Alltag heißt', 'What new work means day to day', 'new work', 4400],
      ['blog', 'Kanban Board: Spalten, Regeln, Beispiele', 'Kanban boards: columns, rules, examples', 'kanban board', 18100],
      ['li', 'Change Management in kleinen Teams', 'Change management in small teams', 'change management', 8100],
      ['blog', 'Scrum einfach erklärt', 'Scrum explained simply', 'scrum', 22200],
      ['li', 'Remote Work ohne Meeting-Chaos', 'Remote work without meeting chaos', 'remote work', 2900],
      ['blog', 'OKR einführen: Schritt für Schritt', 'Introducing OKRs step by step', 'okr', 9900],
      ['li', 'Agile Methoden im Vergleich', 'Agile methods compared', 'agile methoden', 1000],
      ['blog', 'Zeiterfassung im Team einführen', 'Rolling out time tracking in a team', 'zeiterfassung', 8100],
      ['li', 'Teams auf Distanz führen', 'Leading teams remotely', 'teamführung', 260],
      ['blog', 'Ressourcenplanung für Projekte', 'Resource planning for projects', 'ressourcenplanung', 1000],
      ['li', 'Produktiver ohne Überstunden', 'More productive without overtime', 'produktivität steigern', 210],
      ['blog', 'Projektplan-Vorlage zum Download', 'Project plan template to download', 'projektplan vorlage', 1000],
      ['li', 'Eine bessere Meeting-Kultur', 'A better meeting culture', 'meeting kultur', 40],
      ['blog', 'Projektmanagement-Software vergleichen', 'Comparing project management software', 'projektmanagement software', 1300]
    ]
  };

  var grid = root.querySelector('.ccal-grid');
  var est = { sum: root.querySelector('[data-est-sum]'), clicks: root.querySelector('[data-est-clicks]'), leads: root.querySelector('[data-est-leads]'), rev: root.querySelector('[data-est-rev]'), aov: root.querySelector('[data-est-aov]') };
  var CTR = 0.03, LEAD = 0.015, CLOSE = 0.2, shown = 0;
  var tabs = Array.prototype.slice.call(root.querySelectorAll('.ccal-tabs button'));
  var fmt = function (n) { return n.toLocaleString(lang === 'en' ? 'en-US' : 'de-DE'); };
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cur = 0, evs = [], plan = [], timer = null, visible = false, userPicked = false;

  function build(key) {
    var src = PLANS[key], items = [], k = 0;
    for (var w = 0; w < 4; w++) {
      for (var d = 0; d < 4; d++) items.push(src[k++]);
      items.push(['rep', w < 3 ? T.week : T.month, w < 3 ? T.week : T.month, T.weekSub, 0]);
    }
    plan = items;
    grid.innerHTML = '';
    var first = [2, 9, 16, 23];
    evs = items.map(function (p, i) {
      var w = Math.floor(i / 5), d = i % 5;
      var cell = document.createElement('div');
      cell.className = 'ccal-cell';
      cell.innerHTML = '<span class="ccal-dt"><i>' + T.days[d] + ' </i>' + T.date(first[w] + d) + '</span>';
      var ev = document.createElement('div');
      ev.className = 'ccal-ev ' + p[0];
      var title = lang === 'en' ? p[2] : p[1];
      ev.innerHTML = '<div class="ccal-ti">' + title + '</div><div class="ccal-kw"><span>' + p[3] + '</span>' + (p[4] ? '<b>' + fmt(p[4]) + '</b>' : '') + '</div>';
      cell.appendChild(ev);
      grid.appendChild(cell);
      return ev;
    });
  }
  function total() { return plan.reduce(function (a, p) { return a + (p[0] === 'blog' ? p[4] : 0); }, 0); }
  function money(n) { return lang === 'en' ? '€' + fmt(n) : fmt(n) + ' €'; }
  function round(n, step) { return Math.round(n / step) * step; }
  function setSum(n) {
    shown = n;
    var clicks = n * CTR, leads = clicks * LEAD, aov = Math.max(0, parseFloat(est.aov && est.aov.value) || 0);
    est.sum.textContent = fmt(n);
    est.clicks.textContent = '≈ ' + fmt(round(clicks, 10));
    est.leads.textContent = '≈ ' + fmt(Math.round(leads));
    est.rev.textContent = '≈ ' + money(round(leads * CLOSE * aov, 500));
  }
  if (est.aov) est.aov.addEventListener('input', function () { setSum(shown); });
  function showAll() { evs.forEach(function (e) { e.classList.add('on'); }); setSum(total()); }
  function select(i) {
    cur = i;
    tabs.forEach(function (t, j) {
      t.setAttribute('aria-selected', j === i ? 'true' : 'false');
      var bar = t.querySelector('i'); bar.style.transition = 'none'; bar.style.transform = 'scaleX(0)';
    });
    build(tabs[i].getAttribute('data-plan'));
  }
  function stop() { clearInterval(timer); timer = null; }
  function run() {
    stop();
    if (still) { showAll(); return; }
    var i = 0, sum = 0, hold = 18;
    setSum(0);
    timer = setInterval(function () {
      if (i < evs.length) {
        evs[i].classList.add('on');
        if (plan[i][0] === 'blog') { sum += plan[i][4]; setSum(sum); }
        if (i === evs.length - 1 && !userPicked) {
          var bar = tabs[cur].querySelector('i');
          bar.style.transition = 'transform ' + (hold * 0.24) + 's linear'; bar.style.transform = 'scaleX(1)';
        }
      } else if (i >= evs.length + hold && !userPicked) {
        select((cur + 1) % tabs.length); run(); return;
      }
      i++;
    }, 240);
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { userPicked = true; select(i); if (visible) run(); else showAll(); });
  });

  select(0);
  setSum(total());
  if (still || !('IntersectionObserver' in window)) { showAll(); return; }
  new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting && !visible) { visible = true; evs.forEach(function (x) { x.classList.remove('on'); }); run(); }
      else if (!e.isIntersecting && visible) { visible = false; stop(); showAll(); }
    });
  }, { threshold: 0.35 }).observe(root.querySelector('.ccal'));
})();

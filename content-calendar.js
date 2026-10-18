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
    it: [
      ['li', 'Copilot im Arbeitsalltag', 'Copilot in everyday work', 'microsoft copilot', 90500],
      ['blog', 'Cyberangriff: die ersten 24 Stunden', 'Cyberattack: the first 24 hours', 'cyberangriff', 22200],
      ['li', 'Passwortmanager im Team einführen', 'Rolling out a team password manager', 'passwortmanager', 201000],
      ['blog', 'Datenschutz im Mittelstand umsetzen', 'Data protection for mid-sized firms', 'datenschutz', 18100],
      ['li', 'KI im Unternehmen sinnvoll einsetzen', 'Using AI sensibly in your company', 'ki im unternehmen', 260],
      ['blog', 'NIS2: wer betroffen ist', 'NIS2: who is affected', 'nis2', 14800],
      ['li', 'Phishing-Mails erkennen', 'Spotting phishing emails', 'phishing erkennen', 210],
      ['blog', 'IT-Sicherheit für kleine Unternehmen', 'IT security for small businesses', 'it sicherheit', 3600],
      ['li', 'Cloud-Migration ohne Ausfall', 'Cloud migration without downtime', 'cloud migration', 260],
      ['blog', 'Zero Trust einfach erklärt', 'Zero trust explained', 'zero trust', 1900],
      ['li', 'Wie wir IT-Fachkräfte halten', 'How we keep IT talent', 'it fachkräftemangel', 210],
      ['blog', 'Managed Services: was ein MSP übernimmt', 'Managed services: what an MSP covers', 'managed services', 1300],
      ['li', 'Digitalisierung im Mittelstand', 'Digitalisation for mid-sized firms', 'digitalisierung mittelstand', 140],
      ['blog', 'IT-Outsourcing: Kosten und Ablauf', 'IT outsourcing: costs and process', 'it outsourcing', 480],
      ['li', 'Umzug auf Microsoft 365', 'Moving to Microsoft 365', 'microsoft 365 migration', 40],
      ['blog', 'Backup-Strategie nach der 3-2-1-Regel', 'A 3-2-1 backup strategy', 'backup strategie', 320]
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

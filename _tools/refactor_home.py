#!/usr/bin/env python3
"""One-off: move homepage inline CSS/JS into shared files, new lead section, mission to the end."""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

LEAD = {
"en": dict(eyebrow="Free website analysis", h2="Find out what is costing your website <em>enquiries.</em>",
  intro="Send us your website. Within 3 working days you get your visibility analysis with real search data and a concrete proposal for your&nbsp;company.",
  gets=[("Visibility check", "with real Google search data"), ("Your biggest leaks", "ranked by how many enquiries they cost"), ("A concrete proposal", "with the pages that will bring you&nbsp;enquiries")],
  who="<b>Darya Kablash</b>, founder<br>Your request comes straight to&nbsp;me.",
  form_h="Get your free analysis", step="Takes 30 seconds",
  btn="Send me my free analysis", trust=["Free", "No obligation", "Reply within 3 working days"],
  alt='Not ready to talk? <a href="/marketing-plan-generator/">Generate your marketing plan in seconds&nbsp;→</a>'),
"de": dict(eyebrow="Kostenlose Website-Analyse", h2="Finde heraus, was deine Website <em>Anfragen kostet.</em>",
  intro="Schick uns deine Website. Innerhalb von 3 Werktagen bekommst du deine Sichtbarkeits-Analyse mit echten Suchdaten und ein konkretes Angebot für dein&nbsp;Unternehmen.",
  gets=[("Sichtbarkeits-Check", "mit echten Google-Suchdaten"), ("Deine größten Lecks", "sortiert danach, wie viele Anfragen sie kosten"), ("Ein konkretes Angebot", "mit den Seiten, die dir Anfragen&nbsp;bringen")],
  who="<b>Darya Kablash</b>, Gründerin<br>Deine Anfrage landet direkt bei&nbsp;mir.",
  form_h="Hol dir deine kostenlose Analyse", step="Dauert 30 Sekunden",
  btn="Analyse kostenlos anfordern", trust=["Kostenlos", "Unverbindlich", "Antwort in 3 Werktagen"],
  alt='Noch nicht bereit für ein Gespräch? <a href="/marketingplan-erstellen/">Erstelle deinen Marketingplan in Sekunden&nbsp;→</a>'),
}

def lead_section(old, lang):
    L = LEAD[lang]
    form = re.search(r'<form id="lead-form".*?</form>', old, re.S).group(0)
    grid = re.search(r'<div class="lf-grid">.*?</div>', form, re.S).group(0)
    consent = re.search(r'<p class="lf-consent">.*?</p>', form, re.S).group(0)
    status = '<p class="lf-status" role="status" aria-live="polite"></p>'
    open_tag = re.match(r'<form[^>]*>', form).group(0)
    gets = "".join(f'<li><b>{a}</b> {b}</li>' for a, b in L["gets"])
    trust = "".join(f"<li>{t}</li>" for t in L["trust"])
    return f'''<section id="start" class="lead-section">
  <span id="cta"></span>
  <div class="wrap lead-panel">
    <div class="lead-copy reveal">
      <span class="eyebrow">{L["eyebrow"]}</span>
      <h2>{L["h2"]}</h2>
      <p class="intro">{L["intro"]}</p>
      <ul class="lead-gets">{gets}</ul>
      <div class="lead-who"><img src="/darya.jpg" alt="" width="52" height="52" /><p>{L["who"]}</p></div>
    </div>
    <div class="lead-form-card">
      <div class="lf-head"><h3>{L["form_h"]}</h3><span>{L["step"]}</span></div>
      {open_tag}
        {grid}
        <button type="submit" class="lf-submit">{L["btn"]} <span aria-hidden="true">→</span></button>
        <ul class="lf-trust">{trust}</ul>
        {consent}
        {status}
      </form>
    </div>
  </div>
  <p class="lead-alt">{L["alt"]}</p>
</section>'''

SITE_JS = r"""/* Shared on every page: scroll reveal and the lead form.
   Lead form: set LEAD_ENDPOINT to a webhook URL (e.g. n8n) to submit in the background;
   while it is empty, the form opens a prefilled email to darya@getmarketing.team instead. */
(function () {
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.1 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  var LEAD_ENDPOINT = '';
  var form = document.getElementById('lead-form'); if (!form) return;
  var T = JSON.parse(form.getAttribute('data-t'));
  var status = form.querySelector('.lf-status'), btn = form.querySelector('.lf-submit');
  document.querySelectorAll('[data-interest]').forEach(function (a) {
    a.addEventListener('click', function () { var s = form.querySelector('select[name=interest]'); if (s) s.value = a.getAttribute('data-interest'); });
  });
  function say(msg, cls) { status.textContent = msg; status.className = 'lf-status ' + (cls || ''); }
  function track() { try { if (window.gtag) window.gtag('event', 'generate_lead', { form: 'free_analysis', page: location.pathname }); } catch (e) {} }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = {}; new FormData(form).forEach(function (v, k) { d[k] = String(v).trim(); });
    if (d.fax) { say(T.ok, 'ok'); form.reset(); return; }
    if (!d.website || !d.name || !d.email) { say(T.missing, 'err'); return; }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) { say(T.email, 'err'); return; }
    delete d.fax; d.lang = document.documentElement.lang; d.page = location.pathname; d.sent_at = new Date().toISOString();
    function mailFallback() {
      var body = T.mailIntro + '\n\n' + T.lWebsite + ': ' + d.website + '\n' + T.lName + ': ' + d.name + '\n' + T.lEmail + ': ' + d.email + '\n' + T.lPhone + ': ' + (d.phone || '-') + '\n' + T.lInterest + ': ' + d.interest + '\nPage: ' + d.page;
      location.href = 'mailto:darya@getmarketing.team?subject=' + encodeURIComponent(T.subject + ' ' + d.website) + '&body=' + encodeURIComponent(body);
      say(T.mailOpened, 'ok'); track();
    }
    if (!LEAD_ENDPOINT) { mailFallback(); return; }
    btn.disabled = true; say(T.sending);
    fetch(LEAD_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); say(T.ok, 'ok'); form.reset(); track(); })
      .catch(function () { mailFallback(); })
      .then(function () { btn.disabled = false; });
  });
})();
"""

def main():
    css_written = False
    for lang, f in (("en", ROOT / "index.html"), ("de", ROOT / "de" / "index.html")):
        s = f.read_text()
        m = re.search(r"\n<style>\n(.*?)\n</style>\n", s, re.S)
        if m:
            if lang == "en":
                (ROOT / "home.css").write_text("/* Homepage base styles, shared by every page. Loaded before theme.css. */\n" + m.group(1).replace("\n  ", "\n").strip() + "\n"); css_written = True
            s = s[:m.start()] + "\n" + s[m.end():]
        s = s.replace('<link rel="stylesheet" href="/theme.css', '<link rel="stylesheet" href="/home.css?v=1" />\n<link rel="stylesheet" href="/theme.css', 1) if "/home.css" not in s else s
        # scripts: drop inline reveal/approve + lead form, keep page-specific bits
        s = re.sub(r"\n<script>\n/\* Lead form: sends.*?</script>\n", "\n", s, flags=re.S)
        s = re.sub(r"  (/\* Scroll reveal \*/\n  )?const io = new IntersectionObserver.*?io\.observe\(el\)\);\n", "", s, flags=re.S)
        s = re.sub(r"\n\n  (/\* Approve micro-interaction.*?\*/\n  )?document\.querySelectorAll\('\.approve-btn'\).*?\n  \}\);\n", "\n", s, flags=re.S)
        if "/site.js" not in s:
            s = s.replace('<script defer src="/home.js', '<script defer src="/site.js?v=1"></script>\n<script defer src="/home.js', 1)
        s = s.replace('src="logo.jpg"', 'src="/logo.jpg"').replace('src="darya.jpg"', 'src="/darya.jpg"')
        # lead section
        lm = re.search(r'<section id="start" class="lead-section">.*?</section>', s, re.S)
        s = s[:lm.start()] + lead_section(lm.group(0), lang) + s[lm.end():]
        # mission: move after the lead section
        mm = re.search(r'\n<section class="mission-section">.*?</section>\n', s, re.S)
        mission = mm.group(0); s = s[:mm.start()] + "\n" + s[mm.end():]
        s = s.replace("<!-- ===== OFFER ===== -->\n<!-- ===== ONE CLICK BAND ===== -->\n<!-- ===== MISSION ===== -->\n", "<!-- ===== ONE CLICK BAND ===== -->\n")
        lm = re.search(r'<section id="start" class="lead-section">.*?</section>\n', s, re.S)
        s = s[:lm.end()] + "\n<!-- ===== MISSION ===== -->" + mission + s[lm.end():]
        # footer: landing pages are entry points, not topics
        s = re.sub(r'<div class="ft-col ft-topics">.*?</ul></div>', "", s, flags=re.S)
        f.write_text(s); print("updated", f.relative_to(ROOT))
    (ROOT / "site.js").write_text(SITE_JS)
    assert css_written

main()

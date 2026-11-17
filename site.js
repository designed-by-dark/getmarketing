/* Shared on every page: scroll reveal and the lead form.
   Lead form: set LEAD_ENDPOINT to a webhook URL (e.g. n8n) to submit in the background;
   while it is empty, the form opens a prefilled email to darya@getmarketing.team instead. */
/* Click-to-load YouTube player: <div class="player" data-yt="ID" data-title="..."><button class="player-btn">…</button></div>.
   Nothing is requested from YouTube until the visitor clicks play. */
(function () {
  document.querySelectorAll('.player[data-yt]').forEach(function (p) {
    var b = p.querySelector('.player-btn'); if (!b) return;
    b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(p.getAttribute('data-yt')) + '?autoplay=1&rel=0';
      f.title = p.getAttribute('data-title') || 'YouTube video';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.allowFullscreen = true;
      f.referrerPolicy = 'strict-origin-when-cross-origin';
      p.replaceChild(f, b);
      try { if (window.gtag) window.gtag('event', 'video_play', { video_id: p.getAttribute('data-yt'), page: location.pathname }); } catch (e) {}
    });
  });
})();

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

/* Reviews strip: start with the first review (Nicholas) centered, and only start moving once the strip is on screen. */
(function () {
  var vp = document.querySelector('.rv-viewport'), track = vp && vp.querySelector('.rv-track');
  if (!track) return;
  var card = track.querySelector('.rv-card'); if (!card) return;
  var dur = parseFloat(getComputedStyle(track).animationDuration) || 60;
  function place() {
    var D = track.scrollWidth / 2 + 10;            /* distance of one loop (translateX(-50% - 10px)) */
    var x = vp.clientWidth / 2 - (card.offsetLeft - track.offsetLeft) - card.offsetWidth / 2; /* shift that centers the card */
    x = ((x % D) + D) % D - D;                       /* bring into the animated range [-D, 0] */
    track.style.animationDelay = (-(-x / D) * dur) + 's';
  }
  place();
  track.style.animationPlayState = 'paused';
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es, o) {
      es.forEach(function (e) { if (e.isIntersecting) { place(); track.style.animationPlayState = ''; o.disconnect(); } });
    }, { threshold: 0.4 }).observe(vp);
  } else { track.style.animationPlayState = ''; }
})();

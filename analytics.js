/*
 * GetMarketing — consent-gated web analytics
 * Loads Google Analytics 4 + Amplitude (EU data residency) only AFTER the
 * visitor grants consent. Included on every page via:
 *   <script defer src="/analytics.js"></script>
 *
 * Funnel events emitted here (acquisition part of the funnel):
 *   - "Landing Page Viewed"  (on every page load, once consented)
 *   - "Signup Started"       (on click of any app.getmarketing.team CTA)
 * Signup Completed / Onboarding * / Dashboard * live in the app
 * (app.getmarketing.team) and must be instrumented there, reusing the same
 * Amplitude project so the shared deviceId connects anonymous and known users.
 */
(function () {
  'use strict';

  // ---- Configuration -------------------------------------------------------
  // Amplitude → Settings → Projects → "default" → API Key (client-side, public):
  var AMPLITUDE_API_KEY = '76d34022534107357a0a7cef0d6030a9';
  var GA_MEASUREMENT_ID = 'G-T7EBFEM00R';
  var COOKIE_DOMAIN     = '.getmarketing.team'; // share identity across www + app subdomains
  var CONSENT_KEY       = 'gm_analytics_consent'; // localStorage: 'granted' | 'denied'
  var AMPLITUDE_SDK     = 'https://cdn.jsdelivr.net/npm/@amplitude/analytics-browser@2/lib/scripts/amplitude-min.umd.js';
  var LEADFEEDER_ID     = 'YEgkB8lJ5W14ep3Z'; // Leadfeeder / Dealfront website-visitor tracker

  // ---- Consent storage (defensive: private mode / blocked storage) ---------
  function getConsent() {
    try { return localStorage.getItem(CONSENT_KEY); } catch (e) { return null; }
  }
  function setConsent(value) {
    try { localStorage.setItem(CONSENT_KEY, value); } catch (e) {}
  }

  // ---- Google Analytics 4 (loaded only after consent) ----------------------
  function loadGA() {
    if (!GA_MEASUREMENT_ID || window.__gmGaLoaded) return;
    window.__gmGaLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_MEASUREMENT_ID);
  }

  // ---- Amplitude (EU data residency, loaded only after consent) ------------
  function loadAmplitude() {
    if (window.__gmAmpLoaded) return;
    window.__gmAmpLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = AMPLITUDE_SDK;
    s.onload = initAmplitude;
    document.head.appendChild(s);
  }

  function initAmplitude() {
    if (!window.amplitude || typeof window.amplitude.init !== 'function') return;
    if (!AMPLITUDE_API_KEY || AMPLITUDE_API_KEY.indexOf('REPLACE_WITH') === 0) {
      console.warn('[analytics] Amplitude API key is not set — skipping Amplitude init.');
      return;
    }
    window.amplitude.init(AMPLITUDE_API_KEY, {
      serverZone: 'EU',                          // REQUIRED for EU data residency (Frankfurt)
      identityStorage: 'cookie',                 // cookie (not localStorage) so deviceId can be shared…
      cookieOptions: { domain: COOKIE_DOMAIN },  // …across getmarketing.team and app.getmarketing.team
      autocapture: {
        attribution: true,        // referral / UTM context
        sessions: true,
        pageViews: false,         // we emit our own "Landing Page Viewed"
        formInteractions: false,
        fileDownloads: false,
        elementInteractions: false
      }
    });
    trackLandingPageView();
  }

  // ---- Leadfeeder / Dealfront (loaded only after consent) ------------------
  function loadLeadfeeder() {
    if (!LEADFEEDER_ID || window.__gmLfLoaded) return;
    window.__gmLfLoaded = true;
    window.ldfdr = window.ldfdr || function () {
      (ldfdr._q = ldfdr._q || []).push([].slice.call(arguments));
    };
    var first = document.getElementsByTagName('script')[0];
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://sc.lfeeder.com/lftracker_v1_' + LEADFEEDER_ID + '.js';
    first.parentNode.insertBefore(s, first);
  }

  // ---- Funnel events -------------------------------------------------------
  function trackLandingPageView() {
    if (!window.amplitude) return;
    window.amplitude.track('Landing Page Viewed', {
      page_path: location.pathname,
      page_title: document.title,
      referrer: document.referrer || undefined
    });
  }

  function wireSignupLinks() {
    var links = document.querySelectorAll('a[href*="app.getmarketing.team"]');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function (ev) {
        var el = ev.currentTarget;
        if (!window.amplitude) return;
        window.amplitude.track('Signup Started', {
          cta_text: (el.textContent || '').trim().slice(0, 80),
          cta_href: el.getAttribute('href'),
          page_path: location.pathname
        });
        // Flush before the browser navigates away to the app.
        if (typeof window.amplitude.flush === 'function') window.amplitude.flush();
      });
    }
  }

  function enableAnalytics() {
    loadGA();
    loadAmplitude();   // trackLandingPageView() runs after Amplitude finishes init
    loadLeadfeeder();
    wireSignupLinks();
  }

  // ---- Consent banner ------------------------------------------------------
  function showBanner() {
    if (document.getElementById('gm-consent')) return;

    var style = document.createElement('style');
    style.textContent =
      '#gm-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;' +
      'max-width:560px;margin:0 auto;background:#1B4332;color:#fff;border-radius:14px;' +
      'box-shadow:0 12px 40px rgba(0,0,0,.28);padding:20px 22px;box-sizing:border-box;' +
      'font-family:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}' +
      '#gm-consent p{margin:0 0 14px;font-size:14px;line-height:1.55;color:#E7F3EC;}' +
      '#gm-consent a{color:#fff;text-decoration:underline;}' +
      '#gm-consent .gm-row{display:flex;gap:10px;flex-wrap:wrap;}' +
      '#gm-consent button{flex:1 1 140px;cursor:pointer;border:0;border-radius:9px;' +
      'padding:11px 16px;font-size:14px;font-weight:600;font-family:inherit;}' +
      '#gm-consent .gm-accept{background:#52B788;color:#0A0A0A;}' +
      '#gm-consent .gm-accept:hover{background:#63c79a;}' +
      '#gm-consent .gm-decline{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.45);}' +
      '#gm-consent .gm-decline:hover{border-color:#fff;}';
    document.head.appendChild(style);

    var isDe = (document.documentElement.lang || 'en').toLowerCase().indexOf('de') === 0;
    var privacyHref = isDe ? '/datenschutz.html' : '/datenschutz-en.html';

    var wrap = document.createElement('div');
    wrap.id = 'gm-consent';
    wrap.setAttribute('role', 'dialog');
    wrap.setAttribute('aria-label', isDe ? 'Cookie-Einwilligung' : 'Cookie consent');
    wrap.innerHTML =
      '<p>' +
      (isDe
        ? 'Wir nutzen Analyse- und Tracking-Tools (Google Analytics, Amplitude, Leadfeeder), um unsere Website zu verbessern – nur mit Ihrer Einwilligung. Mehr in unserer <a href="' + privacyHref + '">Datenschutzerklärung</a>.'
        : 'We use analytics and tracking tools (Google Analytics, Amplitude, Leadfeeder) to improve our website – only with your consent. See our <a href="' + privacyHref + '">privacy policy</a>.') +
      '</p><div class="gm-row">' +
      '<button class="gm-accept" type="button">' + (isDe ? 'Akzeptieren' : 'Accept') + '</button>' +
      '<button class="gm-decline" type="button">' + (isDe ? 'Ablehnen' : 'Decline') + '</button>' +
      '</div>';
    document.body.appendChild(wrap);

    wrap.querySelector('.gm-accept').addEventListener('click', function () {
      setConsent('granted');
      wrap.parentNode && wrap.parentNode.removeChild(wrap);
      enableAnalytics();
    });
    wrap.querySelector('.gm-decline').addEventListener('click', function () {
      setConsent('denied');
      wrap.parentNode && wrap.parentNode.removeChild(wrap);
    });
  }

  // ---- Boot ----------------------------------------------------------------
  function boot() {
    var consent = getConsent();
    if (consent === 'granted') enableAnalytics();
    else if (consent === 'denied') { /* visitor declined — no tracking */ }
    else showBanner();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  // Let a footer link re-open the consent banner: onclick="gmOpenConsent();return false"
  window.gmOpenConsent = showBanner;
})();

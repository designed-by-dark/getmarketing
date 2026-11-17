/* Hamburger menu for the site header (all pages, EN + DE).
   Below 900px the nav links are hidden; this adds a toggle that opens them as a dropdown. */
(function () {
  var nav = document.querySelector('nav');
  var inner = nav && nav.querySelector('.nav-inner');
  var links = nav && nav.querySelector('.nav-links');
  if (!inner || !links) return;

  var de = (document.documentElement.lang || '').indexOf('de') === 0;
  var label = { open: de ? 'Menü öffnen' : 'Open menu', close: de ? 'Menü schließen' : 'Close menu' };

  /* Mega menu for the use-case pages (markup is static in every page, see _tools/nav_usecases.py) */
  var mcss = document.createElement('style');
  mcss.textContent =
    '.nav-dd{position:relative}' +
    '.nav-dd-t::after{content:"";display:inline-block;width:6px;height:6px;margin-left:7px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:translateY(-3px) rotate(45deg);opacity:.7}' +
    '.nav-mega{position:absolute;top:100%;left:50%;transform:translateX(-50%);padding-top:16px;display:none;z-index:70}' +
    '.nav-dd:hover .nav-mega,.nav-dd:focus-within .nav-mega{display:block}' +
    '.nav-mega-in{width:580px;display:grid;grid-template-columns:1fr 1fr;gap:4px;background:#fff;border-radius:16px;padding:10px;box-shadow:0 24px 48px -20px rgba(0,0,0,.35),0 0 0 1px rgba(0,0,0,.04)}' +
    'nav .nav-links .nav-mega a{display:block;padding:12px 14px;border-radius:11px;color:#111312;text-decoration:none;white-space:normal}' +
    'nav .nav-links .nav-mega a:hover,nav .nav-links .nav-mega a:focus-visible{background:#EEF6F0;color:#111312}' +
    'nav .nav-links .nav-mega b{display:block;font-size:15px;font-weight:650;letter-spacing:-.01em;color:#111312}' +
    'nav .nav-links .nav-mega span{display:block;margin-top:3px;font-size:13px;line-height:1.4;font-weight:400;color:#5F635F}' +
    'nav .nav-links .nav-mega a.nav-mega-all{grid-column:1/-1;font-size:13.5px;font-weight:600;color:#1B4332;padding:10px 14px;border-top:1px solid #EEEEEA;border-radius:0 0 11px 11px}' +
    '@media (max-width:900px){' +
      '.nav-mega{position:static;transform:none;padding:0;display:block}' +
      '.nav-mega-in{width:auto;grid-template-columns:1fr;box-shadow:none;padding:0 0 10px 12px;background:none;gap:0}' +
      'nav.menu-open .nav-links .nav-mega a{padding:8px 0;font-size:15px}' +
      'nav .nav-links .nav-mega span{display:none}' +
      'nav .nav-links .nav-mega a.nav-mega-all{border-top:0;padding:8px 0}' +
      '.nav-dd-t::after{display:none}' +
    '}';
  document.head.appendChild(mcss);

  var css = document.createElement('style');
  css.textContent =
    '.nav-burger{display:none;flex-shrink:0;width:40px;height:40px;margin-right:-8px;border:0;background:none;border-radius:10px;cursor:pointer;color:#111312;position:relative}' +
    '.nav-burger:hover,.nav-burger:focus-visible{background:#F2F2EF}' +
    '.nav-burger span{position:absolute;left:11px;right:11px;height:2px;border-radius:2px;background:currentColor;transition:transform .2s ease,opacity .2s ease}' +
    '.nav-burger span:nth-child(1){top:14px}.nav-burger span:nth-child(2){top:19px}.nav-burger span:nth-child(3){top:24px}' +
    'nav.menu-open .nav-burger span:nth-child(1){transform:translateY(5px) rotate(45deg)}' +
    'nav.menu-open .nav-burger span:nth-child(2){opacity:0}' +
    'nav.menu-open .nav-burger span:nth-child(3){transform:translateY(-5px) rotate(-45deg)}' +
    '@media (max-width:900px){' +
      '.nav-burger{display:block}' +
      'nav.menu-open .nav-links{display:flex!important;position:absolute;top:100%;left:0;right:0;flex-direction:column;align-items:stretch;gap:0;' +
        'background:#fff;border-bottom:1px solid #ebebeb;padding:6px 28px 18px;box-shadow:0 18px 32px -18px rgba(0,0,0,.25)}' +
      'nav.menu-open .nav-links li{border-bottom:1px solid #f0f0ee}' +
      'nav.menu-open .nav-links li:last-child{border-bottom:0}' +
      'nav.menu-open .nav-links a{display:block;padding:14px 0;font-size:17px;font-weight:500;color:#111312}' +
    '}' +
    '@media (max-width:900px){.nav-inner>.nav-lang{margin-left:auto}}' +
    '@media (max-width:600px){nav.menu-open .nav-links{padding:4px 16px 16px}}';
  document.head.appendChild(css);

  if (!links.id) links.id = 'nav-links';
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'nav-burger';
  btn.setAttribute('aria-controls', links.id);
  btn.setAttribute('aria-expanded', 'false');
  btn.setAttribute('aria-label', label.open);
  btn.innerHTML = '<span></span><span></span><span></span>';
  inner.appendChild(btn);

  function set(open) {
    nav.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? label.close : label.open);
  }
  btn.addEventListener('click', function () { set(!nav.classList.contains('menu-open')); });
  links.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('menu-open')) { set(false); btn.focus(); } });
  document.addEventListener('click', function (e) { if (!nav.contains(e.target)) set(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > 900) set(false); });
})();

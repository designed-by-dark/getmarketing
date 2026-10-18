/* Hamburger menu for the site header (all pages, EN + DE).
   Below 900px the nav links are hidden; this adds a toggle that opens them as a dropdown. */
(function () {
  var nav = document.querySelector('nav');
  var inner = nav && nav.querySelector('.nav-inner');
  var links = nav && nav.querySelector('.nav-links');
  if (!inner || !links) return;

  var de = (document.documentElement.lang || '').indexOf('de') === 0;
  var label = { open: de ? 'Menü öffnen' : 'Open menu', close: de ? 'Menü schließen' : 'Close menu' };

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
    '.nav-links .nav-menu-cta{display:none}' +
    '@media (max-width:600px){nav.menu-open .nav-links{padding:4px 16px 16px}}' +
    '@media (max-width:480px){' +
      '.nav-inner>.nav-cta{display:none!important}' +
      '.nav-inner>.nav-lang{margin-left:auto}' +
      'nav.menu-open .nav-links .nav-menu-cta{display:block;border-bottom:0;padding-top:14px}' +
      'nav.menu-open .nav-links .nav-menu-cta a{text-align:center;background:#1B4332;color:#fff;border-radius:12px;padding:13px 20px;font-size:15px;font-weight:600}' +
    '}';
  document.head.appendChild(css);

  // on small phones the header CTA moves into the menu
  var cta = inner.querySelector('.nav-cta');
  if (cta) {
    var li = document.createElement('li');
    li.className = 'nav-menu-cta';
    li.appendChild(cta.cloneNode(true)).className = '';
    links.appendChild(li);
  }

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

/* Homepage animations: before/after calendar and the weekly cycle ring. */
(function () {
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function whenVisible(el, start, stop) {
    if (!('IntersectionObserver' in window)) { start(); return; }
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.isIntersecting ? start() : stop(); });
    }, { threshold: 0.3 }).observe(el);
  }

  /* ---- Before / after: plans slide from week to week vs. get done ---- */
  var ba = document.getElementById('ba');
  if (ba) {
    var moved = ba.getAttribute('data-moved'), dropped = ba.getAttribute('data-dropped');
    var st = ba.getAttribute('data-st').split('|');
    var bItems = ba.querySelectorAll('.ba-before .ba-item'), aItems = ba.querySelectorAll('.ba-after .ba-item');
    var startCol = [0, 0, 1, 1];
    var beforeSteps = [[0, 'm'], [1, 'm'], [2, 'm'], [0, 'm'], [3, 'm'], [1, 'd'], [2, 'd']];
    var afterSteps = [[0, 1], [1, 1], [0, 2], [1, 2], [0, 3], [2, 1], [1, 3], [3, 1], [2, 2], [3, 2], [2, 3], [3, 3]];
    var bCol = [], timer = null, tick = 0;

    function place(el, col) { el.style.transform = 'translateX(' + (col * 100) + '%)'; }
    function tag(el, cls, text) { var t = el.querySelector('.ba-tag'); t.className = 'ba-tag ' + cls; t.textContent = text; }
    function reset() {
      tick = 0;
      for (var i = 0; i < 4; i++) {
        bCol[i] = startCol[i];
        place(bItems[i], startCol[i]); bItems[i].classList.remove('dropped'); tag(bItems[i], '', st[0]);
        place(aItems[i], startCol[i]); tag(aItems[i], '', st[0]);
      }
    }
    function step() {
      var b = beforeSteps[tick], a = afterSteps[tick];
      if (b) {
        var el = bItems[b[0]];
        if (b[1] === 'm') { bCol[b[0]] = Math.min(2, bCol[b[0]] + 1); place(el, bCol[b[0]]); tag(el, 'moved', moved); }
        else { el.classList.add('dropped'); tag(el, 'dropped', dropped); }
      }
      if (a) tag(aItems[a[0]], 's' + a[1], a[1] === 3 && aItems[a[0]].getAttribute('data-res') ? aItems[a[0]].getAttribute('data-res') : st[a[1]]);
      tick++;
      if (tick > afterSteps.length + 4) reset();
    }
    function finalState() {
      reset();
      for (var i = 0; i < beforeSteps.length; i++) step();
      for (; tick < afterSteps.length;) step();
    }
    if (still) finalState();
    else {
      reset();
      whenVisible(ba, function () { if (!timer) timer = setInterval(step, 1100); }, function () { clearInterval(timer); timer = null; });
    }
  }

  /* ---- Cycle ring: dot, trailing arc and active step share one clock ---- */
  var dot = document.getElementById('cyDot'), arc = document.getElementById('cyArc');
  if (dot && !still) {
    var nodes = document.querySelectorAll('.cy-node'), T = 9000, last = -1, raf = null, t0 = null;
    function frame(now) {
      if (t0 === null) t0 = now;
      var a = ((now - t0) % T) / T * 360, rad = (a - 90) * Math.PI / 180;
      dot.setAttribute('cx', 300 + 190 * Math.cos(rad));
      dot.setAttribute('cy', 260 + 190 * Math.sin(rad));
      arc.style.transform = 'rotate(' + (a - 155) + 'deg)';
      var k = Math.floor(a / 90);
      if (k !== last) { nodes.forEach(function (n, i) { n.classList.toggle('on', i === k); }); last = k; }
      raf = requestAnimationFrame(frame);
    }
    whenVisible(document.querySelector('.cy-section'), function () { if (!raf) raf = requestAnimationFrame(frame); }, function () { cancelAnimationFrame(raf); raf = null; });
  }
})();

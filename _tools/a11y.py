#!/usr/bin/env python3
"""Accessibility fixes shared by every page template. Idempotent, run it last (build_all.sh does).

  python3 _tools/a11y.py

- a skip link and a <main id="main"> landmark between the nav and the footer
- footer column headings as <h2 class="ft-h"> instead of <h4> (heading order)
- the logo image next to the visible name "GetMarketing" gets alt="" (no double announcement)
- the scrollable content calendar can be reached and scrolled with the keyboard
- empty table header cells become <td> (an empty <th> labels nothing)
"""
import re
import topics

SKIP = {"en": "Skip to content", "de": "Zum Inhalt springen"}
TABLE = {"en": "Comparison table", "de": "Vergleichstabelle"}
CAL = {"en": "Content calendar", "de": "Content-Kalender"}


def fix(s):
    m = re.search(r'<html lang="(\w+)"', s); lang = "de" if m and m.group(1) == "de" else "en"
    # main landmark
    if '<nav>' in s and '<footer class="ft">' in s:
        if not re.search(r"<main\b", s):
            s = s.replace("</nav>", '</nav>\n<main id="main">', 1)
            s = s.replace('<footer class="ft">', '</main>\n\n<footer class="ft">', 1)
        else:
            if 'id="main"' not in s:
                s = re.sub(r"<main\b", '<main id="main"', s, count=1)
            # hand-built pages close <main> before the lead form: keep everything up to the footer inside it
            head, sep, rest = s.partition('<footer class="ft">')
            if "</main>" in head and head[head.rfind("</main>") + len("</main>"):].strip():
                i = head.rfind("</main>")
                s = head[:i] + head[i + len("</main>"):].rstrip() + "\n</main>\n\n" + sep + rest
        if 'class="skip-link"' not in s:
            s = re.sub(r"(<body[^>]*>)", r'\1\n<a class="skip-link" href="#main">' + SKIP[lang] + "</a>", s, count=1)
    # footer headings
    foot = re.search(r'<footer class="ft">.*?</footer>', s, re.S)
    if foot:
        f = re.sub(r"<h4>(.*?)</h4>", r'<h2 class="ft-h">\1</h2>', foot.group(0))
        s = s[:foot.start()] + f + s[foot.end():]
    # logo next to the visible brand name
    s = s.replace('<img src="/logo.jpg" alt="GetMarketing" />\n      <span class="nav-logo-text">GetMarketing</span>',
                  '<img src="/logo.jpg" alt="" width="34" height="34" />\n      <span class="nav-logo-text">GetMarketing</span>')
    # scrollable calendar
    s = s.replace('<div class="ccal-grid"></div>', f'<div class="ccal-grid" tabindex="0" role="region" aria-label="{CAL[lang]}"></div>')
    # wide tables scroll sideways on phones: make the scroll box reachable by keyboard
    n = len(re.findall(r'<div class="lp-table reveal"', s))
    k = iter(range(1, n + 1))
    s = re.sub(r'<div class="lp-table reveal"(?: tabindex="0" role="region" aria-label="[^"]*")?>',
               lambda m: f'<div class="lp-table reveal" tabindex="0" role="region" aria-label="{TABLE[lang]}{"" if n == 1 else " " + str(next(k))}">', s)
    # empty header cells
    s = re.sub(r"<th(?: class=\"?gm\"?)?></th>", "<td></td>", s)
    return s


if __name__ == "__main__":
    n = 0
    for p in topics.all_pages():
        s = p.read_text(); o = fix(s)
        if o != s: p.write_text(o); n += 1
    print("a11y:", n, "pages updated")

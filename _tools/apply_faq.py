#!/usr/bin/env python3
"""Put the FAQ from _tools/site_faq.py onto the homepages (EN + DE), after the pricing section.

Idempotent: replaces the existing FAQ section and its FAQPage JSON-LD on every run.
  python3 _tools/apply_faq.py
"""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from site_faq import faq_section, faq_ld
from no_orphans import fix

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = {"en": (ROOT / "index.html", "pricing"), "de": (ROOT / "de" / "index.html", "preise")}
LD_START, LD_END = "<!-- FAQ JSON-LD (from _tools/site_faq.py) -->", "<!-- /FAQ JSON-LD -->"

for lang, (path, pricing_id) in PAGES.items():
    s = path.read_text()
    sec = "<!-- ===== FAQ (from _tools/site_faq.py) ===== -->\n" + faq_section(lang)
    if 'class="lp-sec lp-faq" id="faq"' in s:
        s = re.sub(r'<!-- ===== FAQ \(from _tools/site_faq.py\) ===== -->\n<section class="lp-sec lp-faq" id="faq">.*?</section>', lambda m: sec, s, count=1, flags=re.S)
    else:
        m = re.search(r'<section id="' + pricing_id + r'" class="offer-section">.*?</section>\n', s, re.S)
        assert m, (lang, "pricing section")
        s = s[:m.end()] + "\n" + sec + "\n" + s[m.end():]
    ld = LD_START + "\n" + faq_ld(lang) + "\n" + LD_END
    if LD_START in s:
        s = re.sub(re.escape(LD_START) + r".*?" + re.escape(LD_END), lambda m: ld, s, count=1, flags=re.S)
    else:
        s = s.replace("<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />", ld + "\n\n<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />", 1)
    path.write_text(fix(s))
    print("faq", lang, path.relative_to(ROOT))

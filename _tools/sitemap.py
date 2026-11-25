#!/usr/bin/env python3
"""Write sitemap.xml from the pages that are really there.

  python3 _tools/sitemap.py

- Every .html page that is indexable (no noindex) and declares itself canonical goes in.
  Offer pages (angebot/), internal pages (intern/) and redirect stubs stay out.
- lastmod is the date of the last commit that changed the page. A page with uncommitted
  changes gets today's date, so run this right before committing (the page builders call it).
"""
import datetime, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://getmarketing.team"
SKIP = ("angebot", "intern", "_tools", "_content")
TODAY = datetime.date.today().isoformat()
FIRST = ["/", "/de/"]


def _git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout.strip()


def last_changed(path):
    """YYYY-MM-DD of the last commit touching path; today if it has uncommitted changes or is new."""
    rel = str(pathlib.Path(path).resolve().relative_to(ROOT))
    if _git("status", "--porcelain", "--", rel): return TODAY
    d = _git("log", "-1", "--format=%cs", "--", rel)
    return d or TODAY


def pages():
    out = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP or rel.parts[0].startswith("."): continue
        s = p.read_text(errors="ignore")
        head = s.split("</head>", 1)[0]
        if re.search(r'<meta name="robots" content="[^"]*noindex', head): continue
        m = re.search(r'<link rel="canonical" href="([^"]+)"', head)
        if not m or not m.group(1).startswith(SITE): continue
        path = m.group(1)[len(SITE):] or "/"
        own = "/" + str(rel).replace("index.html", "")
        if path != own and path != own.replace("/./", "/"): continue  # page points to another URL
        out.append((path, last_changed(p)))
    out.sort(key=lambda u: (FIRST.index(u[0]) if u[0] in FIRST else len(FIRST), u[0].startswith("/de/"), u[0]))
    return out


def write():
    urls = pages()
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")
    return len(urls)


if __name__ == "__main__":
    print(write(), "urls in sitemap.xml")

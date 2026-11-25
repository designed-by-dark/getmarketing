#!/usr/bin/env bash
# Rebuild every generated page in the right order. Run from anywhere:
#   bash _tools/build_all.sh
# Homepages (index.html, de/index.html) are edited by hand; nav, footer, pricing and lead form
# are copied from them into all other pages, so edit them first and then run this.
set -euo pipefail
cd "$(dirname "$0")"
python3 topics.py              # footer "Solutions" block into the homepages first, the builders copy it
python3 apply_faq.py
python3 build_static_pages.py
python3 build_case_pages.py
python3 usecase_pages.py
python3 build_seo_pages.py
python3 restyle_static.py
python3 topics.py              # footer block into the hand-built pages (press, partners, legal, planner)
python3 nav_usecases.py
python3 a11y.py                # main landmark, skip link, footer headings (see the script)
python3 sitemap.py             # last: lastmod comes from git, so run it right before committing

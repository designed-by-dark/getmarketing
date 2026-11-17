#!/usr/bin/env python3
"""Put the use-case mega menu ("Use cases" / "Lösungen") into the nav of every page.

  python3 _tools/nav_usecases.py

Idempotent: replaces an existing menu entry, inserts it after the first nav link otherwise,
and sets the nav-menu.js version so browsers load the menu styles. Run it after any page builder.
Offer pages under angebot/ have no site nav and are left alone.
"""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from usecase_content import ORDER, SLUG, BASE, MENU

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAV_JS_VERSION = 3


def menu_li(lang):
    m = MENU[lang]
    items = "".join(f'<a href="{BASE[lang]}{SLUG[k][lang]}/"><b>{m[k][0]}</b><span>{m[k][1]}</span></a>' for k in ORDER)
    label = m["label"].replace(" ", "&nbsp;")
    return (f'<li class="nav-dd"><a href="{BASE[lang]}" class="nav-dd-t" aria-haspopup="true">{label}</a>'
            f'<div class="nav-mega"><div class="nav-mega-in">{items}<a class="nav-mega-all" href="{BASE[lang]}">{m["all"]}&nbsp;→</a></div></div></li>')


def apply(path):
    s = path.read_text()
    if '<ul class="nav-links">' not in s:
        return False
    lang = "de" if re.search(r'<html lang="de"', s) else "en"
    li = menu_li(lang)
    if 'class="nav-dd"' in s:
        s2 = re.sub(r'<li class="nav-dd">.*?</div></div></li>', lambda m: li, s, count=1, flags=re.S)
    else:
        s2 = re.sub(r'(<ul class="nav-links">\s*<li>.*?</li>)', lambda m: m.group(1) + "\n      " + li, s, count=1, flags=re.S)
    s2 = re.sub(r"nav-menu\.js\?v=\d+", f"nav-menu.js?v={NAV_JS_VERSION}", s2)
    if s2 != s:
        path.write_text(s2)
        return True
    return False


if __name__ == "__main__":
    changed = [p for p in sorted(ROOT.rglob("*.html")) if "angebot" not in p.parts and ".git" not in p.parts and apply(p)]
    print(len(changed), "pages updated")

#!/usr/bin/env python3
"""Keep the last word of headings, paragraphs and list items on the line before it.

Joins the last two words with &nbsp; so no word ends up alone on the last line.
Skips <script>, <style> and <textarea>. Safe to run again (idempotent).
  python3 _tools/no_orphans.py index.html de/index.html ...
"""
import re, sys, pathlib

SKIP = re.compile(r"(<(script|style|textarea)\b.*?</\2>)", re.S | re.I)
LAST = re.compile(r"[ \t\r\n]+([^\s<>\"=&]{1,14}(?:</(?:b|strong|em|a|span|i)>)*)(\s*</(?:p|li|h1|h2|h3|h4|summary|blockquote|figcaption)>)")

def fix(html):
    parts = SKIP.split(html)
    out, i = [], 0
    while i < len(parts):
        chunk = parts[i]
        if i % 3 == 0:
            chunk = LAST.sub(lambda m: "&nbsp;" + m.group(1) + m.group(2), chunk)
            out.append(chunk); i += 1
        else:
            out.append(chunk); i += 2  # the whole skipped block, then its tag-name group
    return "".join(out)

if __name__ == "__main__":
    for f in sys.argv[1:]:
        p = pathlib.Path(f); s = p.read_text(); n = fix(s)
        if n != s: p.write_text(n); print("fixed", f, n.count("&nbsp;") - s.count("&nbsp;"))

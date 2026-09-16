#!/usr/bin/env python3
"""Validate portal v2 (read-only checks)."""
import io
import re
from html.parser import HTMLParser


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag in ("section", "div", "table", "details"):
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in ("section", "div", "table", "details"):
            assert self.stack and self.stack[-1] == tag, "mismatch " + tag
            self.stack.pop()


t = io.open("cognitive-space/portal/index.v2.html", encoding="utf-8").read()
print("bytes:", len(t.encode("utf-8")))
print("data-i18n:", t.count("data-i18n"))
print("sections:", re.findall(r'<section id="([^"]+)"', t))
p = P()
p.feed(t)
print("tag-balance-ok, open:", p.stack)
keys = set(re.findall(r'data-i18n="([^"]+)"', t))
d = io.open("cognitive-space/portal/_v2dict.js", encoding="utf-8").read()
miss = [k for k in keys if (k + ":") not in d]
print("dict-missing-keys:", miss if miss else "none")
nav = re.findall(r'href="#([^"]+)"', t.split("<nav>")[1].split("</nav>")[0])
secs = re.findall(r'<section id="([^"]+)"', t)
print("nav==dom:", [n for n in nav] == secs)

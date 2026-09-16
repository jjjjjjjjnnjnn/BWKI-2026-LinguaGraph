#!/usr/bin/env python3
"""CDN/vendor gate: live pages must be self-hosted, vendor hashes pinned, no dead anchors.

Checks (exit 0 = pass, 1 = fail):
1. No external script/stylesheet/fetch in live pages
   (portal/index.html, web/index.html, web/story/index.html).
   Allowlist: github.com content links in <a href> (not scanned — only
   <script src>, <link rel=stylesheet>, fetch( patterns are checked).
2. Every file under cognitive-space/vendor/ matches VERSIONS.json sha256
   (top-level js/css entries + _font_files map).
3. No floating CDN versions (@11 / @4 / @1 style) in live pages.
4. Every href="#anchor" in portal/index.html resolves to an id="anchor".
Usage: python scripts/tools/cdn_audit.py [--help]
"""
import hashlib
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIVE = [
    "cognitive-space/portal/index.html",
    "cognitive-space/web/index.html",
    "cognitive-space/web/story/index.html",
]
VENDOR = os.path.join(BASE, "cognitive-space", "vendor")

EXT_PATTERNS = [
    re.compile(r'<script[^>]+src="https?://[^"]+"'),
    re.compile(r'<link[^>]+rel="stylesheet"[^>]+href="https?://[^"]+"'),
    re.compile(r'fetch\(\s*["\']https?://'),
]
FLOAT_PATTERNS = [
    re.compile(r'cdn\.jsdelivr\.net/npm/[a-z0-9@._-]+@\d+[^0-9.]'),
    re.compile(r'unpkg\.com/[a-z0-9@._-]+@\d+[^0-9.]'),
]


def check_external():
    errs = []
    for rel in LIVE:
        t = open(os.path.join(BASE, rel), encoding="utf-8").read()
        for pat in EXT_PATTERNS:
            for m in pat.findall(t):
                errs.append("EXTERNAL %s: %s" % (rel, m[:100]))
    return errs


def check_hashes():
    errs = []
    versions = json.load(open(os.path.join(VENDOR, "VERSIONS.json"), encoding="utf-8"))
    entries = {}
    for name, meta in versions.items():
        if name == "_font_files":
            continue
        entries[meta["local"]] = meta["sha256"]
    for rel, want in versions["_font_files"].items():
        fp = os.path.join(VENDOR, rel.replace("/", os.sep))
        if not os.path.exists(fp):
            errs.append("VENDOR-MISSING fonts/%s" % rel)
            continue
        got = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        if got != want:
            errs.append("VENDOR-HASH fonts/%s" % rel)
    for local, want in entries.items():
        fp = os.path.join(VENDOR, local.replace("/", os.sep))
        if not os.path.exists(fp):
            errs.append("VENDOR-MISSING %s" % local)
            continue
        got = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        if got != want:
            errs.append("VENDOR-HASH %s" % local)
    return errs


def check_floating():
    errs = []
    for rel in LIVE:
        t = open(os.path.join(BASE, rel), encoding="utf-8").read()
        for pat in FLOAT_PATTERNS:
            for m in pat.findall(t):
                errs.append("FLOATING %s: %s" % (rel, m))
    return errs


def check_anchors():
    errs = []
    t = open(os.path.join(BASE, LIVE[0]), encoding="utf-8").read()
    hrefs = set(re.findall(r'href="#([^"]+)"', t))
    ids = set(re.findall(r'id="([^"]+)"', t))
    for h in sorted(hrefs - ids):
        errs.append("DEAD-ANCHOR portal #%s" % h)
    return errs


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: cdn_audit.py [--help]")
        print("  Gates vendor self-hosting: no external scripts, hashes pinned, anchors live.")
        return 0
    errs = check_external() + check_hashes() + check_floating() + check_anchors()
    if errs:
        for e in errs:
            try:
                print(e)
            except UnicodeEncodeError:
                print(e.encode("ascii", "backslashreplace").decode("ascii"))
        print("CDN_GATE FAIL (%d)" % len(errs))
        return 1
    print("CDN_GATE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Mirror the portal page to the Pages root (_deploy/index.html).

The portal source lives one level deep (cognitive-space/portal/), so all
relative `../x` references must be flattened to `x` for the root copy.
Fails loudly on any unhandled `../` so new links can't silently 404.

Usage: python scripts/mirror_root.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "cognitive-space" / "portal" / "index.html"
DST = ROOT / "_deploy" / "index.html"

# Ordered: most specific first.
RULES = [
    ("'../web/index.html'", "'web/index.html'"),  # cover iframe (JS)
    ('"../web/', '"web/'),                        # gallery / 3D links
    ('"../figures/', '"figures/'),                # figure images
    ('"../docs/', '"docs/'),                      # paper md + PDF
    ('"../portal/', '"portal/'),                  # gallery links
    ('"../index.html"', '"web/index.html"'),      # fullscreen -> 3D app
]


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    for old, new in RULES:
        html = html.replace(old, new)
    import re
    leftover = sorted(set(re.findall(r'\.\./[A-Za-z0-9_.-]+', html)))
    if leftover:
        raise SystemExit(f"unhandled relative refs: {leftover}")
    DST.write_text(html, encoding="utf-8")
    print(f"  [OK] {SRC.relative_to(ROOT)} -> {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

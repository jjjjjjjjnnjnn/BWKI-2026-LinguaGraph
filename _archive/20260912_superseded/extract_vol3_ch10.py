"""Extract rough text from the local OpenStax Univ Phys Vol.3 PDF and slice Ch.10
sections 10.4-10.6 (whose web slugs 404'd). Local-only research extract."""
import re
import zlib
from pathlib import Path

PDF = Path("data/textbook/open/en_openstax_univphys3_web.pdf")
OUT = Path("data/textbook/open")
LIC = "License: CC BY-NC-SA 4.0 (OpenStax University Physics Vol.3). Local research copy only, not for redistribution or LLM training.\n"


def main() -> None:
    data = PDF.read_bytes()
    streams = re.findall(rb"stream\r?\n(.*?)endstream", data, re.S)
    chunks = []
    for s in streams:
        try:
            d = zlib.decompress(s)
        except Exception:
            continue
        parts = re.findall(rb"\((?:[^()\\]|\\.)*\)", d)
        if parts:
            chunks.append(b" ".join(p[1:-1] for p in parts))
    full = b"\n".join(chunks).decode("latin1", "replace")
    full = re.sub(r"\\n", "\n", full)
    print("extracted chars:", len(full))
    for kw in ["10.4", "10.5", "10.6", "10.7", "Summary", "Conceptual Questions"]:
        idxs = [m.start() for m in re.finditer(re.escape(kw), full)][:6]
        print(kw, idxs)
    heads = ["10.4 Nuclear Fission", "10.5 Nuclear Fusion",
             "10.6 Medical Applications", "Chapter 11", "11.1"]
    pos = {}
    for h in heads:
        m = re.search(re.escape(h), full)
        pos[h] = m.start() if m else -1
    print(pos)
    if pos["10.4 Nuclear Fission"] < 0:
        print("heading not found in extract; abort")
        return
    end = pos["Chapter 11"] if pos["Chapter 11"] > 0 else len(full)
    body = full[pos["10.4 Nuclear Fission"]:end]
    (OUT / "en_openstax_univphys3_sec10-4_to_10-6_fission-fusion-medical.txt").write_text(
        "# OpenStax University Physics Vol.3 Ch.10 sections 10.4-10.6 "
        "(web slugs returned 404; sliced from local full-book PDF)\n"
        "# Source PDF: https://assets.openstax.org/oscms-prodcms/media/documents/"
        "university-physics-volume-3_-_WEB.pdf\n# " + LIC + "\n" + body,
        encoding="utf-8",
    )
    print("wrote slice chars:", len(body))


if __name__ == "__main__":
    main()

"""Fetch individual OpenStax section pages (single-page reads, CC BY-NC-SA 4.0,
local research copies only — no site crawl). Validates each page contains the
expected section number; logs failures for manual fix.
Writes to data/textbook/open/ (gitignored).
Usage: python scripts/fetch_openstax_sections.py
"""
import html as ihtml
import re
import urllib.request
from pathlib import Path

OUT = Path("data/textbook/open")
UA = {"User-Agent": "BWKI-2026-LinguaGraph research (single-page fetch; contact via repo)"}
LIC = "License: CC BY-NC-SA 4.0 (OpenStax). Local research copy only, not for redistribution or LLM training."

BOOKS = {
    "chemistry-2e": "chem2e",
    "university-physics-volume-2": "univphys2",
    "university-physics-volume-3": "univphys3",
}

# (book, chapter, section, slug)
SECTIONS = [
    # Chemistry 2e
    ("chemistry-2e", 6, 1, "6-1-electromagnetic-energy"),
    ("chemistry-2e", 6, 2, "6-2-the-bohr-model"),
    ("chemistry-2e", 6, 3, "6-3-development-of-quantum-theory"),
    ("chemistry-2e", 6, 4, "6-4-electronic-structure-of-atoms-electron-configurations"),
    ("chemistry-2e", 6, 5, "6-5-periodic-variations-in-element-properties"),
    ("chemistry-2e", 7, 1, "7-1-ionic-bonding"),
    ("chemistry-2e", 7, 2, "7-2-covalent-bonding"),
    ("chemistry-2e", 7, 3, "7-3-lewis-symbols-and-structures"),
    ("chemistry-2e", 7, 4, "7-4-formal-charges-and-resonance"),
    ("chemistry-2e", 7, 5, "7-5-strengths-of-ionic-and-covalent-bonds"),
    ("chemistry-2e", 7, 6, "7-6-molecular-structure-and-polarity"),
    ("chemistry-2e", 8, 1, "8-1-valence-bond-theory"),
    ("chemistry-2e", 8, 2, "8-2-hybrid-atomic-orbitals"),
    ("chemistry-2e", 8, 3, "8-3-multiple-bonds"),
    ("chemistry-2e", 8, 4, "8-4-molecular-orbital-theory"),
    ("chemistry-2e", 16, 1, "16-1-spontaneity"),
    ("chemistry-2e", 16, 2, "16-2-entropy"),
    ("chemistry-2e", 16, 3, "16-3-the-second-and-third-laws-of-thermodynamics"),
    ("chemistry-2e", 16, 4, "16-4-free-energy"),
    ("chemistry-2e", 17, 1, "17-1-review-of-redox-chemistry"),
    ("chemistry-2e", 17, 2, "17-2-galvanic-cells"),
    ("chemistry-2e", 17, 3, "17-3-electrode-and-cell-potentials"),
    ("chemistry-2e", 17, 4, "17-4-potential-free-energy-and-equilibrium"),
    ("chemistry-2e", 17, 5, "17-5-batteries-and-fuel-cells"),
    ("chemistry-2e", 17, 6, "17-6-corrosion"),
    ("chemistry-2e", 17, 7, "17-7-electrolysis"),
    ("chemistry-2e", 20, 1, "20-1-hydrocarbons"),
    ("chemistry-2e", 20, 2, "20-2-alcohols-and-ethers"),
    ("chemistry-2e", 20, 3, "20-3-aldehydes-ketones-carboxylic-acids-and-esters"),
    ("chemistry-2e", 20, 4, "20-4-amines-and-amides"),
    ("chemistry-2e", 21, 1, "21-1-nuclear-structure-and-stability"),
    ("chemistry-2e", 21, 2, "21-2-nuclear-equations"),
    ("chemistry-2e", 21, 3, "21-3-radioactive-decay"),
    ("chemistry-2e", 21, 4, "21-4-transmutation-and-nuclear-energy"),
    ("chemistry-2e", 21, 5, "21-5-uses-of-radioisotopes"),
    ("chemistry-2e", 21, 6, "21-6-biological-effects-of-radiation"),
    # University Physics Vol. 2
    ("university-physics-volume-2", 10, 1, "10-1-electromotive-force"),
    ("university-physics-volume-2", 10, 2, "10-2-resistors-in-series-and-parallel"),
    ("university-physics-volume-2", 10, 3, "10-3-kirchhoffs-rules"),
    ("university-physics-volume-2", 10, 4, "10-4-electrical-measuring-instruments"),
    ("university-physics-volume-2", 10, 5, "10-5-rc-circuits"),
    ("university-physics-volume-2", 10, 6, "10-6-household-wiring-and-electrical-safety"),
    ("university-physics-volume-2", 13, 1, "13-1-faradays-law"),
    ("university-physics-volume-2", 13, 2, "13-2-lenzs-law"),
    ("university-physics-volume-2", 13, 3, "13-3-motional-emf"),
    ("university-physics-volume-2", 13, 4, "13-4-induced-electric-fields"),
    ("university-physics-volume-2", 13, 5, "13-5-eddy-currents"),
    ("university-physics-volume-2", 13, 6, "13-6-electric-generators-and-back-emf"),
    ("university-physics-volume-2", 13, 7, "13-7-applications-of-electromagnetic-induction"),
    ("university-physics-volume-2", 14, 1, "14-1-mutual-inductance"),
    ("university-physics-volume-2", 14, 2, "14-2-self-inductance-and-inductors"),
    ("university-physics-volume-2", 14, 3, "14-3-energy-in-a-magnetic-field"),
    ("university-physics-volume-2", 14, 4, "14-4-rl-circuits"),
    ("university-physics-volume-2", 14, 5, "14-5-oscillations-in-an-lc-circuit"),
    ("university-physics-volume-2", 14, 6, "14-6-rlc-series-circuits"),
    ("university-physics-volume-2", 15, 1, "15-1-ac-sources"),
    ("university-physics-volume-2", 15, 2, "15-2-simple-ac-circuits"),
    ("university-physics-volume-2", 15, 3, "15-3-rlc-series-circuits-with-ac"),
    ("university-physics-volume-2", 15, 4, "15-4-power-in-an-ac-circuit"),
    ("university-physics-volume-2", 15, 5, "15-5-resonance-in-an-ac-circuit"),
    ("university-physics-volume-2", 15, 6, "15-6-transformers"),
    ("university-physics-volume-2", 16, 1, "16-1-maxwells-equations-and-electromagnetic-waves"),
    ("university-physics-volume-2", 16, 2, "16-2-plane-electromagnetic-waves"),
    ("university-physics-volume-2", 16, 3, "16-3-energy-carried-by-electromagnetic-waves"),
    ("university-physics-volume-2", 16, 4, "16-4-momentum-and-radiation-pressure"),
    # University Physics Vol. 3 (nuclear)
    ("university-physics-volume-3", 10, 1, "10-1-properties-of-nuclei"),
    ("university-physics-volume-3", 10, 2, "10-2-nuclear-binding-energy"),
    ("university-physics-volume-3", 10, 3, "10-3-radioactive-decay"),
    ("university-physics-volume-3", 10, 4, "10-4-nuclear-reactions"),
    ("university-physics-volume-3", 10, 5, "10-5-fission"),
    ("university-physics-volume-3", 10, 6, "10-6-nuclear-fusion"),
    ("university-physics-volume-3", 10, 7, "10-7-medical-applications-and-biological-effects-of-nuclear-radiation"),
]


def clean(html_text: str) -> str:
    html_text = re.sub(r"(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", html_text)
    text = re.sub(r"(?s)<[^>]+>", " ", html_text)
    text = ihtml.unescape(text)
    text = re.sub(r"[ \t\xa0]+", " ", text)
    lines = [ln.strip() for ln in text.splitlines() if len(ln.strip()) > 1]
    out = []
    for ln in lines:
        if not out or out[-1] != ln:
            out.append(ln)
    return "\n".join(out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ok, fail = 0, []
    for book, ch, sec, slug in SECTIONS:
        url = f"https://openstax.org/books/{book}/pages/{slug}"
        fname = f"en_openstax_{BOOKS[book]}_sec{ch:02d}-{sec}_{slug.split('-', 2)[2]}.txt"
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                body = clean(r.read().decode("utf-8", "replace"))
        except Exception as exc:  # noqa: BLE001
            fail.append((fname, f"fetch: {exc}"))
            continue
        marker = f"{ch}.{sec}"
        if marker not in body or len(body) < 2000:
            fail.append((fname, f"validate: marker={marker in body} len={len(body)}"))
            continue
        head = f"# OpenStax {book} {marker}\n# Source: {url}\n# {LIC}\n\n"
        (OUT / fname).write_text(head + body, encoding="utf-8")
        ok += 1
        print(f"OK {fname}: {len(body)} chars")
    print(f"\n{ok} ok, {len(fail)} failed")
    for f, why in fail:
        print(f"FAIL {f}: {why}")


if __name__ == "__main__":
    main()

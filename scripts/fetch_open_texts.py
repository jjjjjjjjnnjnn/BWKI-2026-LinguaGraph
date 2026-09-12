"""Fetch public CC/open web pages (OpenStax chapters, MIT OCW syllabi) and save
plain-text extracts with license headers. Read-only, one page per URL, no crawling.
Usage: python scripts/fetch_open_texts.py
Writes to data/textbook/open/ (gitignored).
"""
import html as ihtml
import re
import urllib.request
from pathlib import Path

OUT = Path("data/textbook/open")
UA = {"User-Agent": "BWKI-2026-LinguaGraph research (single-page fetch; contact via repo)"}

JOBS = [
    # (outfile, url, license_line, description)
    ("en_openstax_chem2e_ch06.txt",
     "https://openstax.org/books/chemistry-2e/pages/6-introduction",
     "License: CC BY-NC-SA 4.0 (OpenStax Chemistry 2e). Local research copy only.",
     "OpenStax Chemistry 2e Ch6 Electronic Structure and Periodic Properties"),
    ("en_openstax_chem2e_ch07.txt",
     "https://openstax.org/books/chemistry-2e/pages/7-introduction",
     "License: CC BY-NC-SA 4.0 (OpenStax Chemistry 2e). Local research copy only.",
     "OpenStax Chemistry 2e Ch7 Chemical Bonding and Molecular Geometry"),
    ("en_openstax_chem2e_ch08.txt",
     "https://openstax.org/books/chemistry-2e/pages/8-introduction",
     "License: CC BY-NC-SA 4.0 (OpenStax Chemistry 2e). Local research copy only.",
     "OpenStax Chemistry 2e Ch8 Advanced Theories of Covalent Bonding"),
    ("en_openstax_chem2e_ch16.txt",
     "https://openstax.org/books/chemistry-2e/pages/16-introduction",
     "License: CC BY-NC-SA 4.0 (OpenStax Chemistry 2e). Local research copy only.",
     "OpenStax Chemistry 2e Ch16 Thermodynamics"),
    ("en_openstax_chem2e_ch17.txt",
     "https://openstax.org/books/chemistry-2e/pages/17-introduction",
     "License: CC BY-NC-SA 4.0 (OpenStax Chemistry 2e). Local research copy only.",
     "OpenStax Chemistry 2e Ch17 Electrochemistry"),
    ("en_openstax_chem2e_ch20.txt",
     "https://openstax.org/books/chemistry-2e/pages/20-introduction",
     "License: CC BY-NC-SA 4.0 (OpenStax Chemistry 2e). Local research copy only.",
     "OpenStax Chemistry 2e Ch20 Organic Chemistry"),
    ("en_openstax_chem2e_ch21.txt",
     "https://openstax.org/books/chemistry-2e/pages/21-introduction",
     "License: CC BY-NC-SA 4.0 (OpenStax Chemistry 2e). Local research copy only.",
     "OpenStax Chemistry 2e Ch21 Nuclear Chemistry"),
    ("en_mit560_syllabus.txt",
     "https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/syllabus",
     "License: CC BY-NC-SA 4.0 (MIT OCW). Syllabus metadata only (module mapping evidence).",
     "MIT OCW 5.60 Thermodynamics & Kinetics (Spring 2008) syllabus"),
    ("en_mit512_syllabus.txt",
     "https://ocw.mit.edu/courses/5-12-organic-chemistry-i-spring-2005/pages/syllabus",
     "License: CC BY-NC-SA 4.0 (MIT OCW). Syllabus metadata only (module mapping evidence).",
     "MIT OCW 5.12 Organic Chemistry I (Spring 2005) syllabus"),
    ("en_mit801sc_syllabus.txt",
     "https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/pages/syllabus",
     "License: CC BY-NC-SA 4.0 (MIT OCW). Syllabus metadata only (module mapping evidence).",
     "MIT OCW 8.01SC Classical Mechanics (Fall 2016) syllabus"),
    ("en_mit802_syllabus.txt",
     "https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2007/pages/syllabus",
     "License: CC BY-NC-SA 4.0 (MIT OCW). Syllabus metadata only (module mapping evidence).",
     "MIT OCW 8.02 Physics II: Electricity & Magnetism (Spring 2007) syllabus"),
    ("en_mit513_home.txt",
     "https://ocw.mit.edu/courses/5-13-organic-chemistry-ii-fall-2006",
     "License: CC BY-NC-SA 4.0 (MIT OCW). Course-home metadata only (module mapping evidence).",
     "MIT OCW 5.13 Organic Chemistry II (Fall 2006) course home"),
]


def clean(html_text: str) -> str:
    # drop scripts/styles/nav/footer noise, then tags
    html_text = re.sub(r"(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", html_text)
    text = re.sub(r"(?s)<[^>]+>", " ", html_text)
    text = ihtml.unescape(text)
    text = re.sub(r"[ \t\xa0]+", " ", text)
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if len(ln) > 1]
    # dedupe consecutive repeats (Next.js hydration duplicates)
    out = []
    for ln in lines:
        if not out or out[-1] != ln:
            out.append(ln)
    return "\n".join(out)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode("utf-8", "replace")
    return raw


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for fname, url, lic, desc in JOBS:
        try:
            body = clean(fetch(url))
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"FAIL {fname}: {exc}")
            continue
        head = f"# {desc}\n# Source: {url}\n# {lic}\n# Fetched single page for local research use.\n\n"
        (OUT / fname).write_text(head + body, encoding="utf-8")
        print(f"OK {fname}: {len(body)} chars")


if __name__ == "__main__":
    main()

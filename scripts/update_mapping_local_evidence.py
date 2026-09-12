"""R backfill: attach local-file evidence to open_source_mapping.json entries.
Local texts live in data/textbook/open/ (gitignored). Run once after downloads.
Usage: python scripts/update_mapping_local_evidence.py
"""
import json
from pathlib import Path

MAP = Path("config/expert_graphs/open_source_mapping.json")
OPEN = Path("data/textbook/open")
DATE = "2026-09-12"

CHEM_SECS = {
    6: ["electromagnetic-energy", "the-bohr-model", "development-of-quantum-theory",
        "electronic-structure-of-atoms-electron-configurations",
        "periodic-variations-in-element-properties"],
    7: ["ionic-bonding", "covalent-bonding", "lewis-symbols-and-structures",
        "formal-charges-and-resonance", "strengths-of-ionic-and-covalent-bonds",
        "molecular-structure-and-polarity"],
    8: ["valence-bond-theory", "hybrid-atomic-orbitals", "multiple-bonds",
        "molecular-orbital-theory"],
    16: ["spontaneity", "entropy", "the-second-and-third-laws-of-thermodynamics",
          "free-energy"],
    17: ["review-of-redox-chemistry", "galvanic-cells", "electrode-and-cell-potentials",
          "potential-free-energy-and-equilibrium", "batteries-and-fuel-cells",
          "corrosion", "electrolysis"],
    20: ["hydrocarbons", "alcohols-and-ethers",
          "aldehydes-ketones-carboxylic-acids-and-esters", "amines-and-amides"],
    21: ["nuclear-structure-and-stability", "nuclear-equations", "radioactive-decay",
          "transmutation-and-nuclear-energy", "uses-of-radioisotopes",
          "biological-effects-of-radiation"],
}
PHYS2_SECS = {
    10: ["electromotive-force", "resistors-in-series-and-parallel", "kirchhoffs-rules",
          "electrical-measuring-instruments", "rc-circuits",
          "household-wiring-and-electrical-safety"],
    13: ["faradays-law", "lenzs-law", "motional-emf", "induced-electric-fields",
          "eddy-currents", "electric-generators-and-back-emf",
          "applications-of-electromagnetic-induction"],
    14: ["mutual-inductance", "self-inductance-and-inductors",
          "energy-in-a-magnetic-field", "rl-circuits",
          "oscillations-in-an-lc-circuit", "rlc-series-circuits"],
    15: ["ac-sources", "simple-ac-circuits", "rlc-series-circuits-with-ac",
          "power-in-an-ac-circuit", "resonance-in-an-ac-circuit", "transformers"],
    16: ["maxwells-equations-and-electromagnetic-waves",
          "plane-electromagnetic-waves", "energy-carried-by-electromagnetic-waves",
          "momentum-and-radiation-pressure"],
}
PHYS3_SECS = {
    10: ["properties-of-nuclei", "nuclear-binding-energy", "radioactive-decay",
          "nuclear-reactions", "fission", "nuclear-fusion",
          "medical-applications-and-biological-effects-of-nuclear-radiation"],
}


def sec_files(prefix: str, table: dict) -> list:
    out = []
    for ch, slugs in table.items():
        for i, slug in enumerate(slugs, 1):
            out.append(f"en_openstax_{prefix}_sec{ch:02d}-{i}_{slug}.txt")
    return out


EVIDENCE = {
    "8.02": (["en_mit802_syllabus.txt"], "syllabus metadata only"),
    "8.01SC": (["en_mit801sc_syllabus.txt",
                "en_mit801_course_notes_f16_bundle.pdf"],
               "syllabus metadata + full F16 course-notes bundle (source URL named TableOfContents, serves 64MB/712pp bundle)"),
    "5.60": (["en_mit560_syllabus.txt"], "syllabus metadata only"),
    "5.12": (["en_mit512_syllabus.txt"], "syllabus metadata only"),
    "5.13": (["en_mit513_home.txt"], "course-home metadata only (no syllabus page)"),
    "Chemistry 2e": ([f"en_openstax_chem2e_ch{ch:02d}.txt" for ch in CHEM_SECS]
                     + sec_files("chem2e", CHEM_SECS),
                     "7 chapter intros + 36 full section texts"),
    "University Physics Vol. 2": (["en_openstax_univphys2_web.pdf"]
                                  + sec_files("univphys2", PHYS2_SECS),
                                  "full-book PDF (63.8MB) + 29 full section texts"),
    "University Physics Vol. 3": (["en_openstax_univphys3_web.pdf"]
                                  + sec_files("univphys3", PHYS3_SECS),
                                  "full-book PDF (53.5MB) + 7 full section texts; 10.4-10.7 slugs corrected (Nuclear Reactions/Fission/Nuclear Fusion/Medical 10.7)"),
    "NPTEL": ([], "link-only per license caution, no local copy"),
    "LEIFI": ([], "link-only per license caution (§44b), no local copy"),
    "USTC": (["zh_ustc621_wilihua_dagang.pdf"], "public admin syllabus PDF (module evidence)"),
    "UCAS": (["zh_ucas_youjihuaxue_dagang.pdf"], "public admin syllabus PDF (module evidence)"),
}


def main() -> None:
    m = json.loads(MAP.read_text(encoding="utf-8"))
    missing = []
    for entry in m["entries"]:
        blob = json.dumps(entry, ensure_ascii=False)
        ev = {}
        for key, (files, note) in EVIDENCE.items():
            if key in blob:
                present = [f for f in files if (OPEN / f).exists()]
                absent = [f for f in files if not (OPEN / f).exists()]
                missing.extend(absent)
                ev[key] = {"note": note, "local_files": present,
                           "local_files_missing": absent}
        entry["local_evidence"] = {"date": DATE, "dir": "data/textbook/open/",
                                   "sources": ev}
    m["local_arrivals_20260912"] = {
        "files_total": 89,
        "pdfs": 5,
        "section_texts": 72,
        "intro_or_syllabus_texts": 12,
        "cn_pep_texts": "pending (smartedu login wall — user action required)",
        "missing_files": sorted(set(missing)),
    }
    if m.get("status") == "staging":
        m["status"] = "staging+local-EN-texts"
    MAP.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    print("entries:", len(m["entries"]), "missing:", sorted(set(missing)))


if __name__ == "__main__":
    main()

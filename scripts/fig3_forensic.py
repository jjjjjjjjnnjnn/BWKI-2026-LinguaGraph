"""F3 forensic: recompute math CDS-by-level under all archived graph/definition
combos; compare against published 0.271 (middle) / 0.073 (high).
Writes outputs/figures/fig3_forensic_data.csv (deterministic).
Verdict: UNREPRODUCIBLE (fig5 precedent class) — see docs/fig3_cds_forensic.md.
Usage: python scripts/fig3_forensic.py
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

rows = []


def add(source, definition, lv, n, e):
    dens = 2 * e / (n * (n - 1)) if n > 1 else 0.0
    en = e / n if n else 0.0
    rows.append({"source": source, "definition": definition, "level": lv,
                 "n": n, "e": e, "density": round(dens, 4),
                 "E/N": round(en, 4)})


def main() -> None:
    full = json.loads(Path("config/expert_graphs/math_full.json")
                      .read_text(encoding="utf-8"))
    nodes = {n["name"]: n.get("level", "?") for n in full["concepts"]}
    # A: raw full graph, all internal edges
    by_n: dict = defaultdict(set)
    by_e: dict = defaultdict(int)
    for n, lv in nodes.items():
        by_n[lv].add(n)
    for r in full["relations"]:
        a, b = r["source"], r["target"]
        if a in nodes and b in nodes and nodes[a] == nodes[b]:
            by_e[nodes[a]] += 1
    for lv in ("elementary", "middle", "high", "college"):
        add("math_full raw", "density all-internal",
            lv, len(by_n[lv]), by_e[lv])
    # B/C: by edge type
    for etype in ("requires", "prerequisite"):
        bn: dict = defaultdict(set)
        be: dict = defaultdict(int)
        for r in full["relations"]:
            if r.get("type") != etype:
                continue
            a, b = r["source"], r["target"]
            if a in nodes and b in nodes and nodes[a] == nodes[b]:
                bn[nodes[a]].add(a)
                bn[nodes[a]].add(b)
                be[nodes[a]] += 1
        for lv in ("elementary", "middle", "high", "college"):
            add("math_full raw", f"density {etype}-only same-level-edges",
                lv, len(bn[lv]), be[lv])
    # D: published vis snapshot (556/238)
    snap = json.loads(Path("outputs/physics_comparison.json")
                      .read_text(encoding="utf-8"))
    for lv, v in snap["math"]["cds"].items():
        add("physics_comparison snapshot (556/238)", "density (archived)",
            lv, v["nodes"], v["edges"])
    with open("outputs/figures/fig3_forensic_data.csv", "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows; published claim middle=0.271 high=0.073")
    for r in rows:
        if r["level"] in ("middle", "high"):
            print(r)


if __name__ == "__main__":
    main()

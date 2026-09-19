#!/usr/bin/env python3
"""Deterministic T1 agreement scoring (zero API).

Compares each new T1 arm against mimo baseline (baseline-relative only;
mimo itself unverified). Matcher: normalized name equality OR alias
cross-match (deterministic, documented). Relations: ordered endpoint pairs,
type ignored (rel_agree per audit method).
Inputs: research/ensemble_v2/<ns>/<base>.r1.json + data/math_extractions/<base>.json
Outputs: research/mimo_spark_replication/T1_AGREEMENT.json + .md
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REP = os.path.join(BASE, "research", "mimo_spark_replication")
ENS = os.path.join(BASE, "research", "ensemble_v2")
MEX = os.path.join(BASE, "data", "math_extractions")
ARMS = ["muse-spark-1.3-contributor-free", "muse-spark-1.2-contributor-free",
        "mm-minimax-m3", "r4-deepseek-v4.1-flash",
        "sn-sensenova-6.7-flash-lite", "sn-deepseek-v4-flash", "sn-glm-5.2",
        "sn-sensenova-6.8-flash-lite",
        "sn-deepseek-v4-pro", "sn-kimi-k3", "sn-sensenova-u1.5-fast"]
# NOTE 2026-09-18: mimo-v2.5-free retired by owner decision; outputs archived at
# research/archive_mimo-v2.5-free_20260918/ (excluded from scoring).
# NOTE 2026-09-18: sn-sensenova-u1-fast + sn-sensenova-u1.5-lite EXCLUDED by owner
# decision (image-generation models, not chat) — never run, no outputs.


def norm(s):
    return "".join(str(s).lower().split()).replace("-", "").replace("_", "").replace("\u00df", "ss")


def cmap(concepts):
    m = {}
    for c in concepts:
        if not isinstance(c, dict):
            continue
        keys = {norm(c.get("name", ""))}
        for a in c.get("aliases", []) or []:
            if a:
                keys.add(norm(a))
        keys.discard("")
        for k in keys:
            m.setdefault(k, set()).add(norm(c.get("name", "")))
    return m


def agree(new_cs, ref_cs):
    # REAUDIT 2026-09-19 known limitation (frozen; concept-level rescoring in
    # T1_AGREEMENT_reaudit_20260919.json: micro-P 0.26-0.41 vs 0.21-0.32 here):
    # every alias expands to an independent key, so inter/n_new/n_ref scale with
    # alias COUNT, not concept count. Do NOT change without full refreeze.
    nm, rm = cmap(new_cs), cmap(ref_cs)
    inter = 0
    for k, names in nm.items():
        if k in rm:
            inter += 1
    p = inter / max(len(nm), 1)
    r = inter / max(len(rm), 1)
    return p, r, inter, len(nm), len(rm)


def rels(concepts, relations):
    nm = cmap(concepts)
    out = set()
    for x in relations or []:
        if not isinstance(x, dict):
            continue
        s, t = norm(x.get("source", "")), norm(x.get("target", ""))
        if s in nm and t in nm:
            out.add((s, t))
    return out


def main():
    bases = None
    table = {}
    for arm in ARMS:
        ddir = os.path.join(ENS, arm)
        if not os.path.isdir(ddir):
            table[arm] = {"n": 0, "status": "missing (not run or archived)"}
            continue
        files = sorted(f for f in os.listdir(ddir) if f.endswith(".r1.json"))
        if bases is None:
            bases = [f[:-8] for f in files]
        rows = []
        for f in files:
            b = f[:-8]
            try:
                new = json.load(open(os.path.join(ddir, f), encoding="utf-8"))
                ref = json.load(open(os.path.join(MEX, b + ".json"), encoding="utf-8"))
            except Exception as e:
                rows.append({"base": b, "error": "%s" % type(e).__name__})
                continue
            nc = (new.get("parsed") or new).get("extracted_concepts", [])
            nr = (new.get("parsed") or new).get("extracted_relations", [])
            rc = ref.get("extracted_concepts", [])
            rr = ref.get("extracted_relations", [])
            p, r, inter, nn, rn = agree(nc, rc)
            ra = len(rels(nc, nr) & rels(rc, rr))
            lang = b.split("_")[0]
            rows.append({"base": b, "lang": lang, "p": round(p, 4), "r": round(r, 4),
                         "inter": inter, "n_new": nn, "n_ref": rn,
                         "rel_agree": ra, "n_rel_new": len(rels(nc, nr)),
                         "n_rel_ref": len(rels(rc, rr)),
                         "gate": new.get("gate_pass")})
        ok = [x for x in rows if "error" not in x]
        table[arm] = {
            "n": len(ok),
            "micro_p": round(sum(x["inter"] for x in ok) / max(sum(x["n_new"] for x in ok), 1), 4),
            "micro_r": round(sum(x["inter"] for x in ok) / max(sum(x["n_ref"] for x in ok), 1), 4),
            "mean_rel_agree": round(sum(x["rel_agree"] for x in ok) / max(len(ok), 1), 2),
            "rows": rows,
        }
    json.dump(table, open(os.path.join(REP, "T1_AGREEMENT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    L = ["# T1 Agreement vs mimo baseline (baseline-relative; mimo unverified)", "",
         "Matcher: normalized name equality OR alias cross-match. rel_agree: ordered endpoint pairs, type ignored.",
         "",
         "| arm | files | micro-P | micro-R | mean rel_agree |",
         "|---|---|---|---|---|"]
    for arm, t in table.items():
        if t.get("status", "").startswith("missing") or t.get("n", -1) == 0:
            L.append("| %s | %d | missing/partial | | |" % (arm, t.get("n", 0)))
            continue
        L.append("| %s | %d | %.4f | %.4f | %.2f |" % (
            arm, t["n"], t["micro_p"], t["micro_r"], t["mean_rel_agree"]))
    L += ["", "## Per-file", "",
          "| arm | base | P | R | inter | new/ref | rel_agree | gate |",
          "|---|---|---|---|---|---|---|---|"]
    for arm, t in table.items():
        if t.get("status", "").startswith("missing"):
            continue
        for x in t["rows"]:
            if "error" in x:
                L.append("| %s | %s | ERROR %s | | | | | |" % (arm, x["base"], x["error"]))
            else:
                L.append("| %s | %s | %.3f | %.3f | %d | %d/%d | %d | %s |" % (
                    arm, x["base"], x["p"], x["r"], x["inter"],
                    x["n_new"], x["n_ref"], x["rel_agree"], x["gate"]))
    open(os.path.join(REP, "T1_AGREEMENT.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    for arm, t in table.items():
        if t.get("status", "").startswith("missing") or t.get("n", -1) == 0:
            print("%s MISSING/EMPTY" % arm)
            continue
        print("%s micro-P/R=%.3f/%.3f rel=%.2f" % (arm, t["micro_p"], t["micro_r"], t["mean_rel_agree"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

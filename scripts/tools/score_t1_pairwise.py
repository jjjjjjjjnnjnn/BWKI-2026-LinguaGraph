#!/usr/bin/env python3
"""Deterministic T1 all-vs-all agreement (zero API).

Replaces star-vs-unverified-mimo (REPORT F4 caveat) with inter-model
consensus among complete arms. Matcher/relations identical to
score_t1_agreement.py (norm/cmap/agree/rels, type ignored).
Inputs: research/ensemble_v2/<ns>/<base>.r1.json (5x 11/11 arms + r4 10/11).
Outputs: research/mimo_spark_replication/T1_PAIRWISE.json + .md
Note: consensus != correctness (shared hallucinations inflate agreement).
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REP = os.path.join(BASE, "research", "mimo_spark_replication")
ENS = os.path.join(BASE, "research", "ensemble_v2")
FULL5 = ["muse-spark-1.3-contributor-free", "muse-spark-1.2-contributor-free",
         "mm-minimax-m3", "sn-glm-5.2", "sn-sensenova-6.8-flash-lite"]
R4 = "r4-deepseek-v4.1-flash"


def norm(s):
    return "".join(str(s).lower().split()).replace("-", "").replace("_", "").replace("ß", "ss")


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
    nm, rm = cmap(new_cs), cmap(ref_cs)
    inter = sum(1 for k in nm if k in rm)
    return inter, len(nm), len(rm)


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


def load(arm):
    d = {}
    ddir = os.path.join(ENS, arm)
    for f in sorted(os.listdir(ddir)):
        if not f.endswith(".r1.json"):
            continue
        b = f[:-8]
        j = json.load(open(os.path.join(ddir, f), encoding="utf-8"))
        p = j.get("parsed") or j
        d[b] = (p.get("extracted_concepts", []), p.get("extracted_relations", []))
    return d


def pair_stats(ca, cb, shared):
    si = sn_a = sn_b = sr = 0
    for b in shared:
        i, na, nb = agree(ca[b][0], cb[b][0])
        si += i
        sn_a += na
        sn_b += nb
        sr += len(rels(ca[b][0], ca[b][1]) & rels(cb[b][0], cb[b][1]))
    n = len(shared)
    P = si / max(sn_a, 1)
    R = si / max(sn_b, 1)
    F1 = 2 * P * R / max(P + R, 1e-9)
    return {"n_bases": n, "P": round(P, 4), "R": round(R, 4), "F1": round(F1, 4),
            "mean_shared_rels": round(sr / max(n, 1), 2)}


def main():
    data = {a: load(a) for a in FULL5 + [R4]}
    bases5 = sorted(set.intersection(*[set(data[a]) for a in FULL5]))
    assert len(bases5) == 11, "expected 11 shared bases, got %d" % len(bases5)
    out = {"bases5": bases5, "pairs": {}, "appendix_r4": {}}
    for i in range(len(FULL5)):
        for j in range(i + 1, len(FULL5)):
            a, c = FULL5[i], FULL5[j]
            out["pairs"]["%s vs %s" % (a, c)] = pair_stats(data[a], data[c], bases5)
    shared10 = sorted(set(data[R4]) & set(bases5))
    for a in FULL5:
        out["appendix_r4"]["%s vs %s(10-base)" % (a, R4)] = pair_stats(data[a], data[R4], shared10)
    json.dump(out, open(os.path.join(REP, "T1_PAIRWISE.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    L = ["# T1 Pairwise Agreement (deterministic, zero API)", "",
         "5 complete arms x 11 shared bases. Consensus != correctness.",
         "", "| pair | bases | P | R | F1 | mean shared rels |",
         "|---|---|---|---|---|---|"]
    for k, v in out["pairs"].items():
        L.append("| %s | %d | %.4f | %.4f | %.4f | %.2f |" % (
            k, v["n_bases"], v["P"], v["R"], v["F1"], v["mean_shared_rels"]))
    L += ["", "## Appendix: r4 (10-base intersection, wahrscheinlichkeit missing)", "",
          "| pair | bases | P | R | F1 | mean shared rels |",
          "|---|---|---|---|---|---|"]
    for k, v in out["appendix_r4"].items():
        L.append("| %s | %d | %.4f | %.4f | %.4f | %.2f |" % (
            k, v["n_bases"], v["P"], v["R"], v["F1"], v["mean_shared_rels"]))
    open(os.path.join(REP, "T1_PAIRWISE.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    for k, v in out["pairs"].items():
        print("%s F1=%.4f" % (k, v["F1"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

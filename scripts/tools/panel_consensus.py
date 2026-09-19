#!/usr/bin/env python3
"""Panel consensus + agreement appendix (deterministic, zero API).

Inputs: research/gold_review_v2/panel_<rater>.json (R1..R5, partials allowed).
Outputs: research/gold_review_v2/panel_CONSENSUS.json (review_72 filled schema,
  feed to gold_blind_audit.py --import) + panel_CONSENSUS.md (Fleiss k,
  pairwise Jaccard, exact-match rate).
Rules (A-judge J5): majority >=3/5 per item (of DECIDED raters if partial);
  ties -> edit + needs_human (never silent accept); reject majority -> empty.
"""
import itertools
import json
import math
import os
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(BASE, "research", "gold_review_v2")
RATERS = ["R1", "R2", "R3", "R4", "R5"]


def norm(s):
    return "".join(str(s).lower().split())


def load(rater):
    p = os.path.join(OUT, "panel_%s.json" % rater)
    if not os.path.exists(p):
        return {}
    d = json.load(open(p, encoding="utf-8"))
    return {r["audit_id"]: r for r in d.get("records", []) if r.get("decision")}


def fleiss(table):
    # table: items x categories counts; 5.0 fixed raters -> use decided count per item
    # REAUDIT 2026-09-19 known limitations (frozen; D-V11 context): Pe denominator uses
    # decided-vote total, not n_items*n (biased under partial R4); norm() here is weaker
    # than T1 norm (no ß/-/_ handling — Jaccard not comparable across scorers);
    # empty-vs-empty concept sets count as exact/Jaccard (inflates); second return value
    # is mean observed agreement, mislabeled "mean_pairwise_agreement" downstream.
    n_items = len(table)
    k = 3
    P_bar, Pe_num = 0.0, [0.0] * k
    tot = 0
    for row in table:
        n = sum(row)
        tot += n
        P_bar += (sum(c * (c - 1) for c in row) / (n * (n - 1))) if n > 1 else 0.0
        for j in range(k):
            Pe_num[j] += row[j]
    P_bar /= n_items
    Pe = sum((x / tot) ** 2 for x in Pe_num)
    return round((P_bar - Pe) / max(1 - Pe, 1e-9), 4), round(P_bar, 4)


def main():
    judged = {r: load(r) for r in RATERS}
    aids = sorted(set().union(*[set(v) for v in judged.values()]))
    cats = ["accept", "edit", "reject"]
    table, consensus, exact = [], [], 0
    for aid in aids:
        votes = [(r, judged[r][aid]["decision"]) for r in RATERS if aid in judged[r]]
        row = [sum(1 for _, d in votes if d == c) for c in cats]
        table.append(row)
        n_dec = len(votes)
        top = max(row)
        winners = [c for c, v in zip(cats, row) if v == top]
        sets = []
        for r, d in votes:
            s = set(norm(c) for c in judged[r][aid].get("edited_concepts", []) if norm(c))
            sets.append(s)
        if len(sets) > 1 and all(s == sets[0] for s in sets):
            exact += 1
        if len(winners) == 1 and top >= 3 and (n_dec == 5 or top > n_dec / 2):
            dec = winners[0]
            need = False
        else:
            dec = "edit"
            need = True
        if dec == "reject":
            voted = []
        else:
            cnt = Counter()
            for s in sets:
                for c in s:
                    cnt[c] += 1
            thresh = 3 if n_dec == 5 else (n_dec // 2 + 1)
            voted = sorted([c for c, v in cnt.items() if v >= thresh])
        sample = next(judged[r][aid].get("sample_id", "") for r in RATERS if aid in judged[r])
        consensus.append({"audit_id": aid, "sample_id": sample, "reviewer": "consensus",
                          "decision": dec, "edited_concepts": voted,
                          "needs_human": need, "n_raters": n_dec,
                          "votes": {c: v for c, v in zip(cats, row)}})
    kappa, pbar = fleiss(table)
    # pairwise Jaccard on edited sets
    pairs = []
    for a, b in itertools.combinations(RATERS, 2):
        common = [i for i in aids if i in judged[a] and i in judged[b]]
        js = []
        for i in common:
            sa = set(norm(c) for c in judged[a][i].get("edited_concepts", []))
            sb = set(norm(c) for c in judged[b][i].get("edited_concepts", []))
            if not sa and not sb:
                da = judged[a][i]["decision"] == "reject"
                db = judged[b][i]["decision"] == "reject"
                js.append(1.0 if da and db else 0.0)
            else:
                js.append(len(sa & sb) / max(len(sa | sb), 1))
        pairs.append((a, b, len(common), round(sum(js) / max(len(js), 1), 4)))
    json.dump({"meta": {"annotator": "5-model-agent-panel (non-human; falsify/screen only, never matures C9b)",
                        "raters": RATERS, "fleiss_kappa_decision": kappa,
                        "mean_pairwise_agreement": pbar},
               "records": consensus},
              open(os.path.join(OUT, "panel_CONSENSUS.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    L = ["# Panel Consensus (deterministic — falsify/screen only)", "",
         "Items: %d. Fleiss κ (decision) = %.4f. Exact-5-agreement: %d/%d." % (
             len(aids), kappa, exact, len(aids)),
         "", "## Pairwise Jaccard (edited sets)", "",
         "| pair | common | mean Jaccard |", "|---|---|---|"]
    for a, b, n, j in pairs:
        L.append("| %s-%s | %d | %.4f |" % (a, b, n, j))
    rej = [c["audit_id"] for c in consensus if c["decision"] == "reject"]
    nh = [c["audit_id"] for c in consensus if c["needs_human"]]
    L += ["", "Consensus rejects (%d): %s" % (len(rej), ", ".join(rej)),
          "", "needs_human (%d): %s" % (len(nh), ", ".join(nh))]
    open(os.path.join(OUT, "panel_CONSENSUS.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("items=%d kappa=%.4f exact=%d/%d rejects=%d needs_human=%d" % (
        len(aids), kappa, exact, len(aids), len(rej), len(nh)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Phase-2: E3 238-edge weighted-subsample repeats (N=200) + threshold对照.

Reuses weight_graph_E3 internals (import; main() NOT called).
For each k in (5,10,15), per lang: rebuild candidate pools once, then
200 seeds (BASE 30260916+i): weighted choice 238 edges -> J_edge-only per
pair -> record order + rho vs LDS-K order.
Also: threshold-method对照 (top-238 by similarity, deterministic) and
density note. Output: research/weight_e3_repeats_20260916.json (+ stdout).
Read-only contract: writes ONLY that file. Exploratory appendix-only.
Usage: python scripts/tools/weight_e3_repeats.py [--n 200] [--help]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weight_graph_E3 as E3

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "research", "weight_e3_repeats_20260916.json")
N_DEFAULT = 200
REPEAT_BASE = 30260916


def build_pools():
    import numpy as np
    groups = json.loads(E3.ALIGNED_PATH.read_text(encoding="utf-8"))["aligned_groups"]
    vec_map = json.loads(E3.VECTORS_PATH.read_text(encoding="utf-8"))
    rows = [(i, g.get("id", "?"), {l: ((g.get("labels", {}) or {}).get(l) or "").strip()
                                   for l in E3.LANGS}) for i, g in enumerate(groups)]
    first = {}
    for (i, gid, labs) in rows:
        if gid in first:
            first[gid]["repeat_rows"].append(i)
        else:
            first[gid] = {"first_row": i, "labels": labs, "repeat_rows": []}
    uniq = [gid for (i, gid, _) in rows if first[gid]["first_row"] == i]
    flab = {gid: first[gid]["labels"] for gid in uniq}
    gwv = {l: [gid for gid in uniq if flab[gid][l] in vec_map] for l in E3.LANGS}
    pools = {}
    for k in E3.KS:
        pools[k] = {}
        for lang in E3.LANGS:
            gids = gwv[lang]
            mat = np.array([vec_map[flab[g][lang]] for g in gids], dtype=np.float64)
            cands, sim_lookup, loops = E3.knn_candidates_numpy(gids, mat, k)
            assert loops == 0
            w = np.array([max(0.0, (sim_lookup[(a, b)] + 1.0) / 2.0) for (a, b, _) in cands])
            pools[k][lang] = (cands, w)
    return pools, gwv


def j_of(picked, gwv, la, lb):
    ea = set(picked[la])
    eb = set(picked[lb])
    return E3.lds_jaccard(gwv[la], gwv[lb], ea, eb)["lds_score"]


def main():
    import numpy as np
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: weight_e3_repeats.py [--n 200]")
        return 0
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else N_DEFAULT
    pools, gwv = build_pools()
    out = {"n_repeats": n, "repeat_base": REPEAT_BASE, "per_k": {},
           "status": "EXECUTED (measurement); interpretation Hypothesis/PENDING"}
    for k in E3.KS:
        rhos, orders = [], {}
        for i in range(n):
            picked = {}
            for lang in E3.LANGS:
                cands, w = pools[k][lang]
                rng = np.random.default_rng(REPEAT_BASE + i)
                idx = rng.choice(len(cands), size=E3.N_MATCHED, replace=False, p=w / w.sum())
                picked[lang] = [tuple(cands[j][:2]) for j in idx]
            scores = {f"{la}-{lb}": j_of(picked, gwv, la, lb) for (la, lb) in E3.PAIRS}
            asc, _ = E3.ranks_from_scores(scores)
            rho, _ = E3.spearman_with_ties(scores, dict(E3.LDS_K_FROZEN))
            rhos.append(rho)
            asc = tuple(asc)
            orders[asc] = orders.get(asc, 0) + 1
        rhos = np.array(rhos)
        # threshold对照: top-238 by weight, deterministic
        tp = {}
        for lang in E3.LANGS:
            cands, w = pools[k][lang]
            top = np.argsort(-w)[:E3.N_MATCHED]
            tp[lang] = [tuple(cands[j][:2]) for j in top]
        tscores = {f"{la}-{lb}": j_of(tp, gwv, la, lb) for (la, lb) in E3.PAIRS}
        tasc, _ = E3.ranks_from_scores(tscores)
        trho, _ = E3.spearman_with_ties(tscores, dict(E3.LDS_K_FROZEN))
        out["per_k"][f"k={k}"] = {
            "rho_mean": round(float(rhos.mean()), 4), "rho_std": round(float(rhos.std()), 4),
            "rho_min": round(float(rhos.min()), 4), "rho_max": round(float(rhos.max()), 4),
            "order_histogram": {"|".join(k2): v for k2, v in orders.items()},
            "threshold_contrast": {"asc": list(tasc), "rho": trho, "values": tscores},
        }
        print("k=%d rho %.4f+-%.4f range [%.4f,%.4f] orders %s" % (
            k, rhos.mean(), rhos.std(), rhos.min(), rhos.max(), orders))
    from pathlib import Path
    E3.guard_output(Path(OUT))
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("WROTE", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())

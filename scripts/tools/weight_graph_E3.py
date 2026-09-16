#!/usr/bin/env python3
"""Phase-1 E3: sparsity-matched (238-edge) gid kNN rerun (read-only).

READ-ONLY CONTRACT (violations abort):
  - NEVER writes to tests/, freeze/, _deploy/, data/, linguaGraph.db.
  - NEVER adds concepts, NEVER expands corpus, NEVER changes LDS v3 formula
    (lds_jaccard below is a verbatim reuse of docs/lds_formal_definition.md
    section 8.1, identical to scripts/tools/weight_graph_audit.py and E1b).
  - Does NOT modify scripts/tools/weight_graph_audit.py,
    scripts/tools/weight_graph_E1b.py, nor their outputs.
  - All new statistics are exploratory appendix-only.
  - Inputs (read-only): research/weight_vectors_934x768_20260916.term2vec.json
    (934x768) + data/math_extractions/merged/aligned_data.json (219 rows)
    + manifest.json human baseline (556 nodes / 238 edges / 0.001543).
  - Inherits E1b translation layer term->gid FIRST-ROW rule and ALL its bias
    declarations (MNAR 2/201, 18 first-row picks = selection bias, 2 named
    variants, J_node=1.0 by construction, J_edge still contaminated).
  - ONLY write target: research/weight_graph_E3_20260916.json (+ stdout).

E3 method (sparsity matching):
  1. Build gid-kNN candidate pools per language for k=5/10/15 exactly as E1b
     (symmetrized kNN, cosine distance, stable argsort ties by file order).
  2. Persist FULL candidate edge weight table: per candidate undirected gid
     pair, cosine distance d = 1 - sim, similarity sim, sampling weight
     w = (sim + 1) / 2 in [0, 1] (monotone in closeness, always >= 0).
  3. Subsample 238 undirected edges per language per k-pool with method
     "weight": weighted random sampling WITHOUT replacement, inclusion
     probability p(e) = w(e) / sum(w), numpy Generator with FIXED base seed
     20260916, per-(k,lang) derived seed = base + k*100 + lang_index
     (lang_index: zh=0, en=1, de=2). Deterministic given seed. Recorded.
  4. Recompute J_edge-only(gid,238matched) = (1 - J_edge)/2 under J_node=1.0
     (degenerate LDS v3, range [0,0.5] asymmetric, suspect metric inherited
     from E1b) per k-pool x per pair. Rank vs frozen LDS-K is order-only,
     n=3 no power, EN-gap order ban, zh-de n=65 down-weighted, numeric
     cross-validation banned both directions.

Usage (stdlib + numpy):
  python scripts/tools/weight_graph_E3.py
"""

import itertools
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ALIGNED_PATH = ROOT / "data" / "math_extractions" / "merged" / "aligned_data.json"
VECTORS_PATH = ROOT / "research" / "weight_vectors_934x768_20260916.term2vec.json"
OUT_PATH = ROOT / "research" / "weight_graph_E3_20260916.json"

LDS_K_FROZEN = {"zh-de": 0.519, "zh-en": 0.934, "de-en": 0.938}
KS = (5, 10, 15)
LANGS = ("zh", "en", "de")
LANG_IDX = {"zh": 0, "en": 1, "de": 2}
PAIRS = (("zh", "de"), ("zh", "en"), ("de", "en"))
BASE_SEED = 20260916
N_MATCHED = 238
SAMPLING_METHOD = "weight"  # weight | threshold (this run: weight, recorded)

FORBIDDEN_WRITE_PREFIXES = ("tests", "freeze", "_deploy", "data", "linguaGraph.db")


def guard_output(path: Path) -> None:
    rel = path.resolve().relative_to(ROOT.resolve()).as_posix()
    for prefix in FORBIDDEN_WRITE_PREFIXES:
        if rel == prefix or rel.startswith(prefix + "/"):
            raise SystemExit(f"[ABORT] write target inside forbidden zone: {rel}")
    if not rel.startswith("research/"):
        raise SystemExit(f"[ABORT] write target must be inside research/: {rel}")


def lds_jaccard(nodes_a, nodes_b, edges_a, edges_b):
    """Verbatim reuse of docs/lds_formal_definition.md sect 8.1 (NOT modified)."""
    set_a, set_b = set(nodes_a), set(nodes_b)
    node_jac = len(set_a & set_b) / max(len(set_a | set_b), 1)
    ea, eb = set(edges_a), set(edges_b)
    edge_jac = len(ea & eb) / max(len(ea | eb), 1)
    lds = 1.0 - (node_jac + edge_jac) / 2
    return {"lds_score": round(lds, 4), "jaccard_node": round(node_jac, 4),
            "jaccard_edge": round(edge_jac, 4)}


def knn_candidates_numpy(keys, mat, k):
    """Symmetrized kNN candidate pool over ordered UNIQUE keys.

    Cosine distance, stable argsort (ties keep file order, same rule as E1/E1b).
    Returns list of (a, b, dist) sorted by (dist, a, b) for stable ledger order,
    plus self-loop count removed (0 by construction over unique keys).
    """
    import numpy as np

    n = len(keys)
    assert len(set(keys)) == n, "knn keys must be unique"
    norms = np.linalg.norm(mat, axis=1)
    zero = norms == 0
    safe = np.where(zero, 1.0, norms)
    nmat = mat / safe[:, None]
    sim = nmat @ nmat.T
    np.clip(sim, -1.0, 1.0, out=sim)
    dist = 1.0 - sim
    if zero.any():
        dist[zero, :] = 1.0
        dist[:, zero] = 1.0
    np.fill_diagonal(dist, np.inf)
    kk = min(k, n - 1)
    order = np.argsort(dist, axis=1, kind="stable")[:, :kk]
    edge_dist = {}
    for i in range(n):
        for j in order[i]:
            j = int(j)
            a, b = keys[i], keys[j]
            key = (a, b) if a <= b else (b, a)
            d = float(dist[i, j])
            if key not in edge_dist or d < edge_dist[key]:
                edge_dist[key] = d
    loops = sum(1 for (a, b) in edge_dist if a == b)
    cands = [(a, b, d) for (a, b), d in edge_dist.items() if a != b]
    cands.sort(key=lambda t: (t[2], t[0], t[1]))
    # full symmetric similarity lookup for weight table
    sim_lookup = {}
    for (a, b, d) in cands:
        ia, ib = keys.index(a), keys.index(b)
        sim_lookup[(a, b)] = float(sim[ia, ib])
    return cands, sim_lookup, int(loops)


def ranks_from_scores(scores):
    items = sorted(scores.keys())
    sval = sorted(set(scores.values()))
    rank_of_val = {}
    r = 1
    for v in sval:
        cnt = sum(1 for x in items if scores[x] == v)
        rank_of_val[v] = sum(range(r, r + cnt)) / cnt
        r += cnt
    asc_order = sorted(items, key=lambda x: (scores[x], x))
    return asc_order, [rank_of_val[scores[x]] for x in items]


def spearman_with_ties(scores_a, scores_b):
    assert set(scores_a) == set(scores_b) and len(scores_a) == 3
    items = sorted(scores_a.keys())
    _, ra = ranks_from_scores(scores_a)
    _, rb = ranks_from_scores(scores_b)

    def rho_xy(x, y):
        n = len(x)
        mx, my = sum(x) / n, sum(y) / n
        cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
        vx = sum((a - mx) ** 2 for a in x)
        vy = sum((b - my) ** 2 for b in y)
        if vx == 0 or vy == 0:
            return 0.0
        return cov / (vx ** 0.5 * vy ** 0.5)

    obs = rho_xy(ra, rb)
    ge = sum(1 for perm in itertools.permutations(rb)
             if abs(rho_xy(ra, list(perm))) >= abs(obs) - 1e-12)
    return round(obs, 4), ge / 6.0


def main():
    import numpy as np

    guard_output(OUT_PATH)
    exploratory = True

    groups = json.loads(ALIGNED_PATH.read_text(encoding="utf-8"))["aligned_groups"]
    vec_map = json.loads(VECTORS_PATH.read_text(encoding="utf-8"))
    dim = len(vec_map[next(iter(vec_map))])
    assert len(vec_map) == 934 and dim == 768

    # ---------- row layer + R-gid first-row collapse (E1b rule, inherited) ----------
    rows = []
    for i, g in enumerate(groups):
        labels = g.get("labels", {}) or {}
        rows.append((i, g.get("id", "?"),
                     {l: (labels.get(l) or "").strip() for l in LANGS}))
    n_rows = len(rows)
    first_row_of_gid = {}
    for (i, gid, labs) in rows:
        if gid in first_row_of_gid:
            first_row_of_gid[gid]["repeat_rows"].append(i)
        else:
            first_row_of_gid[gid] = {"first_row": i, "labels": labs,
                                     "repeat_rows": []}
    uniq_gids = [gid for (i, gid, _) in rows
                 if first_row_of_gid[gid]["first_row"] == i]
    first_labels = {gid: first_row_of_gid[gid]["labels"] for gid in uniq_gids}
    gids_with_vec = {l: [gid for gid in uniq_gids
                         if first_labels[gid][l] in vec_map] for l in LANGS}
    gid_sets = {l: set(gids_with_vec[l]) for l in LANGS}
    sets_identical = (gid_sets["zh"] == gid_sets["en"] == gid_sets["de"])
    missing_gids = [gid for gid in uniq_gids
                    if not all(first_labels[gid][l] in vec_map for l in LANGS)]
    n_collisions = sum(1 for gid in uniq_gids
                       if first_row_of_gid[gid]["repeat_rows"])

    # ---------- candidate pools + full weight tables ----------
    cand_tables = {}   # k -> lang -> list of {edge, dist, sim, weight}
    cand_edges = {}    # k -> lang -> set of (a,b)
    cand_summary = {}
    gid_mats = {}
    for lang in LANGS:
        gids = gids_with_vec[lang]
        gid_mats[lang] = (gids, np.array(
            [vec_map[first_labels[gid][lang]] for gid in gids],
            dtype=np.float64))
    for k in KS:
        cand_tables[f"k={k}"] = {}
        cand_edges[f"k={k}"] = {}
        cand_summary[f"k={k}"] = {}
        for lang in LANGS:
            gids, mat = gid_mats[lang]
            cands, sim_lookup, loops = knn_candidates_numpy(gids, mat, k)
            assert loops == 0
            table = []
            for (a, b, d) in cands:
                s = sim_lookup[(a, b)]
                w = (s + 1.0) / 2.0
                if w < 0:
                    w = 0.0
                table.append({"edge": [a, b], "cosine_distance": round(d, 6),
                              "cosine_similarity": round(s, 6),
                              "weight": round(w, 6)})
            cand_tables[f"k={k}"][lang] = table
            cand_edges[f"k={k}"][lang] = {(a, b) for (a, b, _) in cands}
            ws = np.array([r["weight"] for r in table], dtype=np.float64)
            ds = np.array([r["cosine_distance"] for r in table])
            cand_summary[f"k={k}"][lang] = {
                "nodes": len(gids), "n_candidates": len(table),
                "self_loops_removed": loops,
                "weight_min": round(float(ws.min()), 6),
                "weight_mean": round(float(ws.mean()), 6),
                "weight_max": round(float(ws.max()), 6),
                "dist_min": round(float(ds.min()), 6),
                "dist_mean": round(float(ds.mean()), 6),
                "dist_max": round(float(ds.max()), 6),
            }

    # ---------- weighted subsample to 238 edges per lang per k ----------
    matched = {}   # k -> lang -> list of [a,b]
    matched_info = {}
    for k in KS:
        matched[f"k={k}"] = {}
        matched_info[f"k={k}"] = {}
        for lang in LANGS:
            table = cand_tables[f"k={k}"][lang]
            n_pool = len(table)
            assert n_pool >= N_MATCHED, f"pool {n_pool} < 238 for k={k} {lang}"
            seed = BASE_SEED + k * 100 + LANG_IDX[lang]
            rng = np.random.default_rng(seed)
            w = np.array([r["weight"] for r in table], dtype=np.float64)
            wsum = w.sum()
            assert wsum > 0
            p = w / wsum
            idx = rng.choice(n_pool, size=N_MATCHED, replace=False, p=p)
            picked = sorted([tuple(table[i]["edge"]) for i in idx])
            matched[f"k={k}"][lang] = [list(e) for e in picked]
            pw = w[idx]
            matched_info[f"k={k}"][lang] = {
                "seed": seed, "method": SAMPLING_METHOD,
                "pool": n_pool, "picked": N_MATCHED,
                "picked_weight_min": round(float(pw.min()), 6),
                "picked_weight_mean": round(float(pw.mean()), 6),
                "picked_weight_max": round(float(pw.max()), 6),
            }

    # ---------- J_edge-only(gid,238matched) ----------
    results = {}
    for k in KS:
        results[f"k={k}"] = {}
        for (la, lb) in PAIRS:
            ea = {tuple(e) for e in matched[f"k={k}"][la]}
            eb = {tuple(e) for e in matched[f"k={k}"][lb]}
            r = lds_jaccard(gids_with_vec[la], gids_with_vec[lb], ea, eb)
            inter = len(ea & eb)
            union = len(ea | eb)
            r["n_edges_a"] = len(ea)
            r["n_edges_b"] = len(eb)
            r["n_intersection"] = inter
            r["n_union"] = union
            results[f"k={k}"][f"{la}-{lb}"] = r

    # ---------- rank vs LDS-K (order-only) ----------
    rank_block = {
        "method": ("Spearman rho over n=3 language pairs with midrank "
                   "ties; descriptive only; exact two-sided permutation p; "
                   "human pilot N=8: no significance claims anywhere"),
        "LDS_K_frozen_asc": ["zh-de", "zh-en", "de-en"],
        "LDS_K_values_for_order_only": LDS_K_FROZEN,
        "ban": ("order-structure only; forbidden: any numeric comparison of "
                "J_edge-only(gid,238matched) vs LDS-K values (cross-dimension "
                "unit ban, both directions); forbidden: significance language "
                "at n=3 and at human N=8; forbidden: EN order-gap claims on "
                "near-ties (T-P5-3 analog); forbidden: directional narratives"),
    }
    for k in KS:
        scores = {p: results[f"k={k}"][p]["lds_score"]
                  for p in ("zh-de", "zh-en", "de-en")}
        asc, _ = ranks_from_scores(scores)
        ref = dict(LDS_K_FROZEN)
        rho, p = spearman_with_ties(scores, ref)
        rank_block[f"k={k}"] = {
            "J_edge_only_gid238_asc": asc,
            "J_edge_only_gid238_values": scores,
            "rho": rho, "exact_two_sided_p": round(p, 4),
            "p_note": "n.s.: n=3 has no power (descriptive only)",
            "tie_note": "no ties at 4dp" if len(set(scores.values())) == 3
                        else "ties present: no order claim between tied pairs",
        }

    # ---------- k-sensitivity ----------
    sens = {}
    for p in ("zh-de", "zh-en", "de-en"):
        vals = [results[f"k={k}"][p]["lds_score"] for k in KS]
        sens[p] = {"k=5": vals[0], "k=10": vals[1], "k=15": vals[2],
                   "range": round(max(vals) - min(vals), 4)}
    orders = [tuple(rank_block[f"k={k}"]["J_edge_only_gid238_asc"]) for k in KS]
    sens["order_stable_across_k"] = (orders[0] == orders[1] == orders[2])
    sens["orders"] = {f"k={k}": list(o) for k, o in zip(KS, orders)}
    sens["verdict"] = ("descriptive only; k-sensitivity logged, no causal or "
                       "source-attribution claims; pending independent review")

    # ---------- sparsity (edge-matched, node/density still mismatched) ----------
    import math
    n = len(gids_with_vec["zh"])
    matched_density = round(2 * N_MATCHED / (n * (n - 1)), 6)
    sparsity = {
        "human_baseline": {"nodes": 556, "edges": 238, "density": 0.001543,
                           "avg_degree": 0.8561},
        "matched_per_lang": {
            f"k={k}": {lang: {"nodes": n, "edges": N_MATCHED,
                              "density": matched_density,
                              "avg_degree": round(2 * N_MATCHED / n, 4)}
                       for lang in LANGS} for k in KS},
        "candidate_pools": cand_summary,
        "verdict": ("edge count matched (238/lang) but node count (199 vs "
                    "556) and density (0.0121 vs 0.001543, ~7.8x) still "
                    "mismatched; cross-density Jaccard remains confounded; "
                    "interpretation stays Hypothesis/PENDING"),
    }

    gate = {
        "E3_measurement": "EXECUTED",
        "R5_node_caliber": ("Hypothesis/PENDING (inherited E1b 199/201 biased "
                            "caliber: MNAR 2/201 + 18 first-row picks = "
                            "selection bias, no last-row rerun; E3 adds no "
                            "new caliber fix)"),
        "E3_interpretation": ("Hypothesis/PENDING (capped): n=3 rank has no "
                              "power (exact p n.s., order uninterpretable); "
                              "EN near-tie order-gap claims banned; zh-de "
                              "n=65 down-weighted, never sole carrier; N=8: "
                              "no significance claims; sparsity edge-matched "
                              "only, density still mismatched"),
        "promote_to_Developing": False,
        "promote_reason": ("Developing requires independent review of E3 "
                           "sparse-matched rerun plus k-sensitivity "
                           "adjudication; single weighted-subsample run with "
                           "suspect J_edge-only metric cannot promote."),
    }

    out = {
        "lane": "Lane-3 weight-vs-human E3 sparsity-matched rerun",
        "date": "2026-09-16",
        "status": "EXECUTED (measurement); caliber Hypothesis/PENDING; interpretation Hypothesis/PENDING",
        "exploratory_appendix_only": exploratory,
        "read_only_contract": {
            "writes": [OUT_PATH.resolve().relative_to(ROOT.resolve()).as_posix(),
                       "scripts/tools/weight_graph_E3.py",
                       "research/weight_vs_human_E3_20260916.md"],
            "untouched": ["tests/", "freeze/", "_deploy/", "data/",
                          "linguaGraph.db",
                          "scripts/tools/weight_graph_audit.py",
                          "research/weight_graph_audit_20260916.json",
                          "scripts/tools/weight_graph_E1b.py",
                          "research/weight_graph_E1b_20260916.json"],
            "new_concepts": 0,
            "corpus_expanded": False,
            "lds_v3_formula_changed": False,
        },
        "inputs": {
            "aligned_rows": n_rows,
            "unique_gids": len(uniq_gids),
            "id_collisions": n_collisions,
            "vectors_file": "research/weight_vectors_934x768_20260916.term2vec.json",
            "n_terms": len(vec_map), "dim": dim,
            "model": "text-embedding-nomic-embed-text-v1.5",
            "model_revision": "not exposed by LM Studio /v1/models (as in E1)",
            "lds_k_frozen": LDS_K_FROZEN,
            "input_hash": "none: aligned_data.json and term2vec json have no SHA256 on disk; byte consistency unverified (inherited A7)",
            "human_baseline": {"nodes": 556, "edges": 238, "density": 0.001543},
        },
        "translation_layer_inherited_E1b": {
            "R_intra": "three labels of one aligned group share ONE node (gid)",
            "R_gid": ("rows sharing one gid collapse to the FIRST row in "
                      "aligned-file order; all 18 collisions kept as first-row "
                      "picks = selection bias (2 single-label variants: "
                      "math_calculus_LHopital de-slot, math_calculus_divergence "
                      "en-slot); no last-row rerun, no lossless/clean wording"),
            "R_cross": ("same surface label across DISTINCT gids maps to the "
                        "FIRST gid in file order, per language; nodes NOT "
                        "merged (merge would re-contaminate J_node)"),
            "R_loop": "self-loops removed and counted (0 by construction)",
            "missing_mechanism": "MNAR (non-random: 2 groups with fully surface-identical CJK labels systematically absent from 934 term matrix)",
            "missing_rate_gid": f"{len(missing_gids)}/{len(uniq_gids)}",
            "missing_gids": missing_gids,
            "node_gids_per_lang": {l: len(gids_with_vec[l]) for l in LANGS},
            "gid_sets_identical_across_langs": sets_identical,
            "j_node_by_construction": 1.0 if sets_identical else "see results",
            "decontamination": ("J_node decontaminated by construction "
                                "(identical 199-gid sets); J_edge still "
                                "contaminated: (1) de-slot CJK residue; "
                                "(2) twin-pair mechanism; no stripping/clean claims"),
            "caliber": ("199/201 biased caliber inherited from E1b; E3 adds no "
                        "new caliber fix"),
        },
        "sampling": {
            "method": SAMPLING_METHOD,
            "method_note": ("weight: weighted random sampling WITHOUT "
                            "replacement, p(e)=w(e)/sum(w), w=(cos_sim+1)/2; "
                            "threshold (top-238 by distance) NOT used in this run"),
            "base_seed": BASE_SEED,
            "seed_rule": "seed(k,lang) = 20260916 + k*100 + lang_index (zh=0,en=1,de=2)",
            "seeds": {f"k={k}": {lang: BASE_SEED + k * 100 + LANG_IDX[lang]
                                 for lang in LANGS} for k in KS},
            "n_matched_per_lang": N_MATCHED,
            "rng": "numpy.random.default_rng(seed)",
        },
        "candidate_weight_tables": cand_tables,
        "candidate_summary": cand_summary,
        "matched_edges_238": matched,
        "matched_info": matched_info,
        "results_J_edge_only_gid238": results,
        "rank_corr_vs_LDS_K_order_only": rank_block,
        "k_sensitivity": sens,
        "sparsity": sparsity,
        "metric_name": "J_edge-only(gid,238matched)",
        "metric_formula": "J_edge-only=(1-J_edge)/2 (degenerate LDS v3 under J_node=1.0 by construction)",
        "metric_range": "[0,0.5] asymmetric; cross-dimension comparison with LDS-K forbidden both directions",
        "metric_suspect": "new unvalidated suspect metric inherited from E1b; rank comparison is method note only",
        "zh_de_rule": ("zh-de primary n=65 (thinnest) down-weighted; never "
                       "sole carrier; reported only side-by-side with "
                       "zh-en/de-en"),
        "en_cap": ("EN-involved claims stay distribution-level; no "
                   "per-concept validation sentences"),
        "gate_self_eval": gate,
    }
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "J_edge_only_gid238": {k: {p: results[k][p]["lds_score"]
                                   for p in ("zh-de", "zh-en", "de-en")}
                               for k in results},
        "rank": {f"k={k}": rank_block[f"k={k}"] for k in KS},
        "seeds": out["sampling"]["seeds"],
        "k_sensitivity": sens,
        "out": str(OUT_PATH),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

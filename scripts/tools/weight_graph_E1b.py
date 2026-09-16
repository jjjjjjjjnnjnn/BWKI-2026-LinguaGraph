#!/usr/bin/env python3
"""Phase-1 E1b: kNN LDS-VEC rerun with group-id node identity (read-only).

READ-ONLY CONTRACT (violations abort):
  - NEVER writes to tests/, freeze/, _deploy/, data/, linguaGraph.db.
  - NEVER adds concepts, NEVER expands corpus, NEVER changes LDS v3 formula
    (lds_jaccard below is a verbatim reuse of docs/lds_formal_definition.md
    section 8.1, identical to scripts/tools/weight_graph_audit.py).
  - Does NOT modify scripts/tools/weight_graph_audit.py nor its output
    research/weight_graph_audit_20260916.json.
  - All new statistics are exploratory appendix-only.
  - Inputs (read-only): research/weight_vectors_934x768_20260916.term2vec.json
    (934x768) + data/math_extractions/merged/aligned_data.json (219 rows).
  - ONLY write target: research/weight_graph_E1b_20260916.json (+ stdout).

E1b translation layer (term -> gid):
  R-intra: the three language labels of one aligned group share ONE node (gid).
  R-gid:   aligned rows sharing one gid collapse to the FIRST row in file
    order (18 id-collisions recorded; 16 lossless, 2 label-variants).
  R-cross: a surface label repeating across DISTINCT gids maps to the FIRST
    gid in file order (per language); every collision is recorded. Nodes stay
    one-gid-per-group (no merge): collapsing them would make node survival
    depend on surface equality again and re-contaminate J_node.
  R-loop:  self-loops (gid == gid) are removed and counted (0 by construction
    over unique gid keys; the E1 string-space baseline self-loops that this
    removes are recounted row-based for audit).

Usage (stdlib + numpy):
  python scripts/tools/weight_graph_E1b.py
"""

import itertools
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ALIGNED_PATH = ROOT / "data" / "math_extractions" / "merged" / "aligned_data.json"
VECTORS_PATH = ROOT / "research" / "weight_vectors_934x768_20260916.term2vec.json"
OUT_PATH = ROOT / "research" / "weight_graph_E1b_20260916.json"

# Frozen references (read-only copies, never recomputed here).
LDS_K_FROZEN = {"zh-de": 0.519, "zh-en": 0.934, "de-en": 0.938}
# E1 string-space LDS-VEC from research/weight_graph_audit_20260916.json
# (E1_EXECUTED.lds_vec), used ONLY to validate the numpy kNN reproduction.
E1_STRING_FROZEN = {
    "k=5": {"zh-de": 0.5245, "zh-en": 0.9392, "de-en": 0.9416},
    "k=10": {"zh-de": 0.5309, "zh-en": 0.9428, "de-en": 0.9446},
    "k=15": {"zh-de": 0.5457, "zh-en": 0.9476, "de-en": 0.9477},
}
KS = (5, 10, 15)
LANGS = ("zh", "en", "de")
PAIRS = (("zh", "de"), ("zh", "en"), ("de", "en"))

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


def knn_edges_numpy(keys, mat, k):
    """Symmetrized kNN edges over ordered UNIQUE `keys` with row matrix `mat`.

    Cosine distance, stable argsort (ties keep file order, mirroring the
    pure-python stable sort of scripts/tools/weight_graph_audit.py).
    Zero-norm rows get distance 1.0 to everything (same rule as cos_dist).
    Returns (edges:set, self_loops_removed:int).
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
    if zero.any():  # replicate cos_dist zero rule
        dist[zero, :] = 1.0
        dist[:, zero] = 1.0
    np.fill_diagonal(dist, np.inf)  # exclude self (i == j)
    kk = min(k, n - 1)
    order = np.argsort(dist, axis=1, kind="stable")[:, :kk]
    edges = set()
    for i in range(n):
        for j in order[i]:
            a, b = keys[i], keys[int(j)]
            edges.add((a, b) if a <= b else (b, a))
    loops = sum(1 for (a, b) in edges if a == b)
    edges = {e for e in edges if e[0] != e[1]}
    return edges, int(loops)


def knn_edges_dup_keys(keys, mat, k):
    """Row-based kNN allowing DUPLICATE keys (E1 string-space replica).

    Mirrors scripts/tools/weight_graph_audit.py::knn_edges exactly, except
    cosine via numpy + stable argsort (ties keep row order = stable-sort
    order of the original). Self-loop (t,t) edges are counted, not removed.
    """
    import numpy as np

    n = len(keys)
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
    edges = set()
    for i in range(n):
        for j in order[i]:
            a, b = keys[i], keys[int(j)]
            edges.add((a, b) if a <= b else (b, a))
    loops = sum(1 for (a, b) in edges if a == b)
    return edges, int(loops)


def ranks_from_scores(scores):
    """scores: dict item -> float. Returns (asc_order, ranklist aligned to
    sorted(items)) with midranks for ties."""
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
    """Exact Spearman rho + two-sided permutation p for n=3 (midrank ties)."""
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

    # ---------- row layer (file order; rows may share gids) ----------
    rows = []  # (row_idx, gid, {lang: label})
    for i, g in enumerate(groups):
        labels = g.get("labels", {}) or {}
        rows.append((i, g.get("id", "?"),
                     {l: (labels.get(l) or "").strip() for l in LANGS}))
    n_rows = len(rows)

    # ---------- R-gid: collapse same-gid rows to first row ----------
    first_row_of_gid = {}
    id_collisions = []  # one record per repeated gid
    for (i, gid, labs) in rows:
        if gid in first_row_of_gid:
            first_row_of_gid[gid]["repeat_rows"].append(
                {"row": i, "labels": labs})
        else:
            first_row_of_gid[gid] = {"first_row": i, "labels": labs,
                                     "repeat_rows": []}
    for gid, rec in first_row_of_gid.items():
        if rec["repeat_rows"]:
            lossless = all(r["labels"] == rec["labels"]
                           for r in rec["repeat_rows"])
            id_collisions.append({
                "gid": gid, "first_row": rec["first_row"],
                "first_labels": rec["labels"],
                "n_rows": 1 + len(rec["repeat_rows"]),
                "repeat_rows": rec["repeat_rows"],
                "lossless_identical_labels": lossless,
            })
    id_collisions.sort(key=lambda r: r["first_row"])
    uniq_gids = [gid for (i, gid, _) in rows if
                 first_row_of_gid[gid]["first_row"] == i]
    first_labels = {gid: first_row_of_gid[gid]["labels"] for gid in uniq_gids}

    # ---------- vector coverage: rows and unique gids ----------
    rows_missing_all = [gid for (_, gid, labs) in rows
                        if not any(labs[l] in vec_map for l in LANGS)]
    rows_with_vec = {l: [(i, gid) for (i, gid, labs) in rows
                         if labs[l] in vec_map] for l in LANGS}
    gids_with_vec = {l: [gid for gid in uniq_gids
                         if first_labels[gid][l] in vec_map] for l in LANGS}
    gid_sets = {l: set(gids_with_vec[l]) for l in LANGS}
    sets_identical = (gid_sets["zh"] == gid_sets["en"] == gid_sets["de"])
    missing_gids = [gid for gid in uniq_gids
                    if not all(first_labels[gid][l] in vec_map for l in LANGS)]

    # ---------- R-cross: same label across DISTINCT gids -> first gid ----------
    dup_records = []
    term_first_gid = {}
    per_lang_dup = {}
    for lang in LANGS:
        term_gids = defaultdict(list)
        for gid in gids_with_vec[lang]:
            term_gids[first_labels[gid][lang]].append(gid)
        dups = {t: gs for t, gs in term_gids.items() if len(gs) > 1}
        for t, gs in sorted(dups.items()):
            term_first_gid[(lang, t)] = gs[0]
            dup_records.append({"lang": lang, "term": t, "first_gid": gs[0],
                                "duplicate_gids": gs[1:], "count": len(gs)})
        for t, gs in term_gids.items():
            term_first_gid.setdefault((lang, t), gs[0])
        per_lang_dup[lang] = {
            "n_unique_gids_with_vectors": len(gids_with_vec[lang]),
            "n_unique_terms": len(term_gids),
            "dup_keys": len(dups),
            "extra_copies": sum(len(gs) - 1 for gs in dups.values()),
        }

    # ---------- E1 string-space reproduction (row-based, dups kept) ----------
    e1_repro, e1_self_loops = {}, {}
    e1_match = True
    for k in KS:
        e1_repro[f"k={k}"] = {}
        e1_self_loops[f"k={k}"] = {}
        str_edges, str_nodes = {}, {}
        for lang in LANGS:
            terms = [labs[lang] for (_, _, labs) in rows
                     if labs[lang] in vec_map]  # 217, duplicates kept
            mat = np.array([vec_map[t] for t in terms], dtype=np.float64)
            edges, loops = knn_edges_dup_keys(terms, mat, k)
            str_edges[lang] = edges
            str_nodes[lang] = terms
            e1_self_loops[f"k={k}"][lang] = loops
        for (la, lb) in PAIRS:
            r = lds_jaccard(str_nodes[la], str_nodes[lb],
                            str_edges[la], str_edges[lb])
            e1_repro[f"k={k}"][f"{la}-{lb}"] = r
            if abs(r["lds_score"] - E1_STRING_FROZEN[f"k={k}"][f"{la}-{lb}"]) > 1e-4:
                e1_match = False

    # ---------- gid-space kNN graphs (unique gids, first-row labels) ----------
    gid_results, gid_edges_info, gid_self_loops = {}, {}, {}
    for k in KS:
        gid_results[f"k={k}"] = {}
        gid_edges_info[f"k={k}"] = {}
        gid_self_loops[f"k={k}"] = {}
        gedges = {}
        for lang in LANGS:
            gids = gids_with_vec[lang]
            mat = np.array([vec_map[first_labels[gid][lang]] for gid in gids],
                           dtype=np.float64)
            edges, loops = knn_edges_numpy(gids, mat, k)
            gedges[lang] = edges
            gid_self_loops[f"k={k}"][lang] = loops
            n = len(gids)
            e = len(edges)
            gid_edges_info[f"k={k}"][lang] = {
                "nodes": n, "edges": e,
                "density": round(2 * e / (n * (n - 1)), 6),
                "avg_degree": round(2 * e / n, 4),
            }
        for (la, lb) in PAIRS:
            gid_results[f"k={k}"][f"{la}-{lb}"] = lds_jaccard(
                gids_with_vec[la], gids_with_vec[lb],
                gedges[la], gedges[lb])

    # ---------- rank corr vs frozen LDS-K (order only) ----------
    rank_block = {
        "method": ("Spearman rho over n=3 language pairs with midrank "
                   "ties; descriptive only; exact two-sided permutation p; "
                   "human pilot N=8: no significance claims anywhere"),
        "LDS_K_frozen_asc": ["zh-de", "zh-en", "de-en"],
        "LDS_K_values_for_order_only": LDS_K_FROZEN,
        "ban": ("order-structure only; forbidden: any numeric comparison of "
                "LDS-VEC(gid) vs LDS-K values (cross-dimension unit ban); "
                "forbidden: significance language at n=3 and at human N=8; "
                "forbidden: EN order-gap claims on near-ties (T-P5-3 analog)"),
    }
    for k in KS:
        scores = {p: gid_results[f"k={k}"][p]["lds_score"]
                  for p in ("zh-de", "zh-en", "de-en")}
        asc, _ = ranks_from_scores(scores)
        ref = {"zh-de": 0.519, "zh-en": 0.934, "de-en": 0.938}
        rho, p = spearman_with_ties(scores, ref)
        tied = sorted({v for v in scores.values() if
                       sum(1 for x in scores.values() if x == v) > 1})
        rank_block[f"k={k}"] = {
            "LDS_VEC_gid_asc": asc,
            "LDS_VEC_gid_values": scores,
            "rho": rho, "exact_two_sided_p": round(p, 4),
            "p_note": "n.s.: n=3 has no power (descriptive only)",
            "tied_values_at_4dp": tied,
            "tie_note": ("any tied pair: no order claim between them "
                         "(T-P5-3 analog)") if tied else "no ties",
        }

    # ---------- sparsity vs human baseline (E3 context, still mismatched) ----------
    sparsity = {
        "human_baseline": {"nodes": 556, "edges": 238, "density": 0.001543,
                           "avg_degree": 0.8561},
        "gid_knn_per_lang": gid_edges_info,
        "verdict": ("kNN(gid) stays an order of magnitude denser than the "
                    "human textbook graph; cross-density Jaccard remains "
                    "confounded; sparsity-matched rerun (E3-full) PENDING"),
    }

    # ---------- gate self-evaluation ----------
    gate = {
        "E1b_measurement": "EXECUTED",
        "R5_node_census": ("Mature-ready at measurement-hygiene level: "
                           "rows->unique-gids audited, id-collisions logged, "
                           "217->219 cause closed, cross-gid duplicates "
                           "logged, self-loops 0 by construction"),
        "E1b_interpretation": ("Hypothesis (capped): n=3 rank has no power "
                               "(exact p n.s.); sparsity mismatch persists "
                               "(E3-full pending); zh-de n=65 down-weighted, "
                               "never sole carrier; N=8: no significance "
                               "claims"),
        "promote_to_Developing": False,
        "promote_reason": ("Developing requires the registered E3-full "
                           "sparsity-matched rerun (238-edge matching) plus "
                           "k-sensitivity accounting; E1b covers group-id "
                           "identity only, so the Hypothesis cap stays."),
    }

    out = {
        "lane": "Lane-3 weight-vs-human E1b gid-identity rerun",
        "date": "2026-09-16",
        "status": "EXECUTED (measurement); interpretation capped at Hypothesis",
        "exploratory_appendix_only": exploratory,
        "read_only_contract": {
            "writes": [OUT_PATH.resolve().relative_to(ROOT.resolve()).as_posix(),
                       "scripts/tools/weight_graph_E1b.py",
                       "research/weight_vs_human_E1b_20260916.md"],
            "untouched": ["tests/", "freeze/", "_deploy/", "data/",
                          "linguaGraph.db",
                          "scripts/tools/weight_graph_audit.py",
                          "research/weight_graph_audit_20260916.json"],
            "new_concepts": 0,
            "corpus_expanded": False,
            "lds_v3_formula_changed": False,
        },
        "inputs": {
            "aligned_rows": n_rows,
            "unique_gids": len(uniq_gids),
            "vectors_file": "research/weight_vectors_934x768_20260916.term2vec.json",
            "n_terms": len(vec_map), "dim": dim,
            "model": "text-embedding-nomic-embed-text-v1.5",
            "model_revision": "not exposed by LM Studio /v1/models (as in E1)",
            "lds_k_frozen": LDS_K_FROZEN,
        },
        "translation_layer": {
            "R_intra": "three labels of one aligned group share ONE node (gid)",
            "R_gid": ("rows sharing one gid collapse to the FIRST row in "
                      "aligned-file order; all 18 collisions recorded"),
            "R_cross": ("same surface label across DISTINCT gids maps to the "
                        "FIRST gid in file order, per language; all "
                        "collisions recorded; nodes NOT merged (merge would "
                        "re-contaminate J_node via surface equality)"),
            "R_loop": "self-loops (gid==gid) removed and counted",
            "row_census": {
                "aligned_rows": n_rows,
                "unique_gids": len(uniq_gids),
                "id_collisions": len(id_collisions),
                "rows_with_vectors_per_lang":
                    {l: len(rows_with_vec[l]) for l in LANGS},
                "rows_missing_vectors_all_langs": rows_missing_all,
            },
            "id_collisions": id_collisions,
            "missing_gids": [
                {"gid": gid,
                 "labels": first_labels[gid],
                 "cause": ("label absent from the 934 term matrix: not in "
                           "the 700 deduplicated extraction names AND all "
                           "pairs of this group were excluded as "
                           "surface-identical, so the label never entered "
                           "the 434 primary-pair supplement set; no vector "
                           "was ever embedded for it")}
                for gid in missing_gids
            ],
            "missing_rate_gid": f"{len(missing_gids)}/{len(uniq_gids)}",
            "node_gids_per_lang": {l: len(gids_with_vec[l]) for l in LANGS},
            "gid_sets_identical_across_langs": sets_identical,
            "j_node_by_construction": 1.0 if sets_identical else "see results",
            "per_lang_cross_gid_duplicates": per_lang_dup,
            "n_cross_gid_duplicate_records": len(dup_records),
            "cross_gid_duplicates": dup_records,
            "e1_baseline_self_loops_row_string_space": e1_self_loops,
            "e1b_self_loops_removed_gid_space": gid_self_loops,
        },
        "method": {
            "nodes": ("unique-gid sets per language (identical -> "
                      "J_node=1.0 by construction)"),
            "edges": ("per-language symmetrized kNN (k=5/10/15, cosine) over "
                      "gid vectors V(gid,lang)=vec[first-row label]; "
                      "edge endpoints compared as gid pairs"),
            "formula": ("LDS v3 Jaccard reuse "
                        "(docs/lds_formal_definition.md 8.1), unmodified"),
            "tie_rule": "stable argsort (file order), mirrors E1 stable sort",
            "e1_reproduction_check": {
                "numpy_knn_reproduces_E1_row_string_space": e1_match,
                "recomputed": e1_repro,
                "frozen_E1": E1_STRING_FROZEN,
            },
            "rank_method": ("Spearman rho (midrank ties) over n=3 pairs, "
                            "descriptive; exact permutation p; order-only"),
        },
        "results_LDS_VEC_gid": gid_results,
        "rank_corr_vs_LDS_K_order_only": rank_block,
        "sparsity_E3_context": sparsity,
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
        "LDS_VEC_gid": gid_results,
        "rank": {k: rank_block[k] for k in ("k=5", "k=10", "k=15")},
        "e1_repro_match": e1_match,
        "row_census": out["translation_layer"]["row_census"],
        "out": str(OUT_PATH),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

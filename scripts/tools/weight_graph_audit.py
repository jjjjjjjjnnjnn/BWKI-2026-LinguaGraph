#!/usr/bin/env python3
"""Lane-3 weight-vs-human read-only audit (E1-E3 + contamination 4-branch).

READ-ONLY CONTRACT (violations abort):
  - NEVER writes to tests/, freeze/, _deploy/, data/, linguaGraph.db.
  - NEVER adds concepts, NEVER expands corpus, NEVER changes LDS v3 formula
    (LDS Jaccard form below is a verbatim reuse of docs/lds_formal_definition.md
    section 8.1, not a modification).
  - All new statistics are exploratory appendix-only (flagged in output JSON
    and in research/weight_vs_human_audit_20260916.md).
  - Inputs are existing frozen files + %TEMP%/opencode cache (read-only).
  - The ONLY write target is research/weight_graph_audit_20260916.json
    (+ stdout). No new model runs: per-term 768-d vectors were never persisted
    (TEMP cache holds aggregates only), LM Studio is offline, so E1-vector,
    E2-partial-correlation and rewrite/layer branches emit PENDING records with
    the exact required model/data instead of fabricated numbers.

Usage (system python is fine; stdlib only):
  python scripts/tools/weight_graph_audit.py
  python scripts/tools/weight_graph_audit.py --vectors <term2vec.json>
      (optional future path: JSON {term: [768 floats]}; enables E1 kNN branch)
"""

import argparse
import json
import math
import os
import sys
import tempfile
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ALIGNED_PATH = ROOT / "data" / "math_extractions" / "merged" / "aligned_data.json"
VIS_PATH = ROOT / "data" / "math_extractions" / "merged" / "visualization_data.json"
TWO_TIER_CACHE = Path(tempfile.gettempdir()) / "opencode" / "openweight_embed_audit.json"
OUT_PATH = ROOT / "research" / "weight_graph_audit_20260916.json"

# Frozen reference values (read-only copies; script never recomputes LDS-K).
# Source: scripts/analyze_human_lds.py:23-28 + docs/lds_formal_definition.md sect 2.1
LDS_K_FROZEN = {"ZH-EN": 0.934, "DE-EN": 0.938, "ZH-DE": 0.519}
# Source: research/two_tier_benchmark_20260914.md sect 2 (read-only expected values)
VEC_EXPECTED = {
    "zh-de": {"n": 65, "mean": 0.4804},
    "zh-en": {"n": 184, "mean": 0.5249},
    "de-en": {"n": 185, "mean": 0.4888},
    "overall": {"n": 434, "mean": 0.5029},
}
KS = (5, 10, 15)

FORBIDDEN_WRITE_PREFIXES = ("tests", "freeze", "_deploy", "data", "linguaGraph.db")


def guard_output(path: Path) -> None:
    rel = path.resolve().relative_to(ROOT.resolve()).as_posix()
    for prefix in FORBIDDEN_WRITE_PREFIXES:
        if rel == prefix or rel.startswith(prefix + "/"):
            raise SystemExit(f"[ABORT] write target inside forbidden zone: {rel}")
    if not rel.startswith("research/"):
        raise SystemExit(f"[ABORT] write target must be inside research/: {rel}")


def norm(s: str) -> str:
    s = (s or "").strip().lower()
    for ch in (" ", "\t", "-", "_", "/", "(", ")", "[", "]", ".", ",", ":", ";"):
        s = s.replace(ch, "")
    return s.replace("\u00df", "ss")


def lds_jaccard(nodes_a, nodes_b, edges_a, edges_b):
    """Verbatim reuse of docs/lds_formal_definition.md sect 8.1 (NOT modified)."""
    set_a, set_b = set(nodes_a), set(nodes_b)
    node_jac = len(set_a & set_b) / max(len(set_a | set_b), 1)
    ea, eb = set(edges_a), set(edges_b)
    edge_jac = len(ea & eb) / max(len(ea | eb), 1)
    lds = 1.0 - (node_jac + edge_jac) / 2
    return {"lds_score": round(lds, 4), "jaccard_node": round(node_jac, 4),
            "jaccard_edge": round(edge_jac, 4)}


def cos_dist(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 1.0
    return 1.0 - dot / (na * nb)


def knn_edges(terms, vectors, k):
    """Symmetrized kNN edge set over term list using cosine distance."""
    n = len(terms)
    edges = set()
    for i, t in enumerate(terms):
        dists = []
        for j, u in enumerate(terms):
            if i == j:
                continue
            dists.append((cos_dist(vectors[t], vectors[u]), u))
        dists.sort(key=lambda x: x[0])
        for _, u in dists[: min(k, n - 1)]:
            edges.add(tuple(sorted((t, u))))
    return edges


def load_aligned_pairs():
    """Recount primary pairs from frozen aligned table (no model needed)."""
    d = json.loads(ALIGNED_PATH.read_text(encoding="utf-8"))
    groups = d.get("aligned_groups", [])
    pairs = []  # (term_a, lang_a, term_b, lang_b, gid)
    excluded_surface_identical = defaultdict(int)
    empty_label_groups = 0
    for g in groups:
        gid = g.get("id", "?")
        labels = g.get("labels", {}) or {}
        if not all((labels.get(l) or "").strip() for l in ("zh", "en", "de")):
            empty_label_groups += 1
        for (la, lb) in (("zh", "de"), ("zh", "en"), ("de", "en")):
            a = (labels.get(la) or "").strip()
            b = (labels.get(lb) or "").strip()
            if not a or not b:
                excluded_surface_identical[("missing", tuple(sorted((la, lb))))] += 1
                continue
            if norm(a) == norm(b):
                excluded_surface_identical[("surface_identical", tuple(sorted((la, lb))))] += 1
                continue
            key = "-".join(sorted((la, lb)))
            key = {"de-zh": "zh-de", "en-zh": "zh-en"}.get(key, key)
            pairs.append((a, la, b, lb, gid, key))
    by_pair = defaultdict(int)
    for p in pairs:
        by_pair[p[5]] += 1
    return groups, pairs, by_pair, excluded_surface_identical, empty_label_groups


def probe_lm_studio():
    try:
        with urllib.request.urlopen("http://127.0.0.1:1234/v1/models", timeout=3) as r:
            body = r.read().decode("utf-8", errors="replace")
        return {"alive": True, "note": body[:200]}
    except Exception as e:
        return {"alive": False, "note": f"{type(e).__name__}: {e}"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vectors", default="",
                    help="optional JSON {term: [float,...]} to enable E1 kNN branch")
    args = ap.parse_args()
    guard_output(OUT_PATH)

    status = {}   # experiment_id -> EXECUTED / PENDING
    detail = {}
    exploratory = True  # every new number below is appendix-only

    # ---- R1 (EXECUTED): recount 219 groups -> 434 pairs, ZH-DE vs EN split ----
    groups, pairs, by_pair, excl, empty_groups = load_aligned_pairs()
    n_groups = len(groups)
    r1 = {
        "aligned_groups": n_groups,
        "primary_pairs_total": len(pairs),
        "by_pair": {k: by_pair.get(k, 0) for k in ("zh-de", "zh-en", "de-en")},
        "groups_with_any_empty_label": empty_groups,
        "excluded_surface_identical_or_missing": {
            f"{reason}/{''.join(k)}": v for (reason, k), v in sorted(excl.items())
        },
        "exploratory_appendix_only": exploratory,
    }
    status["R1_pair_recount"] = "EXECUTED"
    detail["R1_pair_recount"] = r1

    # ---- R2 (EXECUTED): verify TEMP aggregate cache vs two_tier report ----
    r2 = {"cache_path": str(TWO_TIER_CACHE), "cache_found": TWO_TIER_CACHE.exists()}
    if r2["cache_found"]:
        cache = json.loads(TWO_TIER_CACHE.read_text(encoding="utf-8"))
        drift = cache.get("drift_cosine_distance", {})
        check = {}
        for k, exp in VEC_EXPECTED.items():
            got = drift.get(k, drift.get("_overall", {}) if k == "overall" else {})
            check[k] = {
                "expected_n": exp["n"], "got_n": got.get("n"),
                "expected_mean": exp["mean"], "got_mean": got.get("mean"),
                "match": (got.get("n") == exp["n"] and got.get("mean") == exp["mean"]),
            }
        r2["aggregate_match_vs_two_tier_report"] = check
        r2["per_pair_distances_available"] = False  # aggregates only, no vectors
        r2["model"] = cache.get("model")
        r2["dim"] = cache.get("dim")
    else:
        r2["aggregate_match_vs_two_tier_report"] = "PENDING (cache absent)"
    status["R2_aggregate_verify"] = "EXECUTED"
    detail["R2_aggregate_verify"] = r2

    # ---- R3 (EXECUTED, human side): textbook graph sparsity baseline ----
    vis = json.loads(VIS_PATH.read_text(encoding="utf-8"))
    nodes = vis.get("nodes", [])
    links = vis.get("links", [])
    n = len(nodes)
    e = len(links)
    density = (2 * e / (n * (n - 1))) if n > 1 else 0.0
    avg_deg = (2 * e / n) if n else 0.0
    r3 = {
        "human_nodes": n, "human_edges": e,
        "human_density_undirected": round(density, 6),
        "human_avg_degree": round(avg_deg, 4),
        "human_sparsity_1_minus_density": round(1 - density, 6),
        "knn_matching_targets": {
            f"k={k}": {
                "note": ("future per-language kNN graph over 219 aligned labels "
                         "must be sparsity-matched to this human baseline before "
                         "any LDS-VEC vs LDS-K comparison"),
                "max_edges_per_lang_undirected_symmetrized_le": 219 * k,
            } for k in KS
        },
        "exploratory_appendix_only": exploratory,
    }
    status["R3_human_sparsity"] = "EXECUTED"
    detail["R3_human_sparsity"] = r3

    # ---- R4 (EXECUTED): LM Studio liveness probe (reason for PENDINGs) ----
    r4 = probe_lm_studio()
    status["R4_lm_probe"] = "EXECUTED"
    detail["R4_lm_probe"] = r4

    # ---- E1 (PENDING unless --vectors): kNN graph LDS-VEC, k=5/10/15 ----
    e1 = {"ks": list(KS), "formula": "LDS v3 Jaccard reuse (docs/lds_formal_definition.md 8.1), unmodified"}
    vec_map = None
    if args.vectors:
        vd = json.loads(Path(args.vectors).read_text(encoding="utf-8"))
        if isinstance(vd, dict) and vd:
            dim = len(next(iter(vd.values())))
            vec_map = vd
            e1["vector_dim"] = dim
            e1["n_terms_with_vectors"] = len(vec_map)
    if vec_map is None:
        e1["status_detail"] = (
            "PENDING: no per-term 768-d vectors available. TEMP cache holds "
            "per-pair aggregates only (mean/std/min/max); sem_emb_cache.json holds "
            "10615 EN corpus sentence vectors (wrong object: sentences, not aligned "
            "concept terms). LM Studio probe says "
            + ("ALIVE (unexpected)" if r4["alive"] else "OFFLINE (connection refused)")
            + ". Do NOT re-run the large model inside this lane."
        )
        e1["required_to_unblock"] = (
            "text-embedding-nomic-embed-text-v1.5 via LM Studio "
            "http://127.0.0.1:1234/v1 (or a persisted 934x768 term matrix) "
            "to embed the 934 deduplicated concept terms; then build symmetrized "
            "kNN graphs per language (k=5/10/15) over the 219 aligned labels and "
            "compute LDS-VEC per pair with the frozen Jaccard formula."
        )
        status["E1_knn_lds_vec"] = "PENDING"
    else:
        langs = {"zh": [], "en": [], "de": []}
        for g in groups:
            labels = g.get("labels", {}) or {}
            for l in langs:
                t = (labels.get(l) or "").strip()
                if t and t in vec_map:
                    langs[l].append(t)
        e1_results = {}
        for k in KS:
            ek = {}
            for (la, lb) in (("zh", "de"), ("zh", "en"), ("de", "en")):
                ea = knn_edges(langs[la], vec_map, k)
                eb = knn_edges(langs[lb], vec_map, k)
                ek[f"{la}-{lb}"] = lds_jaccard(langs[la], langs[lb], ea, eb)
            e1_results[f"k={k}"] = ek
        e1["results"] = e1_results
        status["E1_knn_lds_vec"] = "EXECUTED"
    e1["exploratory_appendix_only"] = exploratory
    detail["E1_knn_lds_vec"] = e1

    # ---- E2 (PENDING): frequency-similarity partial correlation ----
    e2 = {
        "status_detail": (
            "PENDING: no frozen math-corpus term-frequency table exists. "
            "data/corpus/corpus_analysis.json covers the Wikipedia SOCIAL pilot "
            "(freedom/justice/...) — domain-mismatched, must NOT be substituted. "
            "Raw textbook text is referenced-only (not versioned); building a new "
            "frequency table would expand the corpus, which is forbidden. "
            "Per-pair cosine distances are likewise unavailable (aggregates only)."
        ),
        "required_to_unblock": (
            "frozen per-concept frequency counts from the ALREADY-USED math textbook "
            "exposure set (no new texts), plus persisted per-pair (n=434) cosine "
            "distances; then Spearman rho + partial correlation controlling for "
            "surface-form identity, reported ZH-DE vs EN separately."
        ),
        "exploratory_appendix_only": exploratory,
    }
    status["E2_freq_sim_partialcorr"] = "PENDING"
    detail["E2_freq_sim_partialcorr"] = e2

    # ---- E3 (human side EXECUTED, vector side PENDING): sparsity-matched control ----
    e3 = {
        "human_side": "EXECUTED (see R3_human_sparsity)",
        "vector_side": ("PENDING (blocked on E1 vectors; kNN graphs must be "
                        "sparsity-matched to R3 baseline before comparison)"),
        "zh_de_vs_en_split": r1["by_pair"],
        "required_to_unblock": "same as E1",
        "exploratory_appendix_only": exploratory,
    }
    status["E3_sparsity_matched_control"] = "PARTIAL (human EXECUTED, vector PENDING)"
    detail["E3_sparsity_matched_control"] = e3

    # ---- Contamination 4-branch table ----
    contam = {
        "branch_1_frequency": {
            "status": "PENDING",
            "what": "vector similarity driven by pretraining frequency, not structure",
            "reason": "same blockers as E2 (no math freq table; corpus expansion forbidden)",
            "needs": "frozen math-corpus frequencies + per-pair distances (E2)",
        },
        "branch_2_rephrase": {
            "status": "PENDING",
            "what": "paraphrase/translation rephrased-sample contamination (Yang et al. 2023)",
            "reason": "no new weights run in this lane; literal dedup (norm) is insufficient per literature",
            "needs": ("LLM-based semantic decontaminator or paraphrase-embedding pass "
                      "(e.g. multilingual paraphrase model) over the 934 terms + 434 pairs; "
                      "no suitable local weight is online (LM Studio offline)"),
        },
        "branch_3_zh_de_asymmetry": {
            "status": "PARTIAL (recount EXECUTED, interpretation downgraded)",
            "what": ("zh-de primary pairs are thinnest (n=65 vs 184/185); most groups "
                     "share one surface form across zh/de and are excluded by rule"),
            "evidence": {
                "by_pair": r1["by_pair"],
                "excluded": r1["excluded_surface_identical_or_missing"],
            },
            "rule": "zh-de vector estimates are down-weighted; no conclusion may rest on zh-de alone",
        },
        "branch_4_cross_tier": {
            "status": "EXECUTED as guardrail; weight-side layer test PENDING",
            "what": "cross-dimension comparison ban: cosine distance (distribution proximity) "
                    "vs LDS-K = 1-mean(node/edge Jaccard) (curricular structure) share no unit",
            "guardrail": ("report order-structure only (vector range 0.0445 vs graph range 0.419); "
                          "forbidden sentence: vector validates/confirms any LDS-K value; "
                          "zh-de -0.04 closeness is a unit coincidence"),
            "needs": "E1 vectors for the layer-specific dissociation test",
        },
    }
    status["contamination_4branch"] = "MIXED (2 EXECUTED/PARTIAL guardrails, 2 PENDING)"
    detail["contamination_4branch"] = contam

    out = {
        "lane": "Lane-3 weight-vs-human read-only audit",
        "date": "2026-09-16",
        "read_only_contract": {
            "writes": [OUT_PATH.resolve().relative_to(ROOT.resolve()).as_posix()],
            "untouched": ["tests/", "freeze/", "_deploy/", "data/", "linguaGraph.db"],
            "new_concepts": 0,
            "corpus_expanded": False,
            "lds_v3_formula_changed": False,
        },
        "inputs": {
            "aligned_data_groups": n_groups,
            "lds_k_frozen": LDS_K_FROZEN,
            "nomic_model": "text-embedding-nomic-embed-text-v1.5, dim=768",
            "lm_studio_alive": r4["alive"],
        },
        "status": status,
        "detail": detail,
        "cross_dimension_ban": ("cosine distance and LDS-K share no unit; "
                                "order-structure comparison only"),
        "en_cap_zh_de_rule": {
            "EN_cap": ("EN-involved vector claims stay distribution-level; "
                       "no per-concept validation sentences"),
            "ZH_DE_rule": "zh-de (n=65, thinnest) down-weighted; never sole carrier",
        },
    }
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": status, "out": str(OUT_PATH)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

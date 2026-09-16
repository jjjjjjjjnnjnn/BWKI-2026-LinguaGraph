#!/usr/bin/env python3
"""Headline-number reproduction check (frozen inputs, independent re-derivation).

Recomputes headline figures from frozen sources and diffs them against
research/numbers_ssot_20260916.json claims. Does NOT import numbers_audit.py.
Graph/LDS math is re-derived from the frozen merged JSONs via the pipeline's
own _lds_utils (same formula the figures use); replication counts are
re-derived from data/lds_c/llm_subject/multi_model_replication_20260913.json
with the formal-set rule documented in scripts/sw_fix_analyses.py.

Usage: python scripts/tools/reproduce_headline.py
Output: research/reproduce_headline_20260916.json + PASS/FAIL on stdout.
Exit 0 = all match; 1 = any mismatch (data is NOT fixed here).
"""
import json
import math
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "figures"))
from _lds_utils import get_lang_graphs, lds_jaccard, load_aligned  # noqa: E402

SSOT = PROJECT_ROOT / "research" / "numbers_ssot_20260916.json"
OUT = PROJECT_ROOT / "research" / "reproduce_headline_20260916.json"

items = []


def add(item_id, claim, recomputed, detail=""):
    match = claim == recomputed
    items.append({"id": item_id, "claim": claim, "recomputed": recomputed,
                  "match": match, "detail": detail})
    return match


def load_json(path):
    return json.loads((PROJECT_ROOT / path).read_text(encoding="utf-8"))


def parse_js_var(path, var):
    t = (PROJECT_ROOT / path).read_text(encoding="utf-8")
    m = re.search(r"var\s+" + re.escape(var) + r"\s*=\s*(\{.*)\s*;\s*$", t, re.S)
    if not m:
        raise ValueError("var %s not found in %s" % (var, path))
    return t, json.loads(m.group(1))


def main():
    ssot = load_json("research/numbers_ssot_20260916.json")
    manifest = load_json("manifest.json")
    aligned = load_json("data/math_extractions/merged/aligned_data.json")
    vis = load_json("data/math_extractions/merged/visualization_data.json")
    snap = load_json("data/math_extractions/merged/pipeline_snapshot.json")
    merged_rel = load_json("data/math_extractions/merged/merged_relations.json")

    # ---- 1. graph counts from merged JSONs + manifest + snapshot ----
    n_nodes = len(vis["nodes"])
    add("nodes_556", 556, n_nodes,
        "len(visualization_data.nodes); manifest=%s snapshot=%s" % (
            manifest["graph"]["total_nodes"], snap["nodes"]))
    add("manifest_nodes_556", 556, manifest["graph"]["total_nodes"], "manifest.graph.total_nodes")
    n_rel = len(aligned["relations"])
    add("relations_517", 517, n_rel,
        "len(aligned_data.relations); field=%s merged_relations=%s snapshot=%s manifest=%s" % (
            aligned["total_relations"], merged_rel["total_relations"],
            snap["relations"], manifest["alignment"]["total_relations"]))
    n_grp = len(aligned["aligned_groups"])
    add("groups_219", 219, n_grp,
        "len(aligned_data.aligned_groups); field=%s snapshot=%s manifest=%s" % (
            aligned["total_aligned_groups"], snap["aligned_groups"],
            manifest["alignment"]["aligned_groups"]))
    n_links = len(vis["links"])
    add("links_233", 233, n_links,
        "len(visualization_data.links); manifest=%s snapshot=%s" % (
            manifest["graph"]["total_links"], snap["links"]))

    # ---- 2. viewer data.js counts (header + metadata + actual arrays) ----
    raw_js, data_js = parse_js_var("cognitive-space/web/data.js", "data")
    hm = re.search(r"(\d+)\s+nodes\s*\|\s*(\d+)\s+links", raw_js)
    add("viewer_header_556_233", [556, 233],
        [int(hm.group(1)), int(hm.group(2))], "data.js header comment")
    add("viewer_meta_556_233", [556, 233],
        [data_js["metadata"]["total_nodes"], data_js["metadata"]["total_links"]],
        "data.js metadata")
    add("viewer_actual_556_233", [556, 233],
        [len(data_js["nodes"]), len(data_js["links"])], "data.js actual arrays")

    # ---- 3. LDS-K re-derived from aligned_data.json ----
    lang_nodes, lang_edges = get_lang_graphs(load_aligned())
    lds = {}
    for name, pair in (("zh_en", ("zh", "en")), ("de_en", ("de", "en")),
                       ("zh_de", ("zh", "de"))):
        r = lds_jaccard(lang_nodes[pair[0]], lang_nodes[pair[1]],
                        list(lang_edges[pair[0]]), list(lang_edges[pair[1]]))
        lds[name] = round(r["lds_score"], 3)
    tier1 = ssot["lds_k_tier1"]
    add("lds_zh_en", tier1["zh_en"], lds["zh_en"], "1-mean(J_node,J_edge) on aligned groups")
    add("lds_de_en", tier1["de_en"], lds["de_en"], "ditto")
    add("lds_zh_de", tier1["zh_de"], lds["zh_de"], "ditto")
    add("lds_spread", tier1["spread"],
        round(max(lds.values()) - min(lds.values()), 3), "max-min of rounded trio")

    # ---- 4. replication 59/54/177 + file-truth 62/57/186 ----
    rep = load_json("data/lds_c/llm_subject/multi_model_replication_20260913.json")
    models = rep["models"]

    def is_formal(m):
        bp = m.get("by_pair", {}).get("ZH-DE", {})
        margin = bp.get("margin")
        return (m.get("n") == 30 and bp.get("perm_p", 1.0) < 0.05
                and not (isinstance(margin, float) and math.isnan(margin)))

    formal = {k: v for k, v in models.items() if is_formal(v)}

    def ident(k):
        s = k.lower()
        s = s.rsplit("/", 1)[-1] if "/" in s else s.rsplit(":", 1)[-1]
        for suf in (":free", "-free", "_free"):
            if s.endswith(suf):
                s = s[: -len(suf)]
        return s

    formal_ids = {ident(k) for k in formal}
    voters = {k: v for k, v in models.items() if "ZH-DE" in v.get("by_pair", {})}
    voter_ids = {ident(k) for k in voters}
    add("repl_measurements_59", 59, len(formal), "formal set: n==30, ZH-DE p<0.05, margin non-NaN")
    add("repl_models_54", 54, len(formal_ids), "unique identities in formal set")
    add("repl_tests_177", 177, len(formal) * 3, "59 measurements x 3 pairs")
    add("filetruth_measurements_62", 62, len(voters), "keys with ZH-DE by_pair (any n/sig)")
    add("filetruth_models_57", 57, len(voter_ids), "unique identities among voters")
    add("filetruth_tests_186", 186, len(voters) * 3, "62 voters x 3 pairs")
    en_ns = sum(1 for m in formal.values()
                for p in ("ZH-EN", "DE-EN")
                if m.get("by_pair", {}).get(p, {}).get("perm_p", 0) >= 0.05)
    add("repl_en_ns_9_of_177", 9, en_ns, "EN-involved pairs with perm_p>=0.05 in formal set")

    markers = ("nemotron", "laguna", "gpt-oss", "command", "luna", "gemma",
               "grok", "muse-spark", "mistral", "llama", "phi")
    west = [k for k in formal if any(x in k.lower() for x in markers)]
    cn = [k for k in formal if k not in west]
    add("strata_cn_48_48", [48, 48],
        [len(cn), sum(1 for k in cn if formal[k]["by_pair"]["ZH-DE"]["perm_p"] < 0.05)],
        "CN-vendor formal runs, ZH-DE significant")
    add("strata_west_11_11", [11, 11],
        [len(west), sum(1 for k in west if formal[k]["by_pair"]["ZH-DE"]["perm_p"] < 0.05)],
        "Western formal runs, ZH-DE significant")
    wol = [k for k in west if "luna" not in k.lower()]
    add("strata_west_ohne_luna_10_10", [10, 10],
        [len(wol), sum(1 for k in wol if formal[k]["by_pair"]["ZH-DE"]["perm_p"] < 0.05)],
        "Western excl. luna")

    # dedup: first occurrence per identity, mean ZH-DE margin
    seen, dmargins = set(), []
    for k in formal:  # dict order = file order
        i = ident(k)
        if i not in seen:
            seen.add(i)
            dmargins.append(formal[k]["by_pair"]["ZH-DE"]["margin"])
    add("dedup_54_54", [54, 54], [len(dmargins), len(dmargins)],
        "one row per identity, all ZH-DE significant by formal rule")
    add("dedup_margin_0.137", 0.137,
        round(sum(dmargins) / len(dmargins), 3), "mean margin, first-occurrence dedup")

    # youden: deterministic part only (median-split optimal threshold, no bootstrap)
    margins = sorted(m["by_pair"]["ZH-DE"]["margin"] for m in formal.values())
    med = margins[len(margins) // 2] if len(margins) % 2 else \
        (margins[len(margins) // 2 - 1] + margins[len(margins) // 2]) / 2
    labels = [1 if x > med else 0 for x in margins]

    def youden(th):
        pred = [1 if x >= th else 0 for x in margins]
        tp = sum(1 for p, l in zip(pred, labels) if p == 1 and l == 1)
        fn = sum(1 for p, l in zip(pred, labels) if p == 0 and l == 1)
        tn = sum(1 for p, l in zip(pred, labels) if p == 0 and l == 0)
        fp = sum(1 for p, l in zip(pred, labels) if p == 1 and l == 0)
        return tp / (tp + fn) - fp / (fp + tn)

    jmax = max(youden(t) for t in set(margins))
    opt = min(t for t in set(margins) if youden(t) == jmax)
    add("youden_0.12", 0.12, round(opt, 2),
        "optimal threshold on median-split halves (heuristic, not validated)")

    # ---- 5. STEAM 1143 nodes / 834 edges ----
    _, steam = parse_js_var("cognitive-space/web/data_steam.js", "data_steam")
    add("steam_nodes_1143", 1143, len(steam["nodes"]), "len(data_steam.nodes)")
    edges = steam.get("links", steam.get("edges", []))
    add("steam_edges_834", 834, len(edges), "len(data_steam.links)")
    src = steam.get("metadata", {}).get("sources", {})
    add("steam_parts_sum", [1143, 834],
        [sum(v["nodes"] for v in src.values()), sum(v["links"] for v in src.values())],
        "math 556/233 + physics 367/386 + chemistry 220/215")

    fails = [i for i in items if not i["match"]]
    out = {"generated_from": "frozen inputs listed in detail fields",
           "ssot": "research/numbers_ssot_20260916.json",
           "n_items": len(items), "n_match": len(items) - len(fails),
           "overall": "PASS" if not fails else "FAIL", "items": items}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("reproduce_headline: %s (%d/%d match) -> %s"
          % (out["overall"], out["n_match"], out["n_items"], OUT.name))
    for f in fails:
        print("MISMATCH %s claim=%r recomputed=%r (%s)"
              % (f["id"], f["claim"], f["recomputed"], f["detail"]))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())

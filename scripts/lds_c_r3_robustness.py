#!/usr/bin/env python3
"""LinguaGraph — R3: metric robustness (k-sensitivity + alignment robustness).

Research-forward review (2026-08-11), G5/G6. Two questions:

  Part A (k-sensitivity): concepts per topic are 5-6 (variable). Does LDS
    depend on how many concepts per topic we retain? Truncate each unit's
    per-topic concepts (sorted by importance desc) to k' in {3, 5, 6} and
    recompute per-pair margins for all 51 models. Checks: ZH-DE margin sign
    stability, pair-ordering stability.

  Part B (alignment robustness): LDS relies on exact canonical-key matching
    (the model's own translation to English keys). Does a LOOSE token-overlap
    alignment (two concepts match if they share >=1 content token) change the
    pair ordering or the DE/ZH direction asymmetry? Run on the baseline model.

Pure computation, zero new API. Reuses frozen helpers (aggregate_languages,
compute_pairwise, within_language_split_half, lds_concept, canonical_key).

Output: data/lds_c/llm_subject/metric_robustness_20260811.json + console.
"""

from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import (  # noqa: E402
    PAIRS,
    aggregate_languages,
    canonical_key,
    compute_pairwise,
    lds_concept,
    within_language_split_half,
)
from lds_c_llm_analyze import OUT_DIR  # noqa: E402
from lds_c_multi_model import MIN_UNITS_PER_LANG, discover_models, p1_records, lang_counts  # noqa: E402

PAIR_ORDER = ["ZH-EN", "DE-EN", "ZH-DE"]
K_SWEEP = [3, 5, 6]

_STOP = {"of", "the", "a", "an", "and", "to", "for", "in", "on", "at",
         "own", "s", "one", "its", "their", "by", "with", "as", "or"}


# ── Part A: k-sensitivity ───────────────────────────────────────────
def truncate_records(records: list, k: int) -> list:
    """Keep top-k concepts per topic (importance desc) for each record."""
    out = []
    for r in records:
        nr = dict(r)
        topics = []
        for t in r.get("topics", []):
            concepts = sorted(t.get("concepts", []),
                              key=lambda c: -(c.get("importance") or 0))[:k]
            topics.append({**t, "concepts": concepts})
        nr["topics"] = topics
        out.append(nr)
    return out


def pair_margins(records: list, n_iter_floor: int = 100) -> dict:
    agg = aggregate_languages(records)
    pw = compute_pairwise(agg)
    fl = within_language_split_half(records, n_iter=n_iter_floor)
    out = {}
    for pair, la, lb in PAIRS:
        lds = (pw.get(pair) or {}).get("ALL")
        floor = fl.get(pair)
        if lds is not None and floor is not None:
            out[pair] = {"lds": round(lds, 4), "floor": round(floor, 4),
                         "margin": round(lds - floor, 4)}
    return out


# ── Part B: fuzzy alignment ─────────────────────────────────────────
def tokens(key: str) -> set:
    return {w for w in key.split() if w and w not in _STOP}


def _concept_set(records: list) -> dict:
    by_lang: dict = {}
    for r in records:
        lang = r.get("language", "")
        s = by_lang.setdefault(lang, set())
        for t in r.get("topics", []):
            for c in t.get("concepts", []):
                k = canonical_key(c.get("en", ""))
                if k:
                    s.add(k)
    return by_lang


def fuzzy_matched(A: set, B: set) -> int:
    """Greedy bipartite match: count pairs sharing >=1 content token."""
    a_toks = [(a, tokens(a)) for a in A]
    b_list = list(B)
    b_toks = [tokens(b) for b in b_list]
    used = set()
    matched = 0
    for a, ta in a_toks:
        if not ta:
            continue
        best = None
        for j, tb in enumerate(b_toks):
            if j in used:
                continue
            if ta & tb:
                best = j
                break
        if best is not None:
            used.add(best)
            matched += 1
    return matched


def fuzzy_pair_report(records: list) -> dict:
    sets = _concept_set(records)
    out = {}
    for pair, la, lb in PAIRS:
        A, B = sets.get(la, set()), sets.get(lb, set())
        if not A or not B:
            continue
        strict_i = len(A & B)
        strict_u = len(A | B)
        matched = fuzzy_matched(A, B)
        out[pair] = {
            "nA": len(A), "nB": len(B),
            "strict_J": round(strict_i / strict_u, 4),
            "strict_lds": round(lds_concept(A, B), 4),
            "fuzzy_matched": matched,
            "fuzzy_J": round(matched / (len(A) + len(B) - matched), 4),
            "fuzzy_lds": round(1 - matched / (len(A) + len(B) - matched), 4),
        }
    return out


def fuzzy_driver_asymmetry(records: list) -> dict:
    """DE-only / ZH-only under strict vs fuzzy, on the baseline aggregate."""
    sets = _concept_set(records)
    A, B = sets.get("de", set()), sets.get("zh", set())
    strict_de_only = A - B
    strict_zh_only = B - A
    a_toks = {a: tokens(a) for a in A}
    b_toks = {b: tokens(b) for b in B}
    fuzzy_de_only = [a for a in A if not any(a_toks[a] & bt for bt in b_toks.values() if bt)]
    fuzzy_zh_only = [b for b in B if not any(b_toks[b] & at for at in a_toks.values() if at)]
    return {
        "nA_de": len(A), "nB_zh": len(B),
        "strict_de_only": len(strict_de_only), "strict_zh_only": len(strict_zh_only),
        "fuzzy_de_only": len(fuzzy_de_only), "fuzzy_zh_only": len(fuzzy_zh_only),
        "strict_dir_de_over_zh": len(strict_de_only) - len(strict_zh_only),
        "fuzzy_dir_de_over_zh": len(fuzzy_de_only) - len(fuzzy_zh_only),
    }


def main() -> None:
    models = discover_models()
    valid = {m: info for m, info in models.items() if "error" not in info}

    # ── Part A ──
    print("  Part A: k-sensitivity (51 models x k' in {3,5,6}) ...")
    k_res = {}
    for m, info in sorted(valid.items()):
        recs = p1_records(info["units"])
        counts = lang_counts(recs)
        if any(counts.get(l, 0) < MIN_UNITS_PER_LANG for l in ("zh", "de", "en")):
            continue
        k_res[m] = {}
        for k in K_SWEEP:
            k_res[m][k] = pair_margins(truncate_records(recs, k), n_iter_floor=100)

    # aggregate stats
    agg_k = {}
    for k in K_SWEEP:
        zhde = [k_res[m][k]["ZH-DE"]["margin"] for m in k_res if "ZH-DE" in k_res[m][k]]
        row = {"n": len(zhde),
               "n_positive": sum(1 for x in zhde if x > 0),
               "median_zhde_margin": round(statistics.median(zhde), 4),
               "min_zhde": round(min(zhde), 4), "max_zhde": round(max(zhde), 4)}
        # pair ordering stability: which pair has the max margin per model
        order = {"ZH-DE>EN": 0, "EN>ZH-DE": 0, "tie": 0}
        for m in k_res:
            mm = k_res[m][k]
            zd = mm.get("ZH-DE", {}).get("margin")
            en = max(mm.get("ZH-EN", {}).get("margin", -9e9),
                     mm.get("DE-EN", {}).get("margin", -9e9))
            if zd is None:
                continue
            if zd > en:
                order["ZH-DE>EN"] += 1
            elif zd < en:
                order["EN>ZH-DE"] += 1
            else:
                order["tie"] += 1
        row["pair_order_zhde_vs_en"] = order
        agg_k[k] = row

    print(f"{'k':>3s} {'n':>3s} {'ZHDE pos%':>9s} {'med ZHDE':>9s} {'min':>7s} {'max':>7s} {'ZHDE>EN':>8s}")
    for k in K_SWEEP:
        a = agg_k[k]
        print(f"{k:>3d} {a['n']:>3d} {100*a['n_positive']/a['n']:>8.0f}% "
              f"{a['median_zhde_margin']:>+9.3f} {a['min_zhde']:>+7.3f} {a['max_zhde']:>+7.3f} "
              f"{a['pair_order_zhde_vs_en']}")

    # ── Part B (baseline model) ──
    print("\n  Part B: fuzzy-alignment robustness (baseline) ...")
    baseline_units = None
    for m, info in models.items():
        if "deepseek-v4-flash" in m and "dashscope" in m:
            baseline_units = info["units"]
            break
    if baseline_units is None:
        baseline_units = valid["deepseek-v4-flash"]["units"]
    brecs = p1_records(baseline_units)
    fuzzy_pairs = fuzzy_pair_report(brecs)
    fuzzy_dir = fuzzy_driver_asymmetry(brecs)

    print("  pair-level strict vs fuzzy LDS:")
    for pair in PAIR_ORDER:
        r = fuzzy_pairs.get(pair)
        if not r:
            continue
        print(f"    {pair}: strict_lds={r['strict_lds']:.3f} fuzzy_lds={r['fuzzy_lds']:.3f} "
              f"strict_J={r['strict_J']:.3f} fuzzy_J={r['fuzzy_J']:.3f}")
    print("  DE/ZH direction asymmetry (strict vs fuzzy):")
    print(f"    strict de_only={fuzzy_dir['strict_de_only']} zh_only={fuzzy_dir['strict_zh_only']} "
          f"dir={fuzzy_dir['strict_dir_de_over_zh']:+d}")
    print(f"    fuzzy  de_only={fuzzy_dir['fuzzy_de_only']} zh_only={fuzzy_dir['fuzzy_zh_only']} "
          f"dir={fuzzy_dir['fuzzy_dir_de_over_zh']:+d}")

    out = {
        "design": "r3_metric_robustness",
        "generated_at": datetime.now().isoformat(),
        "part_a_k_sensitivity": {"k_sweep": K_SWEEP, "aggregate": agg_k,
                                 "per_model": {m: {str(k): v for k, v in d.items()}
                                               for m, d in k_res.items()}},
        "part_b_fuzzy_alignment": {"pairs": fuzzy_pairs, "driver_asymmetry": fuzzy_dir},
    }
    out_path = OUT_DIR / "metric_robustness_20260811.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()

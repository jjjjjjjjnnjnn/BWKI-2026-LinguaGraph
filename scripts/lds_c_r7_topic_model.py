#!/usr/bin/env python3
"""LinguaGraph — R7: topic x model margin table for the 51-model replication.

Research-forward review (2026-08-11), G4. Asks: is the ZH-DE language signal
present in EVERY topic across all 51 models, or driven by 1-2 topics?

For each complete model (>= MIN_UNITS_PER_LANG P1 units per language) and each
pair (ZH-EN / DE-EN / ZH-DE), computes the per-topic LDS-C (pooled) and the
per-topic within-language split-half floor, then margin = lds - floor.

Pure computation on committed subject files. Reuses frozen helpers only
(lds_concept via per_topic_pairwise / per_topic_split_half). No metric change.

Output: data/lds_c/llm_subject/topic_model_margins_20260811.json + console.
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import PAIRS, TOPICS  # noqa: E402
from lds_c_llm_analyze import OUT_DIR  # noqa: E402
from lds_c_llm_per_topic import per_topic_pairwise, per_topic_split_half  # noqa: E402
from lds_c_multi_model import MIN_UNITS_PER_LANG, discover_models, p1_records, lang_counts  # noqa: E402

PAIR_ORDER = ["ZH-EN", "DE-EN", "ZH-DE"]


def percentile(vals: list, p: float) -> float:
    s = sorted(vals)
    if not s:
        return float("nan")
    idx = min(len(s) - 1, int(p * len(s)))
    return s[idx]


def analyze_model(units) -> dict:
    """Per-topic margins for one model."""
    recs = p1_records(units)
    counts = lang_counts(recs)
    if any(counts.get(l, 0) < MIN_UNITS_PER_LANG for l in ("zh", "de", "en")):
        return {"error": f"incomplete P1 data ({dict(counts)})", "n": len(recs)}
    p1 = per_topic_pairwise(recs)
    fl = per_topic_split_half(recs, n_iter=200)
    margins = {}
    lds = {}
    floors = {}
    for tl in TOPICS:
        margins[tl] = {}
        lds[tl] = {}
        floors[tl] = {}
        for pair, la, lb in PAIRS:
            l = p1.get(tl, {}).get(pair)
            f = fl.get(tl, {}).get(pair)
            if l is None or f is None:
                margins[tl][pair] = None
                continue
            lds[tl][pair] = l
            floors[tl][pair] = f
            margins[tl][pair] = round(l - f, 4)
    return {
        "n": len(recs),
        "n_per_language": counts,
        "lds": lds,
        "floors": floors,
        "margins": margins,
    }


def main() -> None:
    models = discover_models()
    valid = {m: info for m, info in models.items() if "error" not in info}
    print(f"  Discovered {len(models)} models; analyzing {len(valid)} complete")

    results = {}
    for m, info in sorted(valid.items()):
        r = analyze_model(info["units"])
        if "error" in r:
            continue
        results[m] = r

    # ── Aggregate: per-topic ZH-DE margin distribution across models ──
    agg = {}
    for tl in TOPICS:
        row = {}
        for pair in PAIR_ORDER:
            margins = [r["margins"][tl][pair] for r in results.values()
                       if r["margins"][tl].get(pair) is not None]
            row[pair] = {
                "n": len(margins),
                "n_positive": sum(1 for x in margins if x > 0),
                "n_positive_ge_0p02": sum(1 for x in margins if x >= 0.02),
                "n_negative": sum(1 for x in margins if x < 0),
                "median": round(percentile(margins, 0.5), 4),
                "p25": round(percentile(margins, 0.25), 4),
                "p75": round(percentile(margins, 0.75), 4),
                "min": round(min(margins), 4) if margins else None,
                "max": round(max(margins), 4) if margins else None,
            }
        agg[tl] = row

    # per-model topic consistency (ZH-DE): how many of 5 topics have positive margin
    topic_consistency = {}
    for m, r in results.items():
        pos = sum(1 for tl in TOPICS if (r["margins"][tl].get("ZH-DE") or 0) > 0)
        topic_consistency[m] = {"n_topics_positive_zhde": pos}
    dist = defaultdict(int)
    for m, v in topic_consistency.items():
        dist[v["n_topics_positive_zhde"]] += 1

    out = {
        "design": "r7_topic_x_model_margins",
        "generated_at": datetime.now().isoformat(),
        "n_models": len(results),
        "topics": TOPICS,
        "aggregate_per_topic": agg,
        "zhde_topic_consistency_dist": dict(sorted(dist.items())),
        "per_model": results,
    }
    out_path = OUT_DIR / "topic_model_margins_20260811.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}\n")

    print("=== Per-topic ZH-DE margin across models (51) ===")
    print(f"{'topic':<15s} {'n':>3s} {'pos%':>6s} {'>=.02%':>7s} {'neg%':>5s} {'median':>7s} {'min':>7s} {'max':>7s}")
    for tl in TOPICS:
        a = agg[tl]["ZH-DE"]
        print(f"{tl:<15s} {a['n']:>3d} {100*a['n_positive']/a['n']:>5.0f}% "
              f"{100*a['n_positive_ge_0p02']/a['n']:>6.0f}% {100*a['n_negative']/a['n']:>4.0f}% "
              f"{a['median']:>+7.3f} {a['min']:>+7.3f} {a['max']:>+7.3f}")
    print("\n=== Per-pair median margin across models (all topics pooled per model) ===")
    # recompute pooled pair margins for reference
    pooled = {pair: [] for pair in PAIR_ORDER}
    for m, r in results.items():
        for pair in PAIR_ORDER:
            vals = [r["margins"][tl][pair] for tl in TOPICS
                    if r["margins"][tl].get(pair) is not None]
            if vals:
                pooled[pair].append(statistics.mean(vals))
    for pair in PAIR_ORDER:
        v = pooled[pair]
        print(f"  {pair}: median={percentile(v,0.5):+.4f} "
              f"%pos={100*sum(1 for x in v if x>0)/len(v):.0f}%  n={len(v)}")
    print("\n=== ZH-DE topic-consistency distribution (# topics with positive margin) ===")
    for k in sorted(dist):
        print(f"  {k}/5 topics positive: {dist[k]} models")


if __name__ == "__main__":
    main()

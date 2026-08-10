#!/usr/bin/env python3
"""LinguaGraph — Multi-model replication of the LLM-as-Subject result.

Runs the SAME P1 within-subject protocol on several models and compares
LDS-C signal vs within-language floor across them. The core question:

  Is the cross-language value divergence (LDS-C >> floor, permutation p<0.01)
  a property of ONE model (deepseek-v4-flash) or a general property of
  multilingual LLMs? And does the cultural direction of divergence drivers
  (DE: autonomy/rules; ZH: space/boundary) replicate across providers?

Design: reuse the frozen pure functions (signal_table, label_permutation_null,
concept_freqs, concept_drivers) via import — this harness adds NO new metric
and does NOT modify the frozen pipeline. Subject files are auto-discovered by
their top-level "model" field, so the deepseek-v4-flash baseline
(llm_subject_20260808.json) and every replication model are compared on the
exact same code path.

Output: data/lds_c/llm_subject/multi_model_replication_<date>.json + console table.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_llm_analyze import OUT_DIR as LLM_OUT, unit_to_record  # noqa: E402
from lds_c_compute import PAIRS, label_permutation_null  # noqa: E402
from lds_c_design_effect import signal_table  # noqa: E402
from lds_c_divergence_drivers import concept_drivers, concept_freqs  # noqa: E402

BASELINE_MODEL = "deepseek-v4-flash"
TOP_DRIVERS = 10
MIN_UNITS_PER_LANG = 5  # require at least this many P1 samples/language to include a model


def discover_models() -> Dict[str, dict]:
    """llm_subject_*.json -> {model: {"path", "units"}}, latest file per model."""
    files = sorted(LLM_OUT.glob("llm_subject_*.json"))
    latest: Dict[str, dict] = {}
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"  [WARN] unreadable {f.name}, skipping")
            continue
        m = data.get("model", "unknown")
        # keep the latest-dated file per model (resume writes append in place,
        # but a re-run with a new date creates a second file)
        latest[m] = {"path": f, "units": data.get("units", [])}
    return latest


def p1_records(units: List[dict]) -> List[dict]:
    return [unit_to_record(u) for u in units if u.get("probe") == "P1"]


def lang_counts(records: List[dict]) -> Dict[str, int]:
    out = defaultdict(int)
    for r in records:
        out[r.get("language", "")] += 1
    return dict(out)


def driver_keys(drivers: List[dict], n: int = TOP_DRIVERS) -> List[str]:
    """Top-N driver keys as 'topic:key' (for cross-model overlap comparison)."""
    return [f"{d['topic']}:{d['key']}" for d in drivers[:n]]


def jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def analyze_model(model: str, units: List[dict], path: Path) -> dict:
    recs = p1_records(units)
    counts = lang_counts(recs)
    print(f"  {model}: {len(recs)} P1 records ({dict(counts)}) from {path.name}")

    if any(counts.get(l, 0) < MIN_UNITS_PER_LANG for l in ("zh", "de", "en")):
        return {"error": f"incomplete P1 data ({dict(counts)})", "n": len(recs)}

    sig = signal_table(recs, tag=model, n_floor=200)
    observed = {pair: sig["by_pair"][pair]["lds_c"]
                for pair, _, _ in PAIRS if pair in sig["by_pair"]}
    perm = label_permutation_null(recs, n_iter=500, observed=observed)

    freqs = concept_freqs(recs)
    # ZH-DE drivers: the cultural-pattern probe. driver dicts carry a "lang"
    # field = the language the concept is ONLY in (robust to arg order).
    drivers_zh_de = concept_drivers(freqs, "zh", "de")

    by_pair: dict = {}
    for pair, la, lb in PAIRS:
        if pair in sig["by_pair"]:
            b = sig["by_pair"][pair]
            by_pair[pair] = {
                "lds_c": b["lds_c"],
                "floor": b["split_half_floor"],
                "margin": b["signal_margin"],
                "ratio": b["signal_to_floor_ratio"],
                "perm_p": perm.get(pair, {}).get("perm_p_two_sided"),
            }

    return {
        "path": str(path),
        "n": len(recs),
        "n_per_language": counts,
        "by_pair": by_pair,
        "drivers_zh_de_top": drivers_zh_de[:TOP_DRIVERS],
        "drivers_zh_de_n": len(drivers_zh_de),
        "drivers_zh_de_direction": {
            "de_only": sum(1 for d in drivers_zh_de if d.get("lang") == "de"),
            "zh_only": sum(1 for d in drivers_zh_de if d.get("lang") == "zh"),
        },
    }


THRESHOLDS = [3, 5, 10, 20]
REPORT_THRESHOLD = 10  # above the random-agreement noise band (audit C2)


def direction_consistency(models: Dict[str, dict], min_models: int = 3,
                          n_null: int = 200) -> dict:
    """Cross-model agreement on the ZH-DE divergence DIRECTION, WITH a null
    model (audit C2).

    For every ZH-DE driver concept, count how many models mark it DE-only vs
    ZH-only. A concept is "direction-consistent" at threshold t if
    max(de_votes, zh_votes) >= t.

    Null model: fix each concept's total appearance frequency, assign every
    vote's direction at random (p=0.5), and count how many concepts would pass
    threshold t by chance. The >=3 count lies inside that noise band, so the
    reported headline uses >= REPORT_THRESHOLD votes where the observed count
    clearly exceeds the null.
    """
    import random
    from collections import Counter, defaultdict

    de_votes: Dict[tuple, Counter] = defaultdict(Counter)
    zh_votes: Dict[tuple, Counter] = defaultdict(Counter)
    voting_models = []
    for model, info in models.items():
        recs = p1_records(info["units"])
        if any(lang_counts(recs).get(l, 0) < MIN_UNITS_PER_LANG for l in ("zh", "de", "en")):
            continue
        voting_models.append(model)
        freqs = concept_freqs(recs)
        for d in concept_drivers(freqs, "zh", "de"):
            key = (d["topic"], d["key"])
            if d.get("lang") == "de":
                de_votes[key][model] += 1
            elif d.get("lang") == "zh":
                zh_votes[key][model] += 1

    # Convert to PLAIN dicts (materialized) to eliminate any defaultdict
    # creation-during-iteration risk in the steps below.
    de_votes = {k: dict(v) for k, v in de_votes.items()}
    zh_votes = {k: dict(v) for k, v in zh_votes.items()}
    totals = {k: (len(de_votes.get(k, {})), len(zh_votes.get(k, {})))
              for k in set(de_votes) | set(zh_votes)}

    def count_consistent(assign):
        return {t: sum(1 for (d, z) in assign.values() if max(d, z) >= t)
                for t in THRESHOLDS}

    observed = count_consistent(totals)

    # Null: random side for each vote, fixed total per concept
    rng = random.Random(20260810)
    null_draws = {t: [] for t in THRESHOLDS}
    for _ in range(n_null):
        draw = {}
        for key, (d, z) in totals.items():
            n = d + z
            d_rand = sum(1 for _ in range(n) if rng.random() < 0.5)
            draw[key] = (d_rand, n - d_rand)
        c = count_consistent(draw)
        for t in THRESHOLDS:
            null_draws[t].append(c[t])
    obs_vs_null = {}
    for t in THRESHOLDS:
        arr = sorted(null_draws[t])
        mean = sum(arr) / len(arr)
        sd = (sum((x - mean) ** 2 for x in arr) / len(arr)) ** 0.5
        p_ge = sum(1 for x in arr if x >= observed[t]) / len(arr)
        obs_vs_null[str(t)] = {
            "observed": observed[t], "null_mean": round(mean, 1),
            "null_sd": round(sd, 1), "p_null_ge_observed": round(p_ge, 3),
        }

    # Concepts with >= REPORT_THRESHOLD votes on a side, as (de, zh) counts
    # (may overlap: a concept with both de>=10 and zh>=10 appears in both).
    # The REPORT count below is the UNIQUE max-based count (204, not 207).
    # NB: use .get() on the defaultdicts so a missing side does not create a
    # key while iterating (RuntimeError).
    top_de = sorted(
        ((f"{t}:{k}", (len(de_votes[(t, k)]), len(zh_votes.get((t, k), {}))))
         for (t, k) in list(de_votes)
         if len(de_votes[(t, k)]) >= REPORT_THRESHOLD),
        key=lambda x: -max(x[1]))
    top_zh = sorted(
        ((f"{t}:{k}", (len(de_votes.get((t, k), {})), len(zh_votes[(t, k)])))
         for (t, k) in list(zh_votes)
         if len(zh_votes[(t, k)]) >= REPORT_THRESHOLD),
        key=lambda x: -max(x[1]))

    return {
        "report_threshold": REPORT_THRESHOLD,
        "n_models_voting": len(voting_models),
        "n_models_unique": len({m.split(":")[-1] for m in voting_models}),
        "n_concepts_drivers": len(totals),
        "observed_vs_null": obs_vs_null,
        "de_only_strong": top_de[:TOP_DRIVERS],
        "zh_only_strong": top_zh[:TOP_DRIVERS],
        "n_consistent_at_report_threshold": sum(
            1 for (d, z) in totals.values() if max(d, z) >= REPORT_THRESHOLD),
        "readme": (
            "Direction-consistent concepts at threshold t = max(DE-only, ZH-only) "
            "votes. Null model fixes per-concept appearance frequency and assigns "
            "direction at random (p=0.5); the >=3 count lies inside that noise "
            "band (audit C2), so the report threshold is >=10 votes where the "
            "observed count exceeds the null. n_consistent_at_report_threshold is "
            "the UNIQUE concept count (max-based), not the sum of the de/zh lists."
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Multi-model replication of LLM-as-Subject")
    ap.add_argument("--baseline", type=str, default=BASELINE_MODEL)
    ap.add_argument("--drivers", type=int, default=TOP_DRIVERS)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    models = discover_models()
    if not models:
        print("ERROR: no llm_subject_*.json found"); sys.exit(1)
    print(f"  Discovered models: {sorted(models)}")

    results: Dict[str, dict] = {}
    for model, info in sorted(models.items()):
        results[model] = analyze_model(model, info["units"], info["path"])

    # ── Cross-model comparison ───────────────────────────────────────
    baseline = args.baseline if args.baseline in results else next(iter(results), None)
    if baseline not in results:
        print(f"  [WARN] baseline {args.baseline} not found; using {baseline}")
    bkeys = driver_keys(results[baseline].get("drivers_zh_de_top", [])) if baseline in results else []

    comparison = {
        "baseline": baseline,
        "per_pair": {},
        "driver_consistency_vs_baseline": {},
        "readme": (
            "driver_consistency = Jaccard over top-N ZH-DE driver keys "
            "between this model and the baseline (deepseek-v4-flash). "
            "High overlap => the cultural direction (DE autonomy / ZH space) "
            "replicates across models, not a single-model artifact."
        ),
    }
    for pair, _, _ in PAIRS:
        row = {"lds_c": {}, "floor": {}, "margin": {}, "perm_p": {}}
        for model, r in results.items():
            if "by_pair" in r and pair in r["by_pair"]:
                b = r["by_pair"][pair]
                row["lds_c"][model] = b["lds_c"]
                row["floor"][model] = b["floor"]
                row["margin"][model] = b["margin"]
                row["perm_p"][model] = b["perm_p"]
        if row["lds_c"]:
            comparison["per_pair"][pair] = row

    for model, r in results.items():
        if model == baseline or "error" in r:
            continue
        mkeys = driver_keys(r.get("drivers_zh_de_top", []))
        comparison["driver_consistency_vs_baseline"][model] = {
            "zh_de_driver_jaccard_top%d" % args.drivers: round(jaccard(bkeys, mkeys), 4),
            "n_baseline_drivers": len(bkeys),
            "n_model_drivers": len(mkeys),
        }

    comparison["direction_consistency"] = direction_consistency(models)

    out = {
        "generated_at": datetime.now().isoformat(),
        "design": "multi_model_replication_P1",
        "k": None,  # filled from subject files' metadata if available
        "baseline_model": baseline,
        "models": results,
        "comparison": comparison,
    }

    out_path = LLM_OUT / (args.out or f"multi_model_replication_{datetime.now().strftime('%Y%m%d')}.json")
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")

    # ── Console comparison table ─────────────────────────────────────
    print("\n=== Cross-language signal: LDS-C | margin (LDS-C - floor) ===\n")
    for pair, _, _ in PAIRS:
        if pair not in comparison["per_pair"]:
            continue
        print(f"  {pair}:")
        for model, r in results.items():
            if "by_pair" not in r or pair not in r["by_pair"]:
                continue
            b = r["by_pair"][pair]
            flag = "  << SIGNAL" if b["margin"] > 0.03 else ""
            print(f"    {model:<18} LDS-C={b['lds_c']:<7} floor={b['floor']:<7} "
                  f"margin={b['margin']:<7} p={b['perm_p']}{flag}")
        print()

    if comparison["driver_consistency_vs_baseline"]:
        print("=== ZH-DE driver consistency vs baseline ===\n")
        for model, d in comparison["driver_consistency_vs_baseline"].items():
            print(f"  {model:<18} {d}")

    dc = comparison.get("direction_consistency", {})
    nv = dc.get("n_models_voting", "?")
    print(f"\n=== ZH-DE direction consistency (>= {dc.get('report_threshold','?')} "
          f"votes; {nv} voting models) ===\n")
    print(f"  {dc.get('n_consistent_at_report_threshold', 0)} concepts consistent at threshold")
    ovn = dc.get("observed_vs_null", {})
    for t in THRESHOLDS:
        r = ovn.get(str(t), {})
        print(f"  t>={t}: observed {r.get('observed')} vs null "
              f"{r.get('null_mean')}±{r.get('null_sd')} (p_null_ge={r.get('p_null_ge_observed')})")
    de_c = dc.get("de_only_strong", [])[:6]
    zh_c = dc.get("zh_only_strong", [])[:6]
    print(f"  Strongest DE (concept, (de,zh) votes): {de_c}")
    print(f"  Strongest ZH (concept, (de,zh) votes): {zh_c}")

    print("\n=== ZH-DE top-5 drivers per model (cultural pattern) ===\n")
    for model, r in results.items():
        if "error" in r or not r.get("drivers_zh_de_top"):
            continue
        print(f"  {model}:")
        for d in r["drivers_zh_de_top"][:5]:
            side = "DE-only" if d.get("lang") == "de" else "ZH-only"
            print(f"    [{side:7}] {d['topic']:<14} {d['key']:<40} "
                  f"freq={d.get('freq_a') or d.get('freq_b')}")


if __name__ == "__main__":
    main()

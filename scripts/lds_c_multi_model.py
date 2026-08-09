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


def direction_consistency(models: Dict[str, dict], min_models: int = 3) -> dict:
    """Cross-model agreement on the ZH-DE divergence DIRECTION.

    For every ZH-DE driver concept, count how many models mark it DE-only vs
    ZH-only. A concept is "direction-consistent" if >= min_models agree on the
    same side. The top-10 Jaccard is too strict (frequency rank varies by model);
    this vote-based measure captures that the DIRECTION of specific recurring
    concepts is stable across independent providers.
    """
    from collections import Counter, defaultdict

    de_votes: Dict[tuple, Counter] = defaultdict(Counter)
    zh_votes: Dict[tuple, Counter] = defaultdict(Counter)
    for model, info in models.items():
        recs = p1_records(info["units"])
        if any(lang_counts(recs).get(l, 0) < MIN_UNITS_PER_LANG for l in ("zh", "de", "en")):
            continue
        freqs = concept_freqs(recs)
        for d in concept_drivers(freqs, "zh", "de"):
            key = (d["topic"], d["key"])
            if d.get("lang") == "de":
                de_votes[key][model] += 1
            elif d.get("lang") == "zh":
                zh_votes[key][model] += 1
    consistent_de = {f"{t}:{k}": len(ms) for (t, k), ms in de_votes.items() if len(ms) >= min_models}
    consistent_zh = {f"{t}:{k}": len(ms) for (t, k), ms in zh_votes.items() if len(ms) >= min_models}
    return {
        "min_models": min_models,
        "n_models": len(models),
        "de_only_consistent": dict(sorted(consistent_de.items(), key=lambda x: -x[1])),
        "zh_only_consistent": dict(sorted(consistent_zh.items(), key=lambda x: -x[1])),
        "n_consistent_total": len(consistent_de) + len(consistent_zh),
        "readme": (
            "concepts where >=min_models independently mark the SAME direction "
            "(DE-only or ZH-only) in the ZH-DE divergence. High agreement => the "
            "cultural direction (DE autonomy/rules, ZH relational/space) is a "
            "robust property across providers, not a single-model artifact."
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
    n_models = dc.get("n_models", "?")
    print(f"\n=== ZH-DE direction consistency (>= {dc.get('min_models','?')}/{n_models} models) ===\n")
    print(f"  {dc.get('n_consistent_total', 0)} concepts with consistent direction")
    de_c = list(dc.get("de_only_consistent", {}))[:6]
    zh_c = list(dc.get("zh_only_consistent", {}))[:6]
    print(f"  DE-only examples: {de_c}")
    print(f"  ZH-only examples: {zh_c}")

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

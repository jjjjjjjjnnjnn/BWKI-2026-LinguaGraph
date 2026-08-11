#!/usr/bin/env python3
"""LinguaGraph — R2: mechanism of the English-pair null result.

Research-forward review (2026-08-11), G2. 8 of 153 language-pair tests are
non-significant, ALL involving English (2 ZH-EN, 6 DE-EN), 6/8 from the
DeepSeek-R1/Distill family. The paper reports this as a fact but offers no
mechanism. This script tests three mutually-exclusive hypotheses on the
existing 51-model data (zero new API calls):

  H_floor : EN has a HIGHER within-language floor (EN samples more
            heterogeneous/sparse) -> margin small even with normal signal.
  H_bridge: EN is a "bridge": its concept space overlaps BOTH DE and ZH more
            than DE-ZH overlap each other -> cross-EN LDS is low.
  H_r1    : the effect is specific to DeepSeek-R1/Distill decoding, not a
            general EN property.

Per model, computes: per-language aggregate set size (richness), per-language
within-language split-half floor, pairwise aggregate Jaccard J(DE,EN)/J(ZH,EN)/
J(DE,ZH), and per-pair margins (from the authoritative replication).

Output: data/lds_c/llm_subject/en_null_mechanism_20260811.json + console.
"""

from __future__ import annotations

import json
import random
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import RANDOM_SEED, canonical_key, lds_concept  # noqa: E402
from lds_c_llm_analyze import OUT_DIR  # noqa: E402
from lds_c_multi_model import MIN_UNITS_PER_LANG, discover_models, p1_records, lang_counts  # noqa: E402

PAIRS = [("ZH-EN", "zh", "en"), ("DE-EN", "de", "en"), ("ZH-DE", "zh", "de")]

# 8 non-significant PAIRS across 7 models (perm_p >= 0.05 on an EN pair),
# verified 2026-08-11; deepseek-r1-distill-qwen-7b is NS on both EN pairs.
NS_MODELS = {
    "dashscope:deepseek-r1", "dashscope:deepseek-r1-0528",
    "dashscope:deepseek-r1-distill-qwen-14b", "dashscope:deepseek-r1-distill-qwen-32b",
    "dashscope:deepseek-r1-distill-qwen-7b", "dashscope:glm-4.6",
    "dashscope:qwen3-235b-a22b",
}
R1_FAMILY = ("dashscope:deepseek-r1",)


def _concept_keys(record: dict) -> set:
    out = set()
    for t in record.get("topics", []):
        for c in t.get("concepts", []):
            k = canonical_key(c.get("en", ""))
            if k:
                out.add(k)
    return out


def lang_set(records: list, lang: str) -> set:
    out = set()
    for r in records:
        if r.get("language", "") == lang:
            out |= _concept_keys(r)
    return out


def lang_floor(records: list, lang: str, n_iter: int = 200) -> float:
    reps = [r for r in records if r.get("language", "") == lang]
    if len(reps) < 2:
        return float("nan")
    rng = random.Random(RANDOM_SEED + 77)
    vals = []
    for _ in range(n_iter):
        rng.shuffle(reps)
        half = len(reps) // 2
        a = set()
        b = set()
        for r in reps[:half]:
            a |= _concept_keys(r)
        for r in reps[half:]:
            b |= _concept_keys(r)
        if a and b:
            vals.append(lds_concept(a, b))
    return statistics.mean(vals) if vals else float("nan")


def jaccard(a: set, b: set):
    u = a | b
    return len(a & b) / len(u) if u else float("nan")


def analyze(units) -> dict:
    recs = p1_records(units)
    counts = lang_counts(recs)
    if any(counts.get(l, 0) < MIN_UNITS_PER_LANG for l in ("zh", "de", "en")):
        return None
    sets = {l: lang_set(recs, l) for l in ("zh", "de", "en")}
    floors = {l: lang_floor(recs, l) for l in ("zh", "de", "en")}
    out = {
        "n_per_language": counts,
        "set_size": {l: len(s) for l, s in sets.items()},
        "within_lang_floor": floors,
        "jaccard": {
            "DE-EN": round(jaccard(sets["de"], sets["en"]), 4),
            "ZH-EN": round(jaccard(sets["zh"], sets["en"]), 4),
            "ZH-DE": round(jaccard(sets["zh"], sets["de"]), 4),
        },
    }
    return out


def _sum(rows, key, sub=None):
    vals = []
    for r in rows:
        v = r.get(key) if sub is None else (r.get(key) or {}).get(sub)
        if v is not None and v == v:
            vals.append(v)
    return vals


def _mean(vals):
    return statistics.mean(vals) if vals else float("nan")


def main() -> None:
    models = discover_models()
    # authoritative margins/perm_p from the replication JSON
    rep = json.loads(
        (OUT_DIR / "multi_model_replication_20260810.json").read_text(encoding="utf-8"))
    rep_models = rep.get("models", {})

    rows = {}
    for m, info in sorted(models.items()):
        a = analyze(info["units"])
        if a is None:
            continue
        a["model"] = m
        a["is_r1"] = any(m.startswith(p) for p in R1_FAMILY)
        # per-pair perm_p / margin from replication (authoritative)
        rp = rep_models.get(m, {})
        a["per_pair"] = {}
        for pair, _, _ in PAIRS:
            b = (rp.get("by_pair") or {}).get(pair, {})
            a["per_pair"][pair] = {
                "margin": b.get("margin"),
                "perm_p": b.get("perm_p"),
            }
        a["any_ns"] = any((a["per_pair"][p].get("perm_p") or 0) >= 0.05
                          for p, _, _ in PAIRS)
        rows[m] = a

    ns = [r for r in rows.values() if r["any_ns"]]
    sig = [r for r in rows.values() if not r["any_ns"]]
    print(f"  models: total={len(rows)}  NS-EN={len(ns)}  all-sig={len(sig)}\n")

    # ── Group comparison table ──
    keys_floor = ["zh", "de", "en"]
    keys_jac = ["DE-EN", "ZH-EN", "ZH-DE"]
    def col_rows(group, key, sub):
        return [g.get(key, {}).get(sub) for g in group if g.get(key, {}).get(sub) is not None]
    def fmt(v):
        return f"{v:+.4f}" if v is not None else "  n/a"

    print("  ── within-language floor (higher = more within-language divergence) ──")
    print(f"  {'metric':<14s} {'NS-EN mean':>10s} {'Sig mean':>10s} {'NS-Sig':>9s}")
    for sub in keys_floor:
        vn, vs = _mean(col_rows(ns, "within_lang_floor", sub)), _mean(col_rows(sig, "within_lang_floor", sub))
        print(f"  floor_{sub:<9s} {fmt(vn):>10s} {fmt(vs):>10s} {fmt(vn-vs):>9s}")

    print(f"\n  ── aggregate set size (richness) ──")
    print(f"  {'metric':<14s} {'NS-EN mean':>10s} {'Sig mean':>10s}")
    for sub in keys_floor:
        vn, vs = _mean(col_rows(ns, "set_size", sub)), _mean(col_rows(sig, "set_size", sub))
        print(f"  |set_{sub}|{'':<6s} {vn:>10.1f} {vs:>10.1f}")

    print(f"\n  ── cross-language aggregate Jaccard (higher = more similar) ──")
    print(f"  {'metric':<14s} {'NS-EN mean':>10s} {'Sig mean':>10s} {'NS-Sig':>9s}")
    for sub in keys_jac:
        vn, vs = _mean(col_rows(ns, "jaccard", sub)), _mean(col_rows(sig, "jaccard", sub))
        print(f"  J{sub:<9s} {fmt(vn):>10s} {fmt(vs):>10s} {fmt(vn-vs):>9s}")

    print(f"\n  ── per-pair margin (replication authoritative) ──")
    for pair, _, _ in PAIRS:
        vn = _mean([g.get("per_pair", {}).get(pair, {}).get("margin")
                    for g in ns if g.get("per_pair", {}).get(pair, {}).get("margin") is not None])
        vs = _mean([g.get("per_pair", {}).get(pair, {}).get("margin")
                    for g in sig if g.get("per_pair", {}).get(pair, {}).get("margin") is not None])
        print(f"  margin[{pair}]  {fmt(vn):>10s} {fmt(vs):>10s} {fmt(vn-vs):>9s}")

    # ── R1 vs non-R1 within the NS group ──
    print(f"\n  ── NS group composition ──")
    r1_in_ns = [r for r in ns if r["is_r1"]]
    print(f"  NS-EN models: {len(ns)}  (R1-family: {len(r1_in_ns)})")
    for r in sorted(ns, key=lambda x: x["model"]):
        ns_pairs = [p for p, _, _ in PAIRS if (r["per_pair"][p].get("perm_p") or 0) >= 0.05]
        print(f"    {r['model']:<42s} NS pairs={ns_pairs} "
              f"ENsize={r['set_size']['en']} floor_en={r['within_lang_floor']['en']:.3f} "
              f"J(DE,EN)={r['jaccard']['DE-EN']:.3f} J(ZH,EN)={r['jaccard']['ZH-EN']:.3f}")

    out = {
        "design": "r2_en_null_mechanism",
        "generated_at": datetime.now().isoformat(),
        "n_models": len(rows),
        "ns_models": sorted(r["model"] for r in ns),
        "group_means": {
            "within_lang_floor": {
                sub: {"ns": round(_mean(col_rows(ns, "within_lang_floor", sub)), 4),
                      "sig": round(_mean(col_rows(sig, "within_lang_floor", sub)), 4)}
                for sub in keys_floor},
            "set_size": {
                sub: {"ns": round(_mean(col_rows(ns, "set_size", sub)), 4),
                      "sig": round(_mean(col_rows(sig, "set_size", sub)), 4)}
                for sub in keys_floor},
            "jaccard": {
                sub: {"ns": round(_mean(col_rows(ns, "jaccard", sub)), 4),
                      "sig": round(_mean(col_rows(sig, "jaccard", sub)), 4)}
                for sub in keys_jac},
            "per_pair_margin": {
                pair: {"ns": round(_mean([g.get("per_pair", {}).get(pair, {}).get("margin")
                                          for g in ns
                                          if g.get("per_pair", {}).get(pair, {}).get("margin") is not None]), 4),
                       "sig": round(_mean([g.get("per_pair", {}).get(pair, {}).get("margin")
                                           for g in sig
                                           if g.get("per_pair", {}).get(pair, {}).get("margin") is not None]), 4)}
                for pair, _, _ in PAIRS},
        },
        "per_model": rows,
    }
    out_path = OUT_DIR / "en_null_mechanism_20260811.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()

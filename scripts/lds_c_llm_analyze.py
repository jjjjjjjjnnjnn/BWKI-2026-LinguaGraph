#!/usr/bin/env python3
"""LinguaGraph — D1: LLM-as-Subject mechanism analysis.

Consumes scripts/lds_c_llm_subject.py output (data/lds_c/llm_subject/llm_subject_*.json)
and produces the mechanism-decomposition results:

  P1  language main effect : LDS-C(zh-de/en) vs within-lang split-half floor
                             vs label permutation (reuses lds_c_compute nulls)
  P2  frame-code decoupling: same code (zh), natural vs DE-frame; and DE side.
                             If natural-vs-cross-frame LDS > split-half floor,
                             cultural frame drives divergence independently of code.
  P3  free association (M2) : association-set divergence across languages,
                             compared to P1 concept divergence (statistical mechanism).
  P5  answer-vs-prompt lang : concept divergence when prompt lang fixed, answer lang
                             varied, and vice versa.

Output: data/lds_c/llm_subject/analysis_<date>.json + console summary.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import (  # noqa: E402
    PAIRS,
    RANDOM_SEED,
    TOPICS,
    aggregate_languages,
    bootstrap_ci,
    canonical_key,
    compute_pairwise,
    label_permutation_null,
    lds_concept,
    within_language_split_half,
)

OUT_DIR = PROJECT_ROOT / "data" / "lds_c" / "llm_subject"


# ── Load ────────────────────────────────────────────────────────────
def latest_units() -> List[dict]:
    files = sorted(OUT_DIR.glob("llm_subject_*.json"))
    if not files:
        raise FileNotFoundError(f"No collection files in {OUT_DIR}")
    data = json.loads(files[-1].read_text(encoding="utf-8"))
    units = data.get("units", [])
    print(f"  Loaded {len(units)} units from {files[-1].name}")
    print(f"  Probes: {dict(Counter(u['probe'] for u in units))}")
    return units


def unit_to_record(unit: dict) -> dict:
    """Convert a P1/P2/P5 unit to an lds_c_compute-compatible record."""
    topics = [
        {"topic": t, "concepts": concepts}
        for t, concepts in unit.get("concepts", {}).items()
    ]
    return {
        "response_id": unit["unit_id"],
        "language": unit["language"],
        "probe": unit["probe"],
        "frame": unit.get("frame", "natural"),
        "prompt_lang": unit.get("prompt_lang", unit["language"]),
        "sample": unit.get("sample", 0),
        "topics": topics,
    }


def unit_to_assoc_record(unit: dict, gloss_map: Optional[Dict[str, str]] = None) -> dict:
    """Convert a P3 unit to a record; associations become 'concepts'.

    gloss_map maps source-language word -> English gloss (from the P3 glossing
    post-pass). If provided, concepts use the English gloss as 'en' so the
    association LDS is computed in the same canonical key space as concept
    graphs (otherwise ZH associations have no Latin tokens and canonicalize
    to empty keys)."""
    concepts = []
    for w in unit.get("associations", []):
        w = w.strip()
        if not w:
            continue
        en = (gloss_map or {}).get(w, w)
        concepts.append({"en": en, "concept": w, "importance": 1.0})
    return {
        "response_id": unit["unit_id"],
        "language": unit["language"],
        "probe": "P3",
        "topic": unit.get("topic"),
        "sample": unit.get("sample", 0),
        "topics": [{"topic": "ALL", "concepts": concepts}],
    }


def load_assoc_gloss() -> Dict[str, str]:
    """Load the P3 gloss map {word -> en} from the glossing post-pass."""
    files = sorted(OUT_DIR.glob("assoc_gloss_*.json"))
    if not files:
        return {}
    data = json.loads(files[-1].read_text(encoding="utf-8"))
    m: Dict[str, str] = {}
    for c in data.get("cells", []):
        for w, en in c.get("glosses", {}).items():
            m[w] = en
    print(f"  Loaded {len(m)} association glosses from {files[-1].name}")
    return m


# ── P1: language main effect ────────────────────────────────────────
def analyze_p1(records: List[dict]) -> dict:
    by_lang = defaultdict(list)
    for r in records:
        by_lang[r["language"]].append(r)

    agg = aggregate_languages(records)
    pairwise = compute_pairwise(agg)
    lds_pooled = {pair: pairwise[pair]["ALL"] for pair in PAIRS if pair in pairwise}

    ci = bootstrap_ci(records, n_iter=1000)
    floors = within_language_split_half(records, n_iter=200)
    perm = label_permutation_null(records, n_iter=500)

    out = {"n": {lang: len(reps) for lang, reps in by_lang.items()}}
    for pair in PAIRS:
        la, lb = pair.split("-")
        if la in by_lang and lb in by_lang:
            out[pair] = {
                "lds_c_pooled": round(lds_pooled.get(pair, float("nan")), 4),
                "ci": ci.get(pair, {}),
                "split_half_floor": floors.get(pair, None),
                "label_perm_mean": round(perm.get(pair, {}).get("mean", float("nan")), 4)
                    if pair in perm else None,
                "label_perm_p_lt": perm.get(pair, {}).get("p_lt", None),
            }
    out["interpretation"] = (
        "LDS-C ~ split-half floor => language carries no separable signal "
        "(participant-equivalent variability); LDS-C >> floor => language effect."
    )
    return out


# ── P2: frame-code decoupling ───────────────────────────────────────
def analyze_p2(records: List[dict]) -> dict:
    """Compare natural vs cross-frame within the same code language.

    For code=zh: natural ZH (frame=natural) vs ZH-code+DE-frame.
    A non-zero LDS between these (relative to the within-language split-half
    floor of P1 zh) means the cultural frame changes concept structure
    independently of the language code.
    """
    out: dict = {}
    for code in ["zh", "de"]:
        natural = [r for r in records
                   if r["language"] == code and r["probe"] == "P1" and r["frame"] == "natural"]
        other = code == "zh" and "de" or "zh"  # opposite frame code
        crossed = [r for r in records
                   if r["language"] == code and r["probe"] == "P2" and r["frame"] == other]
        if not natural or not crossed:
            out[code] = {"error": f"missing units (natural={len(natural)}, crossed={len(crossed)})"}
            continue

        agg_nat = aggregate_languages(natural)
        agg_cross = aggregate_languages(crossed)
        lds = lds_concept(agg_nat.get(code, {}).get("ALL", set()),
                          agg_cross.get(code, {}).get("ALL", set()))

        # bootstrap CI on the frame effect
        random_seed_local = RANDOM_SEED
        import random
        rng = random.Random(random_seed_local + 7)
        vals = []
        for _ in range(500):
            sa = [rng.choice(natural) for _ in natural]
            sb = [rng.choice(crossed) for _ in crossed]
            aa = aggregate_languages(sa)
            ab = aggregate_languages(sb)
            vals.append(lds_concept(aa.get(code, {}).get("ALL", set()),
                                    ab.get(code, {}).get("ALL", set())))
        vals.sort()
        out[code] = {
            "code": code, "frame_cross": other,
            "n_natural": len(natural), "n_crossed": len(crossed),
            "lds_natural_vs_crossframe": round(lds, 4),
            "ci_95": [round(vals[int(0.025 * len(vals))], 4),
                      round(vals[int(0.975 * len(vals))], 4)],
        }
    out["interpretation"] = (
        "natural-vs-cross-frame LDS >> within-lang split-half floor => cultural "
        "frame drives concept divergence independently of language code (M3)."
    )
    return out


# ── P3: free-association (M2 statistical mechanism) ────────────────
def analyze_p3(assoc_records: List[dict], p1_lds: dict) -> dict:
    """Association-set divergence across languages (pooled per language), compared
    to P1 concept divergence. Associations are raw words in the source language;
    canonical_key normalizes them per language, and cross-language comparison uses
    the same canonical English-gloss key space (associations stored as en=word)."""
    by_lang = defaultdict(list)
    for r in assoc_records:
        by_lang[r["language"]].append(r)

    agg = aggregate_languages(assoc_records)
    pairwise = compute_pairwise(agg)
    assoc_lds = {pair: round(pairwise[pair]["ALL"], 4) for pair in PAIRS if pair in pairwise}

    # within-language association split-half (association sampling noise floor)
    floors = within_language_split_half(assoc_records, n_iter=200)

    out = {"n": {lang: len(reps) for lang, reps in by_lang.items()},
           "assoc_lds_pooled": assoc_lds,
           "assoc_split_half_floor": floors}
    for pair in PAIRS:
        if pair in assoc_lds and pair in p1_lds:
            out[pair] = {
                "assoc_lds": assoc_lds[pair],
                "concept_lds_p1": p1_lds.get(pair),
                "delta": round(assoc_lds[pair] - (p1_lds.get(pair) or 0), 4),
            }
    out["interpretation"] = (
        "assoc_lds ~ concept_lds => concept divergence is association-statistics "
        "driven (M2); concept_lds >> assoc_lds => structural layer beyond statistics."
    )
    return out


# ── P5: answer-vs-prompt language ───────────────────────────────────
def analyze_p5(records: List[dict]) -> dict:
    """Fix answer language (de), vary prompt language (zh vs de). If LDS > floor,
    the prompt/question language influences concept structure even when the
    answer language is held constant (M5: instruction-conditioning layer)."""
    deq_dea = [r for r in records if r["probe"] == "P5" and r["prompt_lang"] == "de"]
    zhq_dea = [r for r in records if r["probe"] == "P5" and r["prompt_lang"] == "zh"]
    if not deq_dea or not zhq_dea:
        return {"error": f"missing P5 units (deq={len(deq_dea)}, zhq={len(zhq_dea)})"}

    agg_deq = aggregate_languages(deq_dea)
    agg_zhq = aggregate_languages(zhq_dea)
    lds = lds_concept(agg_deq.get("de", {}).get("ALL", set()),
                      agg_zhq.get("de", {}).get("ALL", set()))

    import random
    rng = random.Random(RANDOM_SEED + 11)
    vals = []
    for _ in range(500):
        sa = [rng.choice(deq_dea) for _ in deq_dea]
        sb = [rng.choice(zhq_dea) for _ in zhq_dea]
        aa = aggregate_languages(sa)
        ab = aggregate_languages(sb)
        vals.append(lds_concept(aa.get("de", {}).get("ALL", set()),
                                ab.get("de", {}).get("ALL", set())))
    vals.sort()
    return {
        "n": {"deq_dea": len(deq_dea), "zhq_dea": len(zhq_dea)},
        "lds_prompt_de_vs_zh_answering_de": round(lds, 4),
        "ci_95": [round(vals[int(0.025 * len(vals))], 4),
                  round(vals[int(0.975 * len(vals))], 4)],
        "interpretation": (
            "> split-half floor => question language shapes concepts even when "
            "answer language is fixed (M5); ~0 => answer language dominates."
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="D1 mechanism analysis")
    ap.add_argument("--in", dest="in_file", type=str, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    units = json.loads(Path(args.in_file).read_text(encoding="utf-8"))["units"] \
        if args.in_file else latest_units()

    p1_records = [unit_to_record(u) for u in units if u["probe"] == "P1"]
    p2_records = [unit_to_record(u) for u in units if u["probe"] in ("P1", "P2")]
    p5_records = [unit_to_record(u) for u in units if u["probe"] == "P5"]
    p3_units = [u for u in units if u["probe"] == "P3"]

    # For M2 comparability, P3 associations must be glossed to English (canonical
    # key space). If the glossing post-pass hasn't run yet, warn loudly.
    gloss = load_assoc_gloss()
    p3_records = [unit_to_assoc_record(u, gloss) for u in p3_units]
    if p3_records and gloss:
        unglossed = sum(1 for u in p3_units for w in u.get("associations", [])
                        if w.strip() and w.strip() not in gloss)
        if unglossed:
            print(f"  WARN: {unglossed} association words have no gloss "
                  f"(run scripts/lds_c_llm_gloss_assoc.py)")

    print(f"  P1 records: {len(p1_records)} | P2: {len(p2_records)} | "
          f"P3: {len(p3_records)} | P5: {len(p5_records)}")

    result: dict = {"design": "d1_mechanism", "generated_at": datetime.now().isoformat()}

    if p1_records:
        print("  Analyzing P1 (language main effect)...")
        result["P1_language_main_effect"] = analyze_p1(p1_records)

    if p2_records:
        print("  Analyzing P2 (frame-code decoupling)...")
        result["P2_frame_code_decoupling"] = analyze_p2(p2_records)

    p1_lds = {pair: result["P1_language_main_effect"][pair]["lds_c_pooled"]
              for pair in PAIRS if pair in result.get("P1_language_main_effect", {})
              and "lds_c_pooled" in result["P1_language_main_effect"][pair]}

    if p3_records and p1_lds:
        print("  Analyzing P3 (free association / M2)...")
        result["P3_free_association_M2"] = analyze_p3(p3_records, p1_lds)

    if p5_records:
        print("  Analyzing P5 (answer-vs-prompt language)...")
        result["P5_answer_vs_prompt"] = analyze_p5(p5_records)

    out_path = OUT_DIR / (args.out or f"analysis_{datetime.now().strftime('%Y%m%d')}.json")
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")
    print("\n=== P1 ===")
    if "P1_language_main_effect" in result:
        for pair in PAIRS:
            if pair in result["P1_language_main_effect"]:
                print(f"  {pair}: {json.dumps(result['P1_language_main_effect'][pair], ensure_ascii=False)}")
    print("\n=== P2 ===")
    if "P2_frame_code_decoupling" in result:
        for k, v in result["P2_frame_code_decoupling"].items():
            print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
    print("\n=== P3 ===")
    if "P3_free_association_M2" in result:
        for pair in PAIRS:
            if pair in result["P3_free_association_M2"]:
                print(f"  {pair}: {json.dumps(result['P3_free_association_M2'][pair], ensure_ascii=False)}")
    print("\n=== P5 ===")
    if "P5_answer_vs_prompt" in result:
        print(f"  {json.dumps(result['P5_answer_vs_prompt'], ensure_ascii=False)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""LinguaGraph — D1: per-topic mechanism decomposition.

Decomposes the D1 mechanism results by the 5 canonical topics:
  For each topic t:
    P1_lds[t][pair]      : LDS-C across languages on topic t (pooled over k samples)
    P1_floor[t][pair]    : within-language split-half floor on topic t
    P2_frame[t][code]    : natural vs cross-frame LDS on topic t
    P3_assoc[t][pair]    : association-set LDS on topic t (glossed, M2)
    P3_assoc_floor[t]    : within-language association floor on topic t

Answers: WHICH topics drive the language signal / the frame effect? Is ZH-DE's
structural layer concentrated in specific topics?

Output: data/lds_c/llm_subject/per_topic_<date>.json + console table.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
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
    canonical_key,
    lds_concept,
)

from lds_c_llm_analyze import (  # noqa: E402
    OUT_DIR,
    load_assoc_gloss,
    unit_to_assoc_record,
    unit_to_record,
)

CATEGORIES = ["Legal/Institutional", "Individual/Autonomy", "Material/Concrete",
              "Social/Relational", "Moral/Abstract", "Emotional/Affective"]


# ── Per-topic helpers ───────────────────────────────────────────────
def response_topic_groups(record: dict, topic: str) -> set:
    """Canonical keys for ONE topic of one record."""
    out = set()
    for t in record.get("topics", []):
        if t.get("topic", "") == topic:
            for c in t.get("concepts", []):
                en = c.get("en", "")
                k = canonical_key(en)
                if k:
                    out.add(k)
    return out


def per_topic_pairwise(records: List[dict]) -> Dict[str, Dict[str, float]]:
    """topic -> (pair -> LDS-C pooled over records of that language)."""
    by_lang_topic = defaultdict(lambda: defaultdict(set))
    for r in records:
        lang = r.get("language", "")
        for t in r.get("topics", []):
            tl = t.get("topic", "")
            if tl not in TOPICS:
                continue
            for c in t.get("concepts", []):
                en = c.get("en", "")
                k = canonical_key(en)
                if k:
                    by_lang_topic[lang][tl].add(k)
    out: Dict[str, Dict[str, float]] = defaultdict(dict)
    for tl in TOPICS:
        for pair, la, lb in PAIRS:
            sa = by_lang_topic.get(la, {}).get(tl, set())
            sb = by_lang_topic.get(lb, {}).get(tl, set())
            if sa and sb:
                out[tl][pair] = round(lds_concept(sa, sb), 4)
    return dict(out)


def per_topic_split_half(records: List[dict], n_iter: int = 200) -> Dict[str, Dict[str, float]]:
    """topic -> (pair -> within-language split-half floor)."""
    import random
    rng = random.Random(RANDOM_SEED + 3)
    by_lang = defaultdict(list)
    for r in records:
        by_lang[r.get("language", "")].append(r)
    out: Dict[str, Dict[str, float]] = defaultdict(dict)
    for tl in TOPICS:
        for pair, la, lb in PAIRS:
            vals = []
            for lang in (la, lb):
                reps = by_lang.get(lang, [])
                if len(reps) < 2:
                    continue
                lv = []
                for _ in range(n_iter):
                    rng.shuffle(reps)
                    half = len(reps) // 2
                    a = set()
                    b = set()
                    for r in reps[:half]:
                        a |= response_topic_groups(r, tl)
                    for r in reps[half:]:
                        b |= response_topic_groups(r, tl)
                    if a and b:
                        lv.append(lds_concept(a, b))
                if lv:
                    vals.append(statistics.mean(lv))
            if vals:
                out[tl][pair] = round(statistics.mean(vals), 4)
    return dict(out)


def per_topic_frame(records: List[dict], n_iter: int = 500) -> Dict[str, Dict[str, float]]:
    """topic -> (code -> LDS natural vs cross-frame)."""
    import random
    rng = random.Random(RANDOM_SEED + 7)
    out: Dict[str, Dict[str, float]] = defaultdict(dict)
    for code in ["zh", "de"]:
        other = "de" if code == "zh" else "zh"
        natural = [r for r in records
                   if r["probe"] == "P1" and r["language"] == code and r["frame"] == "natural"]
        crossed = [r for r in records
                   if r["probe"] == "P2" and r["language"] == code and r["frame"] == other]
        if not natural or not crossed:
            continue
        for tl in TOPICS:
            a = set()
            b = set()
            for r in natural:
                a |= response_topic_groups(r, tl)
            for r in crossed:
                b |= response_topic_groups(r, tl)
            if a and b:
                # point estimate
                point = lds_concept(a, b)
                # bootstrap CI via resampling units
                vals = []
                for _ in range(n_iter):
                    na = {frozenset(response_topic_groups(r, tl)) for r in
                          [rng.choice(natural) for _ in natural]}
                    cb = {frozenset(response_topic_groups(r, tl)) for r in
                          [rng.choice(crossed) for _ in crossed]}
                    a_ = set().union(*na) if na else set()
                    b_ = set().union(*cb) if cb else set()
                    if a_ and b_:
                        vals.append(lds_concept(a_, b_))
                ci = None
                if vals:
                    vals.sort()
                    ci = [round(vals[int(0.025 * len(vals))], 4),
                          round(vals[int(0.975 * len(vals))], 4)]
                out[tl][code] = {"lds": round(point, 4), "ci_95": ci}
    return dict(out)


def per_topic_assoc(assoc_records: List[dict], gloss: Dict[str, str]) -> Dict[str, Dict[str, float]]:
    """topic -> (pair -> association LDS on that topic, glossed)."""
    by_lang_topic = defaultdict(lambda: defaultdict(set))
    for r in assoc_records:
        lang = r.get("language", "")
        topic = r.get("topic", "ALL")
        for t in r.get("topics", []):
            tl = t.get("topic", "")
            for c in t.get("concepts", []):
                en = c.get("en", "")
                k = canonical_key(en)
                if k:
                    by_lang_topic[lang][tl].add(k)
    out: Dict[str, Dict[str, float]] = defaultdict(dict)
    for tl in TOPICS:
        for pair, la, lb in PAIRS:
            sa = by_lang_topic.get(la, {}).get(tl, set())
            sb = by_lang_topic.get(lb, {}).get(tl, set())
            if sa and sb:
                out[tl][pair] = round(lds_concept(sa, sb), 4)
    return dict(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="D1 per-topic mechanism decomposition")
    ap.add_argument("--in", dest="in_file", type=str, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    if args.in_file:
        units = json.loads(Path(args.in_file).read_text(encoding="utf-8"))["units"]
    else:
        from lds_c_llm_analyze import latest_units
        units = latest_units()

    p1_records = [unit_to_record(u) for u in units if u["probe"] == "P1"]
    p2_records = [unit_to_record(u) for u in units if u["probe"] in ("P1", "P2")]
    gloss = load_assoc_gloss()
    p3_records = [unit_to_assoc_record(u, gloss) for u in units if u["probe"] == "P3"]

    print("  Computing per-topic P1 LDS-C...")
    p1 = per_topic_pairwise(p1_records)
    print("  Computing per-topic split-half floors...")
    floors = per_topic_split_half(p1_records)
    print("  Computing per-topic frame effects...")
    frame = per_topic_frame(p2_records)
    print("  Computing per-topic association LDS...")
    assoc = per_topic_assoc(p3_records, gloss)

    result = {
        "design": "d1_mechanism_per_topic",
        "generated_at": datetime.now().isoformat(),
        "topics": TOPICS,
        "p1_lds_per_topic": p1,
        "p1_split_half_floor_per_topic": floors,
        "p2_frame_effect_per_topic": frame,
        "p3_assoc_lds_per_topic": assoc,
    }

    out_path = OUT_DIR / (args.out or f"per_topic_{datetime.now().strftime('%Y%m%d')}.json")
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")

    # Console table
    print("\n=== P1 LDS-C per topic (ZH-DE / ZH-EN / DE-EN) + floor ===")
    for tl in TOPICS:
        row = p1.get(tl, {})
        fl = floors.get(tl, {})
        cells = " | ".join(f"{pair}:{row.get(pair, '—')}" for pair, _, _ in PAIRS)
        fcells = " | ".join(f"flr:{fl.get(pair, '—')}" for pair, _, _ in PAIRS)
        print(f"  {tl:14s} {cells}   ({fcells})")
    print("\n=== P2 frame effect per topic (natural vs cross-frame) ===")
    for tl in TOPICS:
        fr = frame.get(tl, {})
        cells = " | ".join(f"{code}:{fr.get(code, {}).get('lds', '—')}"
                           for code in ["zh", "de"])
        print(f"  {tl:14s} {cells}")
    print("\n=== P3 association LDS per topic ===")
    for tl in TOPICS:
        row = assoc.get(tl, {})
        cells = " | ".join(f"{pair}:{row.get(pair, '—')}" for pair, _, _ in PAIRS)
        print(f"  {tl:14s} {cells}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""LinguaGraph — R1: human within-subject analysis (ready-to-run).

Completes the pre-registered within-subject arm (OSF §2.1/§4.2). For each
bilingual participant who answered the same 5 topics in L1, L2, and L1-retest
(3 rounds), computes:

  LDS_cross  = lds_concept(S_L1, S_L2)       (within-person cross-language)
  LDS_retest = lds_concept(S_L1, S_L1r)      (within-person within-language floor)
  margin     = LDS_cross - LDS_retest

Decision rule (research_forward_review R1):
  margin > 0 and ~ LLM within-subject margin (0.08-0.09)  => human null =
    between-subject heterogeneity, directly confirmed
  margin ~ 0  => honest negative; LLM signal is a model property, not human
  margin < 0  => counterintuitive; needs interpretation

Expected input JSON (participant-linked, documented format):
{
  "participants": {
    "P01": {"pair": "ZH-EN", "L1": "zh", "L2": "en",
            "rounds": {"R1": {"topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom"}]}, ...]},
                       "R2": {...}, "R3": {...}}},
    ...
  }
}
Concept extraction is done upstream (qwen-plus, frozen) and formatted like the
human extractions_*.json topics structure. Only canonical_key + lds_concept are
used here (frozen). To adapt: --in <path>, and an --out path.

Output: data/lds_c/llm_subject/r1_within_subject_<date>.json + console.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import canonical_key, lds_concept  # noqa: E402
from lds_c_llm_analyze import OUT_DIR  # noqa: E402


def _concept_set(topics: list) -> set:
    out = set()
    for t in topics or []:
        for c in t.get("concepts", []):
            k = canonical_key(c.get("en", ""))
            if k:
                out.add(k)
    return out


def analyze_participant(p: dict) -> dict:
    rounds = p.get("rounds", {})
    s1 = _concept_set(rounds.get("R1", {}).get("topics", []))
    s2 = _concept_set(rounds.get("R2", {}).get("topics", []))
    s1r = _concept_set(rounds.get("R3", {}).get("topics", []))
    if not s1 or not s2 or not s1r:
        return {"error": "incomplete rounds", "sizes": [len(s1), len(s2), len(s1r)]}
    lds_cross = lds_concept(s1, s2)
    lds_retest = lds_concept(s1, s1r)
    overlap_enforce = len(s1 & s2) / len(s1 | s2) if (s1 | s2) else 0
    return {
        "pair": p.get("pair"), "L1": p.get("L1"), "L2": p.get("L2"),
        "n_concepts": {"L1": len(s1), "L2": len(s2), "L1_retest": len(s1r)},
        "cross_lang_J": round(len(s1 & s2) / len(s1 | s2), 4),
        "lds_cross": round(lds_cross, 4),
        "lds_retest": round(lds_retest, 4),
        "margin": round(lds_cross - lds_retest, 4),
        "cross_lang_overlap_pct": round(100 * overlap_enforce, 1),
    }


def _bootstrap_ci(values: list, n_iter: int = 2000, seed: int = 2026) -> dict:
    import random
    rng = random.Random(seed)
    if not values:
        return {"ci_lower": None, "ci_upper": None}
    means = []
    for _ in range(n_iter):
        s = [rng.choice(values) for _ in values]
        means.append(statistics.mean(s))
    means.sort()
    return {"ci_lower": round(means[int(0.025 * len(means))], 4),
            "ci_upper": round(means[int(0.975 * len(means))], 4)}


def _one_sample_t(values: list) -> dict:
    n = len(values)
    if n < 2:
        return {"n": n, "t": None, "p": None}
    mean = statistics.mean(values)
    sd = statistics.stdev(values) if n > 1 else 0
    se = sd / (n ** 0.5)
    t = mean / se if se else None
    from scipy import stats as _st
    p = (2 * _st.t.sf(abs(t), n - 1)) if t is not None and t == t else None
    return {"n": n, "mean": round(mean, 4), "sd": round(sd, 4),
            "t": round(t, 3) if t == t else None, "p": p}


def main() -> None:
    ap = argparse.ArgumentParser(description="R1 human within-subject analysis")
    ap.add_argument("--in", dest="in_file", type=str, required=True)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    data = json.loads(Path(args.in_file).read_text(encoding="utf-8"))
    participants = data.get("participants", data)  # tolerate bare dict

    results = {}
    for pid, p in participants.items():
        r = analyze_participant(p)
        r["participant"] = pid
        results[pid] = r

    valid = [r for r in results.values() if "error" not in r]
    print(f"  Participants: {len(results)}  valid: {len(valid)}")

    # ── Aggregate per pair ──
    by_pair = defaultdict(list)
    for r in valid:
        pair = r.get("pair") or "UNKNOWN"
        by_pair[pair].append(r)

    agg = {}
    for pair, rows in sorted(by_pair.items()):
        margins = [r["margin"] for r in rows]
        cross = [r["lds_cross"] for r in rows]
        retest = [r["lds_retest"] for r in rows]
        agg[pair] = {
            "n": len(rows),
            "margin_mean": round(statistics.mean(margins), 4),
            "margin_median": round(statistics.median(margins), 4),
            "n_positive": sum(1 for m in margins if m > 0),
            "margin_ci": _bootstrap_ci(margins),
            "one_sample_t_margin_gt_0": _one_sample_t(margins),
            "lds_cross_mean": round(statistics.mean(cross), 4),
            "lds_retest_mean": round(statistics.mean(retest), 4),
            "cross_lang_overlap_pct_mean": round(
                statistics.mean([r["cross_lang_overlap_pct"] for r in rows]), 1),
        }

    print("\n  === R1 within-subject results (per pair) ===")
    print(f"  {'pair':<8s} {'n':>2s} {'margin mean':>10s} {'n_pos':>5s} "
          f"{'t':>7s} {'p':>7s} {'ci95':>16s} {'crossLDS':>9s} {'retestLDS':>9s}")
    for pair, a in agg.items():
        ts = a["one_sample_t_margin_gt_0"]
        t_str = f"{ts['t']:.2f}" if ts["t"] is not None else "—"
        p_str = f"{ts['p']:.4f}" if ts["p"] is not None else "—"
        ci = a["margin_ci"]
        ci_str = f"[{ci['ci_lower']:.3f},{ci['ci_upper']:.3f}]" if ci["ci_lower"] is not None else "—"
        print(f"  {pair:<8s} {a['n']:>2d} {a['margin_mean']:>+10.4f} {a['n_positive']:>5d} "
              f"{t_str:>7s} {p_str:>7s} {ci_str:>16s} "
              f"{a['lds_cross_mean']:>+9.4f} {a['lds_retest_mean']:>+9.4f}")

    print("\n  Reference (LLM within-subject, D1 baseline): margin +0.08..+0.09; "
          "55-model panel: +0.03..+0.42")

    out = {
        "design": "r1_human_within_subject",
        "generated_at": datetime.now().isoformat(),
        "n_participants": len(valid),
        "aggregate": agg,
        "per_participant": results,
        "reference_llm_margin": {"D1_baseline": "0.08-0.09", "panel_range": "0.03-0.42"},
    }
    out_path = OUT_DIR / (args.out or f"r1_within_subject_{datetime.now().strftime('%Y%m%d')}.json")
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()

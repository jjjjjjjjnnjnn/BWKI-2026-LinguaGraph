#!/usr/bin/env python3
"""G2 gold blind-audit tool (social subset, n=72).

- --generate: deterministic shuffle (seed default 20260914) of the 72
  auto_accepted social gold items, STRIPPING gold concepts, writing a
  review template to research/gold_review_v2/review_72.json.
  concepts are NEVER prefilled and no AI pre-labeling is run.
- --import <filled.json>: score a filled review file:
  (1) Jaccard agreement vs current gold concepts (overall + by language);
  (2) qwen-plus social F1 recomputed with v2 as gold, using
      data/model_comparison/qwen-plus_results.json predicted_concepts;
  (3) verdict: pass (may mature) iff F1>=0.85 AND agreement>=0.8.

Template record fields:
  audit_id / sample_id / language / question / text /
  concepts_blank[] (always []) / reviewer / decision (accept|edit|reject) /
  edited_concepts (reviewer-filled list; required unless reject).
"""

import argparse
import json
import random
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
GOLD_PATH = PROJECT / "data" / "gold" / "gold_dataset.json"
QWEN_PLUS_PATH = PROJECT / "data" / "model_comparison" / "qwen-plus_results.json"
OUT_DIR = PROJECT / "research" / "gold_review_v2"
DEFAULT_SEED = 20260914
PASS_F1 = 0.85
PASS_AGR = 0.80


def load_social_gold():
    items = json.loads(GOLD_PATH.read_text(encoding="utf-8"))
    if isinstance(items, dict):
        items = items.get("items", items.get("results", items.get("data", [])))
    social = [x for x in items if x.get("annotator") == "auto_accepted"]
    if len(social) != 72:
        print(f"[warn] expected 72 social items, found {len(social)}", file=sys.stderr)
    return social


def generate(seed: int, out_name: str = "review_72.json") -> Path:
    social = load_social_gold()
    rng = random.Random(seed)
    order = list(social)
    rng.shuffle(order)
    records = []
    for i, it in enumerate(order, 1):
        records.append({
            "audit_id": f"A{i:03d}",
            "sample_id": it.get("sample_id"),
            "language": it.get("language"),
            "question": it.get("question", ""),
            "text": it.get("text", ""),
            "concepts_blank": [],
            "reviewer": "",
            "decision": "",
            "edited_concepts": [],
        })
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / out_name
    payload = {
        "meta": {
            "seed": seed,
            "n": len(records),
            "source": "data/gold/gold_dataset.json (annotator=auto_accepted)",
            "blinding": "gold concepts stripped; concepts_blank always []; no AI pre-label",
            "decision_values": ["accept", "edit", "reject"],
        },
        "records": records,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[generate] seed={seed} n={len(records)} -> {out}")
    return out


def jaccard(a, b) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def prf(gold, pred):
    g, p = set(gold), set(pred)
    if not g or not p:
        return 0.0, 0.0, 0.0
    tp = len(g & p)
    prec = tp / len(p)
    rec = tp / len(g)
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return prec, rec, f1


def import_scores(path: Path):
    filled = json.loads(Path(path).read_text(encoding="utf-8"))
    records = filled.get("records", filled) if isinstance(filled, dict) else filled
    gold = {x["sample_id"]: x for x in load_social_gold()}
    qpred = {}
    qd = json.loads(QWEN_PLUS_PATH.read_text(encoding="utf-8"))
    for r in qd.get("results", []):
        qpred[r["sample_id"]] = r.get("predicted_concepts", [])

    agr_all, agr_by_lang = [], {}
    f1s = []
    n_reject = 0
    for rec in records:
        sid = rec.get("sample_id")
        dec = (rec.get("decision") or "").strip().lower()
        edited = rec.get("edited_concepts", []) or []
        cur = gold.get(sid, {}).get("human_labels", {}).get("concepts", [])
        lang = rec.get("language", gold.get(sid, {}).get("language", "?"))
        if dec == "reject":
            n_reject += 1
            agr = 0.0
        elif dec in ("accept", "edit"):
            agr = jaccard(cur, edited)
        else:
            print(f"[warn] {sid}: bad decision {dec!r}, skipped", file=sys.stderr)
            continue
        agr_all.append(agr)
        agr_by_lang.setdefault(lang, []).append(agr)
        if dec != "reject" and edited:
            _, _, f1 = prf(edited, qpred.get(sid, []))
            f1s.append(f1)

    agr_mean = sum(agr_all) / len(agr_all) if agr_all else 0.0
    by_lang = {k: round(sum(v) / len(v), 4) for k, v in sorted(agr_by_lang.items())}
    f1_mean = sum(f1s) / len(f1s) if f1s else 0.0
    verdict = "pass (may mature)" if (f1_mean >= PASS_F1 and agr_mean >= PASS_AGR) else "maintain (stay pilot)"
    report = {
        "n_reviewed": len(agr_all),
        "n_reject": n_reject,
        "agreement_overall": round(agr_mean, 4),
        "agreement_by_language": by_lang,
        "qwen_plus_social_f1_v2gold": round(f1_mean, 4),
        "n_f1_valid": len(f1s),
        "thresholds": {"f1": PASS_F1, "agreement": PASS_AGR},
        "verdict": verdict,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main():
    ap = argparse.ArgumentParser(description="G2 gold blind audit (social n=72)")
    ap.add_argument("--generate", action="store_true")
    ap.add_argument("--import", dest="import_path", default=None)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--out", default="review_72.json")
    args = ap.parse_args()
    if args.generate:
        generate(args.seed, args.out)
    elif args.import_path:
        import_scores(Path(args.import_path))
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()

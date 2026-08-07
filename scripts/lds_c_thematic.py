#!/usr/bin/env python3
"""
LinguaGraph — Thematic Qualitative Analysis (coarse 6-category codebook)

Classifies LLM-extracted concept glosses into a 6-category codebook and
compares the category distributions across ZH/DE/EN.

Codebook v1 (confirmed 2026-08-07):
  LI  Legal/Institutional — law, rights, rules, formal systems, procedure
  IA  Individual/Autonomy — personal agency, choice, self-determination, free will
  MC  Material/Concrete   — survival, physical needs, resources, money, housing
  SR  Social/Relational   — family, others, community, collective, duties-to-others
  MA  Moral/Abstract      — values, principles, ethics, abstract ideals
  EA  Emotional/Affective — feelings, safety, belonging, happiness, comfort

Pipeline:
  1. Load extractions (concept + English gloss per response per topic)
  2. LLM classify UNIQUE glosses (batched, resume-safe) -> save mapping
  3. Aggregate counts per language × category (pooled + per-topic)
  4. Statistics: chi-square, permutation p, Cramér's V, Wilson CI, Shannon entropy
  5. Save results + print table

Usage:
    python scripts/lds_c_thematic.py                     # classify + analyze
    python scripts/lds_c_thematic.py --analyze-only      # skip LLM, reuse mapping
    python scripts/lds_c_thematic.py --iterations 5000   # permutation iterations

Output: data/lds_c/thematic_classification_<date>.json, outputs/lds_c_thematic_<date>.json
"""

import argparse
import json
import math
import os
import re
import random
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
API_URL = "https://opencode.ai/zen/go/v1"
MODEL = "deepseek-v4-flash"
BATCH = 15  # small batches reduce deepseek reasoning explosion
RANDOM_SEED = 42

CATEGORIES = ["Legal/Institutional", "Individual/Autonomy", "Material/Concrete",
              "Social/Relational", "Moral/Abstract", "Emotional/Affective"]
CAT_SHORT = {"Legal/Institutional": "LI", "Individual/Autonomy": "IA",
             "Material/Concrete": "MC", "Social/Relational": "SR",
             "Moral/Abstract": "MA", "Emotional/Affective": "EA"}
SHORT_TO_FULL = {v: k for k, v in CAT_SHORT.items()}


def norm_cat(c: str) -> str:
    """Normalize a category label from the LLM (may be short code or full name)."""
    c = (c or "").strip()
    if c in CATEGORIES:
        return c
    if c in SHORT_TO_FULL:
        return SHORT_TO_FULL[c]
    for full in CATEGORIES:
        if full.lower() in c.lower() or c.lower() in full.lower():
            return full
    return c

CODEBOOK_DEF = """LI Legal/Institutional: law, rights, rules, courts, procedures, formal institutions
IA Individual/Autonomy: personal agency, choice, self-determination, independence, free will
MC Material/Concrete: survival, physical needs, resources, money, food, housing, work/income
SR Social/Relational: family, others, community, collective, relationships, duties toward others
MA Moral/Abstract: values, principles, ethics, philosophical/abstract ideals, justice as ideal
EA Emotional/Affective: feelings, safety, belonging, happiness, comfort, wellbeing"""

CLASSIFY_PROMPT = """Classify each concept into exactly ONE category. Definitions:
{codebook}

Rules: pick the SINGLE most salient category. If a concept spans two, choose the primary one.
Return ONLY JSON array (no reasoning):
[{{"gloss": "...", "category": "..."}}]

Concepts:
{glosses}"""


def load_env_key() -> str:
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() == "OPENAI_API_KEY":
                    return v.strip()
    return os.environ.get("OPENAI_API_KEY", "")


def load_extractions() -> List[dict]:
    import glob
    files = sorted(glob.glob(str(PROJECT_ROOT / "data" / "lds_c" / "extractions_*.json")))
    files = [f for f in files if "TEST" not in f and "cluster" not in f]
    if not files:
        raise FileNotFoundError("No extractions found in data/lds_c")
    data = json.loads(Path(files[-1]).read_text(encoding="utf-8"))
    return data.get("responses", [])


# ── LLM classification ─────────────────────────────────────

def _parse_classify(raw: str) -> List[dict]:
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    if "```json" in cleaned:
        cleaned = cleaned.split("```json")[1].split("```")[0].strip()
    elif "```" in cleaned:
        cleaned = cleaned.split("```")[1].split("```")[0].strip()
    try:
        arr = json.loads(cleaned)
        return arr if isinstance(arr, list) else []
    except json.JSONDecodeError:
        m = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                return []
        return []


def classify_batch(client, glosses: List[str]) -> Dict[str, str]:
    prompt = CLASSIFY_PROMPT.format(codebook=CODEBOOK_DEF, glosses="\n".join(f"- {g}" for g in glosses))
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a precise qualitative codebook coder. Output only JSON, no reasoning."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=4000,
        timeout=120,
    )
    raw = resp.choices[0].message.content or ""
    results = _parse_classify(raw)
    mapping = {}
    for item in results:
        g = (item.get("gloss") or "").strip().lower()
        c = item.get("category") or ""
        if g and c:
            mapping[g] = norm_cat(c)
    return mapping


# ── Aggregation ────────────────────────────────────────────

def aggregate(records: List[dict], gloss_cat: Dict[str, str]) -> Dict:
    """Return pooled (lang->cat->count) and per-topic (lang->topic->cat->count),
    plus per-response concept counts and topic coverage."""
    pooled: Dict[str, Counter] = defaultdict(Counter)
    per_topic: Dict[str, Dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    n_concepts_per_lang = Counter()
    n_concepts_per_topic_lang = defaultdict(Counter)
    unmapped: Counter = Counter()

    for r in records:
        lang = r.get("language", "")
        for t in r.get("topics", []):
            topic = t.get("topic", "")
            for c in t.get("concepts", []):
                gloss = (c.get("en") or "").strip().lower()
                cat = norm_cat(gloss_cat.get(gloss, "UNK"))
                pooled[lang][cat] += 1
                per_topic[lang][topic][cat] += 1
                n_concepts_per_lang[lang] += 1
                n_concepts_per_topic_lang[lang][topic] += 1
                if cat == "UNK":
                    unmapped[lang] += 1
    return {
        "pooled": {k: dict(v) for k, v in pooled.items()},
        "per_topic": {k: {t: dict(v) for t, v in lang.items()} for k, lang in per_topic.items()},
        "n_concepts": dict(n_concepts_per_lang),
        "n_concepts_per_topic": {k: dict(v) for k, v in n_concepts_per_topic_lang.items()},
        "unknown_cats": {g: c for g, c in gloss_cat.items() if norm_cat(c) not in CATEGORIES},
        "unmapped_count": dict(unmapped),
    }


# ── Statistics ─────────────────────────────────────────────

def contingency(pooled: Dict[str, Dict[str, int]]) -> Tuple[List[List[int]], List[str], List[str]]:
    langs = sorted(pooled.keys())
    cats = [c for c in CATEGORIES]
    table = [[pooled.get(l, {}).get(c, 0) for c in cats] for l in langs]
    return table, langs, cats


def chi2_test(table, langs, cats) -> dict:
    from scipy.stats import chi2_contingency
    chi2, p, dof, expected = chi2_contingency(table)
    n = sum(sum(row) for row in table)
    cramers_v = math.sqrt(chi2 / (n * min(len(langs) - 1, len(cats) - 1)))
    return {"chi2": round(chi2, 4), "p_value": round(p, 6), "dof": dof,
            "cramers_v": round(cramers_v, 4), "n": n,
            "min_expected": round(float(expected.min()), 4),
            "warning": "expected<5 cells" if (expected < 5).any() else ""}


def permutation_p(records, gloss_cat, n_iter=5000) -> dict:
    """Permute language labels across concept instances; recompute chi2 statistic.
    Empirical p = P(null chi2 >= observed chi2). Robust for small samples."""
    random.seed(RANDOM_SEED)
    # flatten concept instances: (orig_lang, cat)
    instances = []
    for r in records:
        lang = r.get("language", "")
        for t in r.get("topics", []):
            for c in t.get("concepts", []):
                gloss = (c.get("en") or "").strip().lower()
                instances.append((lang, gloss_cat.get(gloss, "UNK")))
    langs = sorted(set(i[0] for i in instances))
    cats = sorted(set(i[1] for i in instances))
    orig_langs = [i[0] for i in instances]

    def _chi2(lang_list):
        tbl = [[0] * len(cats) for _ in langs]
        for l, c in zip(lang_list, [i[1] for i in instances]):
            if l in langs and c in cats:
                tbl[langs.index(l)][cats.index(c)] += 1
        # chi2 stat (manual, no scipy for speed)
        row_tot = [sum(row) for row in tbl]
        col_tot = [sum(tbl[i][j] for i in range(len(langs))) for j in range(len(cats))]
        n = sum(row_tot)
        if n == 0:
            return 0.0
        stat = 0.0
        for i in range(len(langs)):
            for j in range(len(cats)):
                exp = row_tot[i] * col_tot[j] / n
                if exp > 0:
                    stat += (tbl[i][j] - exp) ** 2 / exp
        return stat

    observed = _chi2(orig_langs)
    count_ge = 0
    for _ in range(n_iter):
        shuffled = orig_langs[:]
        random.shuffle(shuffled)
        if _chi2(shuffled) >= observed:
            count_ge += 1
    return {"perm_p": round(count_ge / n_iter, 6), "n_iter": n_iter, "obs_chi2": round(observed, 4)}


def wilson_ci(k: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def entropy(counts: Dict[str, int]) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    h = 0.0
    for c in counts.values():
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return round(h, 4)


# ── Report ─────────────────────────────────────────────────

def build_report(records, gloss_cat, n_iter) -> dict:
    agg = aggregate(records, gloss_cat)
    table, langs, cats = contingency(agg["pooled"])
    chi2 = chi2_test(table, langs, cats)
    perm = permutation_p(records, gloss_cat, n_iter)
    # per-language entropy + per-category proportions
    lang_entropy = {l: entropy(agg["pooled"].get(l, {})) for l in langs}
    proportions = {}
    for c in cats:
        proportions[c] = {}
        for l in langs:
            k = agg["pooled"].get(l, {}).get(c, 0)
            n = agg["n_concepts"].get(l, 0)
            lo, hi = wilson_ci(k, n)
            proportions[c][l] = {"count": k, "prop": round(k / n, 4) if n else 0,
                                 "ci_lo": round(lo, 4), "ci_hi": round(hi, 4)}
    return {
        "generated_at": datetime.now().isoformat(),
        "model": MODEL,
        "codebook_version": "v1",
        "categories": CATEGORIES,
        "n_responses": len(records),
        "language_sizes": dict(Counter(r.get("language", "") for r in records)),
        "n_concepts": agg["n_concepts"],
        "pooled_counts": agg["pooled"],
        "per_topic_counts": agg["per_topic"],
        "chi2_test": chi2,
        "permutation_test": perm,
        "lang_entropy": lang_entropy,
        "per_category": proportions,
        "unknown_categories": agg["unknown_cats"],
        "unmapped_gloss_count": agg["unmapped_count"],
    }


def format_table(report: dict) -> str:
    langs = sorted(report["language_sizes"].keys())
    lines = []
    header = f"{'Category':22s}" + "".join(f"| {l.upper():>6s} prop(CI)" for l in langs)
    lines.append(header)
    lines.append("-" * len(header))
    for c in report["categories"]:
        row = f"{CAT_SHORT[c]:22s}"
        for l in langs:
            d = report["per_category"][c].get(l, {})
            prop = d.get("prop", 0)
            lo, hi = d.get("ci_lo", 0), d.get("ci_hi", 0)
            row += f"| {prop:.2f}({lo:.2f}-{hi:.2f})"
        lines.append(row)
    lines.append("")
    lines.append(f"  Chi-square: χ²={report['chi2_test']['chi2']}, p={report['chi2_test']['p_value']}, "
                 f"Cramér's V={report['chi2_test']['cramers_v']} (min expected={report['chi2_test']['min_expected']})")
    lines.append(f"  Permutation p (n={report['permutation_test']['n_iter']}): {report['permutation_test']['perm_p']}")
    lines.append(f"  Shannon entropy H(lang): " + ", ".join(f"{l.upper()}={report['lang_entropy'].get(l, 0)}" for l in langs))
    lines.append(f"  Unknown categories: {len(report['unknown_categories'])}")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analyze-only", action="store_true", help="Skip LLM, reuse classification mapping")
    ap.add_argument("--iterations", type=int, default=5000)
    args = ap.parse_args()

    records = load_extractions()
    print(f"  Responses: {len(records)}")

    # collect unique glosses
    unique = set()
    for r in records:
        for t in r.get("topics", []):
            for c in t.get("concepts", []):
                g = (c.get("en") or "").strip().lower()
                if g:
                    unique.add(g)
    print(f"  Unique glosses: {len(unique)}")

    # classification mapping file
    out_dir = PROJECT_ROOT / "data" / "lds_c"
    out_dir.mkdir(parents=True, exist_ok=True)
    cls_path = out_dir / f"thematic_classification_{datetime.now().strftime('%Y%m%d')}.json"
    gloss_cat: Dict[str, str] = {}
    if cls_path.exists() or args.analyze_only:
        existing = sorted(out_dir.glob("thematic_classification_*.json"))
        if existing:
            raw_map = json.loads(Path(existing[-1]).read_text(encoding="utf-8"))
            gloss_cat = {g: norm_cat(c) for g, c in raw_map.items()}
            print(f"  Reused classification: {len(gloss_cat)} glosses")

    if not args.analyze_only:
        todo = [g for g in sorted(unique) if g not in gloss_cat]
        print(f"  To classify: {len(todo)} glosses")
        if todo:
            key = load_env_key()
            if not key:
                sys.exit("ERROR: OPENAI_API_KEY not found")
            from openai import OpenAI
            client = OpenAI(base_url=API_URL, api_key=key)
            for i in range(0, len(todo), BATCH):
                chunk = todo[i : i + BATCH]
                ok = False
                part: Dict[str, str] = {}
                for attempt in range(3):
                    try:
                        part = classify_batch(client, chunk)
                    except Exception as e:
                        if attempt < 2:
                            print(f"    [retry {attempt + 1}] {e}", flush=True)
                            time.sleep(2)
                        continue
                    if part:
                        ok = True
                        break
                    if attempt < 2:
                        print(f"    [retry {attempt + 1}] empty result", flush=True)
                        time.sleep(2)
                gloss_cat.update(part)
                if not ok:
                    print(f"    [FAIL] chunk {i // BATCH + 1}: {chunk[:3]}...", flush=True)
                # incremental save
                cls_path.write_text(json.dumps(gloss_cat, ensure_ascii=False, indent=1), encoding="utf-8")
                print(f"    chunk {i // BATCH + 1}/{(len(todo) - 1) // BATCH + 1}: {len(gloss_cat)} mapped", flush=True)
                time.sleep(0.3)
            # save final under canonical name
            out_path = out_dir / f"thematic_classification_{datetime.now().strftime('%Y%m%d')}.json"
            out_path.write_text(json.dumps(gloss_cat, ensure_ascii=False, indent=1), encoding="utf-8")

    report = build_report(records, gloss_cat, args.iterations)
    print("\n" + format_table(report))

    out = PROJECT_ROOT / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    out_path = out / f"lds_c_thematic_{datetime.now().strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  [OK] Saved: {out_path}")


if __name__ == "__main__":
    main()

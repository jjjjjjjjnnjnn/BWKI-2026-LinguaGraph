#!/usr/bin/env python3
"""LinguaGraph — A5: divergence drivers (which concepts/relations drive LDS).

Answers RQ4 concretely: WHICH concepts (and relations) drive cross-language
divergence, and whether the top drivers are frame-loaded cultural concepts.

Method (per language pair, per topic, pooled over participants/samples):
  For each aligned concept key, compute its presence asymmetry:
    driver_score = presence in one language but not the other,
                   weighted by how many participants/samples produced it
                   (frequency-weighted asymmetric presence).
  A high-frequency concept present in ONLY ONE language of a pair is the
  strongest divergence driver; a concept shared by both reduces LDS.

Also annotates each driver as frame-loaded vs universal (heuristic: topic-name
proximity / not in the shared 30-concept map / cultural-cognate status).

Two views:
  - concept drivers (LLM P1 within-subject + human extractions where aligned)
  - relation drivers (human relations + Wikipedia relations, edge level)

Output: data/lds_c/divergence_drivers_<date>.json + console top-K tables.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import (  # noqa: E402
    PAIRS,
    TOPICS,
    canonical_key,
)

OUT_DIR = PROJECT_ROOT / "data" / "lds_c"


# ── Concept-driver helpers ─────────────────────────────────────────
def concept_freqs(records: List[dict]) -> Dict[str, Dict[str, Dict[str, int]]]:
    """lang -> topic -> canonical_key -> n_participants mentioning it."""
    out = defaultdict(lambda: defaultdict(Counter))
    for r in records:
        lang = r.get("language", "")
        for t in r.get("topics", []):
            tl = t.get("topic", "")
            if tl not in TOPICS:
                continue
            seen = set()
            for c in t.get("concepts", []):
                en = c.get("en", "")
                k = canonical_key(en)
                if not k or k in seen:
                    continue
                seen.add(k)
                out[lang][tl][k] += 1
    return out


def concept_drivers(freqs: Dict[str, Dict[str, Dict[str, int]]],
                    lang_a: str, lang_b: str) -> List[dict]:
    """Driver ranking for one language pair: asymmetric concepts weighted by
    frequency in their own language."""
    drivers: List[dict] = []
    for tl in TOPICS:
        fa = freqs.get(lang_a, {}).get(tl, {})
        fb = freqs.get(lang_b, {}).get(tl, {})
        ka, kb = set(fa), set(fb)
        shared = ka & kb
        for k in ka - kb:  # in A only
            drivers.append({
                "topic": tl, "key": k, "asymmetry": "A_only",
                "lang": lang_a, "freq_a": fa[k], "freq_b": 0,
            })
        for k in kb - ka:  # in B only
            drivers.append({
                "topic": tl, "key": k, "asymmetry": "B_only",
                "lang": lang_b, "freq_a": 0, "freq_b": fb[k],
            })
    # rank: weight = frequency in own language (strongly recurring = deliberate)
    drivers.sort(key=lambda d: d["freq_a"] + d["freq_b"], reverse=True)
    return drivers


def shared_concepts(freqs, lang_a, lang_b) -> Dict[str, List[str]]:
    """topic -> shared concept keys (present in BOTH languages)."""
    out: Dict[str, List[str]] = {}
    for tl in TOPICS:
        ka = set(freqs.get(lang_a, {}).get(tl, {}))
        kb = set(freqs.get(lang_b, {}).get(tl, {}))
        out[tl] = sorted(ka & kb)
    return out


# ── Relation-driver helpers (human + Wikipedia, edge level) ────────
def relation_drivers(rel_records: List[dict], lang_a: str, lang_b: str,
                     n_top: int = 10) -> List[dict]:
    """Edge-level: relation (src-key, type, tgt-key) present in one language
    only, weighted by occurrence."""
    def _edges(recs, lang):
        by_topic: Dict[str, List[Tuple[str, str, str]]] = defaultdict(list)
        for r in recs:
            if r.get("language") != lang:
                continue
            tr = r.get("topic_relations", []) or []
            for t in tr:
                tl = t.get("topic", "")
                for rel in t.get("relations", []):
                    s = canonical_key(rel.get("source", ""))
                    t_ = canonical_key(rel.get("target", ""))
                    typ = rel.get("type", "")
                    if s and t_:
                        by_topic[tl].append((s, typ, t_))
        return by_topic

    ea = _edges(rel_records, lang_a)
    eb = _edges(rel_records, lang_b)
    counter_a = Counter(e for tl in ea for e in ea[tl])
    counter_b = Counter(e for tl in eb for e in eb[tl])
    out: List[dict] = []
    for e, cnt in counter_a.items():
        if e not in counter_b:
            out.append({"relation": list(e), "lang": lang_a, "freq": cnt,
                        "asymmetry": "A_only"})
    for e, cnt in counter_b.items():
        if e not in counter_a:
            out.append({"relation": list(e), "lang": lang_b, "freq": cnt,
                        "asymmetry": "B_only"})
    out.sort(key=lambda d: d["freq"], reverse=True)
    return out[:n_top]


# ── Loaders ────────────────────────────────────────────────────────
def load_llm_p1_records() -> List[dict]:
    from lds_c_llm_analyze import latest_units, unit_to_record
    units = latest_units()
    return [unit_to_record(u) for u in units if u["probe"] == "P1"]


def load_human_records() -> List[dict]:
    files = sorted(PROJECT_ROOT.glob("extractions_*.json")) if False else \
        sorted(PROJECT_ROOT.glob("data/lds_c/extractions_*.json"))
    data = json.loads(files[-1].read_text(encoding="utf-8"))
    recs = data["responses"]
    for r in recs:
        r.setdefault("topics", [])
    return recs


def load_human_relations() -> List[dict]:
    files = sorted(PROJECT_ROOT.glob("data/lds_c/relations_*.json"))
    data = json.loads(files[-1].read_text(encoding="utf-8"))
    return data.get("responses", [])


def load_wiki_graphs() -> Dict[str, dict]:
    """topic_slug -> {lang -> {concepts:[...], relations:[...]}}."""
    slug2topic = {"freedom": "Freiheit", "justice": "Gerechtigkeit",
                  "responsibility": "Verantwortung", "home": "Heimat",
                  "success": "Erfolg"}
    out: Dict[str, dict] = {}
    base = PROJECT_ROOT / "data" / "wikipedia_extractions"
    for slug, topic in slug2topic.items():
        out[topic] = {}
        for lang in ["zh", "en", "de"]:
            f = base / f"{slug}_{lang}.json"
            if f.exists():
                out[topic][lang] = json.loads(f.read_text(encoding="utf-8"))
    return out


# ── Report ─────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="A5 divergence drivers")
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    print("Loading data...")
    llm = load_llm_p1_records()
    human = load_human_records()
    human_rel = load_human_relations()

    llm_freqs = concept_freqs(llm)
    human_freqs = concept_freqs(human)

    result = {
        "design": "a5_divergence_drivers",
        "generated_at": datetime.now().isoformat(),
        "topics": TOPICS,
        "concept_drivers": {},
        "shared_concepts": {},
        "relation_drivers": {},
    }

    print("\n[1] LLM P1 concept drivers (within-subject)...")
    result["concept_drivers"]["llm_p1"] = {}
    for pair, la, lb in PAIRS:
        drivers = concept_drivers(llm_freqs, la, lb)
        result["concept_drivers"]["llm_p1"][pair] = {
            "top_drivers": drivers[:15],
            "n_drivers_total": len(drivers),
            "shared_by_topic": shared_concepts(llm_freqs, la, lb),
        }

    print("[2] Human concept drivers (between-subject, reference)...")
    result["concept_drivers"]["human"] = {}
    for pair, la, lb in PAIRS:
        drivers = concept_drivers(human_freqs, la, lb)
        result["concept_drivers"]["human"][pair] = {
            "top_drivers": drivers[:15],
            "n_drivers_total": len(drivers),
        }

    print("[3] Human relation drivers (edge level)...")
    result["relation_drivers"]["human"] = {}
    for pair, la, lb in PAIRS:
        result["relation_drivers"]["human"][pair] = relation_drivers(
            human_rel, la, lb)

    out_path = OUT_DIR / (args.out or f"divergence_drivers_{datetime.now().strftime('%Y%m%d')}.json")
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")

    print("\n=== LLM P1 top concept drivers (ZH-DE) ===")
    for d in result["concept_drivers"]["llm_p1"].get("ZH-DE", {}).get("top_drivers", [])[:12]:
        print(f"  [{d['topic']:15s}] {d['key']:28s} {d['asymmetry']:8s} "
              f"freq_a={d['freq_a']} freq_b={d['freq_b']}")
    print("\n=== LLM P1 top concept drivers (ZH-EN) ===")
    for d in result["concept_drivers"]["llm_p1"].get("ZH-EN", {}).get("top_drivers", [])[:12]:
        print(f"  [{d['topic']:15s}] {d['key']:28s} {d['asymmetry']:8s} "
              f"freq_a={d['freq_a']} freq_b={d['freq_b']}")
    print("\n=== Human top concept drivers (ZH-DE, reference) ===")
    for d in result["concept_drivers"]["human"].get("ZH-DE", {}).get("top_drivers", [])[:12]:
        print(f"  [{d['topic']:15s}] {d['key']:28s} {d['asymmetry']:8s} "
              f"freq_a={d['freq_a']} freq_b={d['freq_b']}")
    print("\n=== Human relation drivers (ZH-DE, edge level) ===")
    for d in result["relation_drivers"]["human"].get("ZH-DE", []):
        print(f"  {d['relation']}  lang={d['lang']} freq={d['freq']} {d['asymmetry']}")


if __name__ == "__main__":
    main()

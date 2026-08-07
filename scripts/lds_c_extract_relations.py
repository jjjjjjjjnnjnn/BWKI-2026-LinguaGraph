#!/usr/bin/env python3
"""
LinguaGraph — LDS-C Relation Extraction (edges for v3 node+edge LDS)

Extracts explicit semantic relations between the already-extracted concepts
of each response (per topic), using the 7-type vocabulary from
config/prompts/extract.md. Relations are mapped to canonical concept keys
(via English gloss + canonical_key) so edges align across languages.

Designed for reliability with deepseek-v4-flash: per-topic small calls,
retry + resume, temperature 0.

Usage:
    python scripts/lds_c_extract_relations.py              # extract all
    python scripts/lds_c_extract_relations.py --dry-run    # show what would run

Output: data/lds_c/relations_<date>.json
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

API_URL = "https://opencode.ai/zen/go/v1"
MODEL = "deepseek-v4-flash"

RELATION_TYPES = ["part_of", "cause_effect", "represents", "implies",
                  "relates_to", "opposite_of", "is_a"]

RELATION_PROMPT = """The person answered the abstract topic "{topic}" like this:
{text}

The extracted concepts (with English glosses) are:
{concepts}

Extract the RELATIONSHIPS the person explicitly states BETWEEN these concepts.
Use ONLY these relation types: {types}
Return ONLY JSON array (no reasoning): [{{"source":"<concept string>","target":"<concept string>","type":"<type>"}}]
Only include relations the person explicitly expresses. If none, return [].
"""


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


def latest_concepts() -> Path:
    files = sorted(PROJECT_ROOT.glob("data/lds_c/extractions_*.json"))
    files = [f for f in files if "TEST" not in f.name and "cluster" not in f.name]
    if not files:
        raise FileNotFoundError("No concept extractions found")
    return files[-1]


def load_concepts(path: Path) -> List[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("responses", [])


def _parse_relations(raw: str) -> List[dict]:
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


def call_relations(client, topic: str, text: str, concept_list: List[dict]) -> Tuple[List[dict], str]:
    """Call LLM for relations on one topic. Returns (relations, raw)."""
    concepts_block = "\n".join(f"- {c.get('concept','')}  [gloss: {c.get('en','')}]" for c in concept_list)
    prompt = RELATION_PROMPT.format(topic=topic, text=text,
                                    concepts=concepts_block,
                                    types=", ".join(RELATION_TYPES))
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a precise cognitive-linguistics relation extractor. Output only JSON, no reasoning."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=8192,
        timeout=180,
    )
    raw = resp.choices[0].message.content or ""
    rels = _parse_relations(raw)
    # validate types
    valid = [r for r in rels if r.get("type") in RELATION_TYPES]
    return valid, raw


def map_to_edge(rel: dict, concept_gloss: Dict[str, str]) -> Optional[Tuple[str, str, str]]:
    """Map a relation (source/target concept strings) to canonical edge keys.
    Returns (src_key, tgt_key, type) or None if endpoints not mappable."""
    from lds_c_compute import canonical_key
    src_concept = rel.get("source", "")
    tgt_concept = rel.get("target", "")
    src_gloss = concept_gloss.get(src_concept, "")
    tgt_gloss = concept_gloss.get(tgt_concept, "")
    src_key = canonical_key(src_gloss)
    tgt_key = canonical_key(tgt_gloss)
    if not src_key or not tgt_key or src_key == tgt_key:
        return None
    return (src_key, tgt_key, rel.get("type", "relates_to"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    concepts_path = latest_concepts()
    records = load_concepts(concepts_path)
    if args.limit:
        records = records[: args.limit]
    print(f"  Concepts source: {concepts_path}")
    print(f"  Responses: {len(records)}")

    out_dir = PROJECT_ROOT / "data" / "lds_c"
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    out_path = out_dir / (args.out or f"relations_{date_str}.json")

    if args.dry_run:
        n_topics = sum(1 for r in records for t in r.get("topics", []))
        print(f"  Would extract relations for {n_topics} response-topic units")
        return

    key = load_env_key()
    if not key:
        sys.exit("ERROR: OPENAI_API_KEY not found")
    from openai import OpenAI
    client = OpenAI(base_url=API_URL, api_key=key)

    # resume
    done_ids = set()
    existing_rels = []
    if out_path.exists():
        prev = json.loads(out_path.read_text(encoding="utf-8"))
        existing_rels = prev.get("responses", [])
        done_ids = {r["response_id"] for r in existing_rels if r.get("relations")}
        print(f"  Resume: {len(done_ids)} responses already have relations")

    from lds_c_compute import canonical_key  # noqa: F401 (used in map_to_edge)

    results = []
    t0 = time.time()
    for idx, rec in enumerate(records, 1):
        rid = rec["response_id"]
        if rid in done_ids:
            print(f"  [{idx}/{len(records)}] {rid} skip (done)")
            continue
        # build concept_gloss map: concept string -> gloss
        answers = _load_answers(rid)
        topic_relations = []
        for t in rec.get("topics", []):
            topic = t.get("topic", "")
            concepts = t.get("concepts", [])
            if not concepts:
                continue
            concept_gloss = {c.get("concept", ""): (c.get("en", "") or "") for c in concepts}
            text = answers.get(topic, "") if answers else ""
            if not text:
                continue
            rels, raw = None, ""
            for attempt in range(3):
                rels, raw = call_relations(client, topic, text, concepts)
                if rels is not None:
                    break
                if attempt < 2:
                    print(f"    [retry {attempt + 1}] {topic}", flush=True)
                    time.sleep(1.5)
            mapped = []
            for r in rels or []:
                e = map_to_edge(r, concept_gloss)
                if e:
                    mapped.append({"source": e[0], "target": e[1], "type": e[2]})
            topic_relations.append({"topic": topic, "relations": mapped, "raw_len": len(raw or "")})
        n_edges = sum(len(tr["relations"]) for tr in topic_relations)
        print(f"  [{idx}/{len(records)}] {rid}: {n_edges} edges ({time.time()-t0:.0f}s elapsed)", flush=True)
        results.append({"response_id": rid, "language": rec["language"], "topic_relations": topic_relations})
        out_path.write_text(json.dumps({
            "model": MODEL, "api_url": API_URL, "source_concepts": str(concepts_path),
            "extracted_at": datetime.now().isoformat(),
            "responses": results + [r for r in existing_rels if r["response_id"] not in done_ids],
        }, ensure_ascii=False, indent=1), encoding="utf-8")

    # merge existing + new
    merged = {r["response_id"]: r for r in existing_rels}
    for r in results:
        merged[r["response_id"]] = r
    out_path.write_text(json.dumps({
        "model": MODEL, "api_url": API_URL, "source_concepts": str(concepts_path),
        "extracted_at": datetime.now().isoformat(),
        "responses": list(merged.values()),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Done in {time.time()-t0:.0f}s. Saved: {out_path}")


def _load_answers(rid: str) -> Dict[str, str]:
    """Fetch response texts for a response_id from the freeze SSOT."""
    import csv
    answers: Dict[str, str] = {}
    topics = ["Freiheit", "Gerechtigkeit", "Verantwortung", "Heimat", "Erfolg"]
    for tag in ["freeze_survey_20260703", "freeze_survey_20260712"]:
        path = PROJECT_ROOT / "freeze" / tag / "eligible.csv"
        if not path.exists():
            continue
        for row in csv.DictReader(path.open(encoding="utf-8")):
            if row["response_id"] == rid:
                for i, t in enumerate(topics):
                    answers[t] = (row.get(f"q{i+1}", "") or "").strip()
                return answers
    return answers


if __name__ == "__main__":
    main()

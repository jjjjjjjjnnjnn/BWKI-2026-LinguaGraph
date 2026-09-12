"""Merge sidecar grounding evidence back into the main expert graphs (P0-A).

Reads:
  config/expert_graphs/text_grounding_20260912.json            (substring layer)
  config/expert_graphs/text_grounding_en_semantic_20260912.json (semantic layer)

Writes per-concept `verification` field into:
  config/expert_graphs/physics_full.json
  config/expert_graphs/chemistry_full.json

verification schema:
  {zh_pages: [{file, term, count}],
   en_pages: [{file, term, count}],
   semantic_hits: [{file, sent}],
   merged_at: "YYYY-MM-DD"}

Match key: concept `name` (exact string match against sidecar `name`).
Nodes with no sidecar entry or with zero evidence on all three lists are
collected into the unmatched list (count + first 10 printed, no abort).
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH_DIR = ROOT / "config" / "expert_graphs"
SUBSTRING_FILE = GRAPH_DIR / "text_grounding_20260912.json"
SEMANTIC_FILE = GRAPH_DIR / "text_grounding_en_semantic_20260912.json"

TARGETS = {
    "physics": GRAPH_DIR / "physics_full.json",
    "chemistry": GRAPH_DIR / "chemistry_full.json",
}


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    merged_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    sub = load_json(SUBSTRING_FILE)
    sem = load_json(SEMANTIC_FILE)

    # name -> grounding item (substring layer), scoped per graph
    grounding = {}  # (graph, name) -> item
    for graph_key, gdata in sub.get("graphs", {}).items():
        for item in gdata.get("items", []):
            grounding[(graph_key, item.get("name"))] = item

    # name -> semantic evidence (only hits carry evidence)
    semantic = {}  # (graph, name) -> {file, sent}
    for r in sem.get("results", []):
        if r.get("semantic_hit") and r.get("evidence"):
            ev = r["evidence"]
            semantic[(r.get("graph"), r.get("name"))] = {
                "file": ev.get("file"),
                "sent": ev.get("sent"),
            }

    summary = {}
    for graph_key, path in TARGETS.items():
        data = load_json(path)
        concepts = data.get("concepts", [])
        unmatched = []
        n_with_verification = 0
        for node in concepts:
            name = node.get("name")
            item = grounding.get((graph_key, name))
            zh_pages = [
                {"file": e.get("file"), "term": e.get("term"), "count": e.get("count")}
                for e in (item.get("zh_grounded", []) if item else [])
            ]
            en_pages = [
                {"file": e.get("file"), "term": e.get("term"), "count": e.get("count")}
                for e in (item.get("en_grounded", []) if item else [])
            ]
            sem_ev = semantic.get((graph_key, name))
            semantic_hits = [sem_ev] if sem_ev else []

            node["verification"] = {
                "zh_pages": zh_pages,
                "en_pages": en_pages,
                "semantic_hits": semantic_hits,
                "merged_at": merged_at,
            }
            if zh_pages or en_pages or semantic_hits:
                n_with_verification += 1
            else:
                unmatched.append(name)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        summary[graph_key] = {
            "total": len(concepts),
            "with_verification": n_with_verification,
            "unmatched": unmatched,
        }
        print(f"[{graph_key}] total={len(concepts)} "
              f"with_verification={n_with_verification} "
              f"unmatched={len(unmatched)}")
        if unmatched:
            print(f"[{graph_key}] unmatched first 10: {unmatched[:10]}")

    # spot check: first concept with a semantic hit per graph, else first concept
    for graph_key, path in TARGETS.items():
        data = load_json(path)
        concepts = data.get("concepts", [])
        pick = next((n for n in concepts if n.get("verification", {}).get("semantic_hits")),
                    concepts[0] if concepts else None)
        if pick is not None:
            print(f"--- spot [{graph_key}] {pick.get('name')} ---")
            print(json.dumps(pick.get("verification"), ensure_ascii=False)[:1000])
    return 0


if __name__ == "__main__":
    sys.exit(main())

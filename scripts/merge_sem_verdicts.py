"""Merge 10 shard verdicts into text_grounding_en_semantic_20260912.json + rates."""
import glob
import json
from pathlib import Path

D = Path("C:/Users/rongj/AppData/Local/Temp/opencode/sem_shards")
results = []
for f in sorted(glob.glob(str(D / "verdict_*.json"))):
    results.extend(json.loads(Path(f).read_text(encoding="utf-8")))
print("verdicts:", len(results))

g = json.loads(Path("config/expert_graphs/text_grounding_20260912.json")
               .read_text(encoding="utf-8"))
by_name = {n["name"]: n for gk in ("physics", "chemistry")
           for n in g["graphs"][gk]["items"]}
assert len(results) == 407, len(results)
for r in results:
    assert r["name"] in by_name, r["name"]

out = {"date": "2026-09-12",
       "method": "nomic-embed-v1.5 prefilter (top-5) + "
                 "muse-spark-1.3-contributor adjudication, 10 parallel judges; "
                 "substantive-description rule, passing mentions rejected",
       "results": results}
Path("config/expert_graphs/text_grounding_en_semantic_20260912.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

for gk in ("physics", "chemistry"):
    sub = [r["name"] for r in g["graphs"][gk]["items"]]
    n = len(sub)
    sub_h = sum(1 for r in g["graphs"][gk]["items"] if r["en_grounded"])
    sem = [r for r in results if r["graph"] == gk and r["semantic_hit"]]
    total = sub_h + len(sem)
    print(f"{gk}: substr {sub_h}/{n} + semantic {len(sem)} -> "
          f"EN {total}/{n} = {total/n:.1%}")
print("total semantic hits:", sum(1 for r in results if r["semantic_hit"]))

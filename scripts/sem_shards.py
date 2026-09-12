"""P1 prep: embedding-prefilter top-5 candidates for all ungrounded EN nodes,
write adjudication shards for parallel Spark judges.
Usage: python scripts/sem_shards.py [--n 10]
Reads Temp/sem_emb_cache.json (fast, no new embeddings except labels).
Writes Temp/sem_shards/shard_XX.json + manifest.
"""
import argparse
import glob
import json
import math
import re
import urllib.request
from pathlib import Path

LM = "http://127.0.0.1:1234/v1"
EMB_MODEL = "text-embedding-nomic-embed-text-v1.5"
CACHE = Path("C:/Users/rongj/AppData/Local/Temp/opencode/sem_emb_cache.json")
SHARD_DIR = Path("C:/Users/rongj/AppData/Local/Temp/opencode/sem_shards")


def post(path: str, payload: dict, timeout: int = 300) -> dict:
    req = urllib.request.Request(
        LM + path, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def sentences(text: str) -> list:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text)
    out, seen = [], set()
    for p in parts:
        p = re.sub(r"\s+", " ", p).strip()
        if 40 <= len(p) <= 500 and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def cos(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    a = ap.parse_args()
    g = json.loads(Path("config/expert_graphs/text_grounding_20260912.json")
                   .read_text(encoding="utf-8"))
    targets = []
    for gk in ("physics", "chemistry"):
        for n in g["graphs"][gk]["items"]:
            if not n["en_grounded"] and n["en"]:
                targets.append({"graph": gk, "name": n["name"],
                                "en": n["en"], "zh": n["zh"]})
    print(f"targets: {len(targets)}")
    files = sorted(glob.glob("data/textbook/open/en_openstax_*sec*.txt")) + sorted(
        glob.glob("data/textbook/en_mit801_notes_ch*.txt"))
    corpus = []
    for f in files:
        for s in sentences(Path(f).read_text(encoding="utf-8")):
            corpus.append({"file": Path(f).name, "sent": s})
    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    for c in corpus:
        c["vec"] = cache[c["sent"]]
    print(f"corpus: {len(corpus)}")
    label_vecs = {}
    shard_items = []
    for t in targets:
        if t["en"] not in label_vecs:
            d = post("/embeddings", {"model": EMB_MODEL, "input": [t["en"]]})
            label_vecs[t["en"]] = d["data"][0]["embedding"]
        lv = label_vecs[t["en"]]
        top = sorted(((cos(lv, c["vec"]), c) for c in corpus),
                     key=lambda x: -x[0])[:5]
        shard_items.append({"name": t["name"], "graph": t["graph"],
                            "en": t["en"], "zh": t["zh"],
                            "cands": [{"file": c["file"], "sent": c["sent"],
                                       "cos": round(s, 4)}
                                      for s, c in top]})
    SHARD_DIR.mkdir(parents=True, exist_ok=True)
    per = math.ceil(len(shard_items) / a.n)
    manifest = []
    for i in range(a.n):
        chunk = shard_items[i * per:(i + 1) * per]
        if not chunk:
            continue
        p = SHARD_DIR / f"shard_{i:02d}.json"
        p.write_text(json.dumps(chunk, ensure_ascii=False, indent=1),
                     encoding="utf-8")
        manifest.append({"shard": p.name, "nodes": len(chunk)})
        print(f"wrote {p.name}: {len(chunk)} nodes")
    (SHARD_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

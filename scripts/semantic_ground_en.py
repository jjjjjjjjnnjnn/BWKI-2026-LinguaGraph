"""P1 EN semantic grounding: LM Studio embeddings prefilter + phi-4-mini adjudication.
Layers kept separate from substring grounding (no number mixing).
Usage:
  python scripts/semantic_ground_en.py --test     # 5 nodes smoke test
  python scripts/semantic_ground_en.py --full     # all ungrounded EN nodes
Needs LM Studio server at 127.0.0.1:1234 with text-embedding-nomic-embed-text-v1.5
and phi-4-mini-instruct loaded. Temp 0, seeds fixed where possible.
Writes config/expert_graphs/text_grounding_en_semantic_20260912.json (resume-safe).
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
CHAT_MODEL = "phi-4-mini-instruct"
CACHE = Path("C:/Users/rongj/AppData/Local/Temp/opencode/sem_emb_cache.json")
OUT = Path("config/expert_graphs/text_grounding_en_semantic_20260912.json")


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


def load_corpus() -> list:
    files = sorted(glob.glob("data/textbook/open/en_openstax_*sec*.txt")) + sorted(
        glob.glob("data/textbook/en_mit801_notes_ch*.txt"))
    items = []
    for f in files:
        for s in sentences(Path(f).read_text(encoding="utf-8")):
            items.append({"file": Path(f).name, "sent": s})
    return items


def embed(texts: list, batch: int = 32) -> list:
    vecs = []
    for i in range(0, len(texts), batch):
        d = post("/embeddings", {"model": EMB_MODEL,
                                 "input": texts[i:i + batch]}, timeout=600)
        vecs.extend([e["embedding"] for e in d["data"]])
        if (i // batch) % 20 == 0:
            print(f"  emb {i}/{len(texts)}", flush=True)
    return vecs


def cos(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


ADJ_SYS = ("You are a physics/chemistry textbook grounding judge. "
           "Answer with a single digit only.")


def adjudicate(label: str, cands: list) -> int:
    numbered = "\n".join(f"{i + 1}. {c['sent'][:300]}"
                         for i, c in enumerate(cands))
    prompt = (f"Concept: {label}\nWhich numbered sentence describes this "
              f"concept (same phenomenon, synonyms allowed)?\n{numbered}\n"
              f"Answer with the number only, or 0 if none matches.")
    d = post("/chat/completions",
             {"model": CHAT_MODEL, "temperature": 0, "max_tokens": 5,
              "messages": [{"role": "system", "content": ADJ_SYS},
                           {"role": "user", "content": prompt}]},
             timeout=600)
    m = re.search(r"[0-5]", d["choices"][0]["message"]["content"] or "")
    return int(m.group(0)) if m else 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--full", action="store_true")
    a = ap.parse_args()

    g = json.loads(Path("config/expert_graphs/text_grounding_20260912.json")
                   .read_text(encoding="utf-8"))
    targets = []
    for gk in ("physics", "chemistry"):
        for n in g["graphs"][gk]["items"]:
            if not n["en_grounded"] and n["en"]:
                targets.append({"graph": gk, "name": n["name"],
                                "en": n["en"]})
    print(f"ungrounded EN nodes: {len(targets)}")
    if a.test:
        targets = targets[:5]

    corpus = load_corpus()
    print(f"corpus sentences: {len(corpus)}")
    if CACHE.exists():
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
        print(f"cache hit: {len(cache)} vecs")
    else:
        cache = {}
    texts = [c["sent"] for c in corpus]
    missing = [t for t in texts if t not in cache]
    print(f"embedding {len(missing)} new sentences...")
    new_vecs = embed(missing)
    for t, v in zip(missing, new_vecs):
        cache[t] = v
    CACHE.write_text(json.dumps(cache), encoding="utf-8")
    for c in corpus:
        c["vec"] = cache[c["sent"]]

    done = {}
    if OUT.exists():
        for r in json.loads(OUT.read_text(encoding="utf-8"))["results"]:
            done[r["name"]] = r
    print(f"resuming: {len(done)} done")
    results = list(done.values())
    label_vecs = {}
    for t in targets:
        if t["name"] in done:
            continue
        if t["en"] not in label_vecs:
            label_vecs[t["en"]] = embed([t["en"]])[0]
        lv = label_vecs[t["en"]]
        scored = sorted(((cos(lv, c["vec"]), c) for c in corpus),
                        key=lambda x: -x[0])[:5]
        cands = [c for _, c in scored]
        pick = adjudicate(t["en"], cands)
        r = {"name": t["name"], "graph": t["graph"], "en": t["en"],
             "semantic_hit": pick > 0,
             "evidence": ({k: cands[pick - 1][k] for k in ("file", "sent")}
                          if pick > 0 else None),
             "top_cos": round(scored[0][0], 4),
             "model": CHAT_MODEL, "temperature": 0}
        results.append(r)
        print(f"{'HIT' if pick else 'miss'} {t['graph']}/{t['name']} "
              f"cos={scored[0][0]:.3f}", flush=True)
        OUT.write_text(json.dumps(
            {"date": "2026-09-12", "method": "embedding-prefilter + "
             f"{CHAT_MODEL} adjudication (temp 0)",
             "results": results}, ensure_ascii=False, indent=1),
            encoding="utf-8")
    hits = sum(1 for r in results if r["semantic_hit"])
    print(f"semantic hits: {hits}/{len(results)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Open-weight embedding audit (Two-Tier Tier-2 / latent-space leg).

Reads all concept names from data/math_extractions/*.json (dedup; if >1200,
stratified round-robin sample per file down to ~800 to bound runtime),
embeds them with a local open-weight model via LM Studio
(http://127.0.0.1:1234/v1, text-embedding-nomic-embed-text-v1.5),
then computes cosine DISTANCE (1 - cos_sim) for cross-lingual synonymous
concept pairs and aggregates mean/std per language pair (zh-de / zh-en / de-en).

Pair source priority:
  1) data/math_extractions/merged/aligned_data.json `aligned_groups[].labels`
     ({zh,en,de} per group -> 3 pairs per group where both labels non-empty
     and normalized forms differ);
  2) fallback: normalized-name + aliases pairing across languages
     (norm = lowercase + strip spaces/hyphens/underscores + ss-mapping),
     language inferred from extraction filename prefix (zh_/en_/de_) or from
     unmatched_concepts[].language. Used only when aligned table is missing
     OR as supplementary pair count (reported separately, never merged
     silently into the primary means).

Only stdlib (urllib). No repo writes: results go to stdout; optional cache
lives OUTSIDE the repo in %TEMP%/opencode/ (never data/ or research/).

Usage:
  python scripts/tools/openweight_embed_audit.py [--smoke] [--limit-pairs N]
  python scripts/tools/openweight_embed_audit.py --full --batch 32
"""
import argparse
import glob
import json
import math
import os
import random
import sys
import tempfile
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXTRACT_GLOB = str(ROOT / "data" / "math_extractions" / "*.json")
ALIGNED_PATH = ROOT / "data" / "math_extractions" / "merged" / "aligned_data.json"

DEFAULT_BASE = "http://127.0.0.1:1234/v1"
DEFAULT_MODEL = "text-embedding-nomic-embed-text-v1.5"
MAX_CONCEPTS = 1200
TARGET_SAMPLE = 800


def norm(s: str) -> str:
    s = (s or "").strip().lower()
    for ch in (" ", "\t", "-", "_", "/", "(", ")", "[", "]", ".", ",", ":", ";"):
        s = s.replace(ch, "")
    s = s.replace("ß", "ss")
    return s


def lang_of_file(path: str) -> str:
    base = os.path.basename(path).lower()
    for lg in ("zh", "en", "de"):
        if base.startswith(lg + "_") or base.startswith(lg + "-"):
            return lg
    return "unk"


def collect_concepts():
    """Return (per_file: {file: [names]}, all_unique: set)."""
    files = sorted(glob.glob(EXTRACT_GLOB))
    per_file = {}
    for f in files:
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] skip {f}: {e}", file=sys.stderr)
            continue
        names = []
        for c in d.get("extracted_concepts", []):
            n = (c.get("name") or "").strip()
            if n:
                names.append(n)
        # dedup preserving order within file
        seen, uniq = set(), []
        for n in names:
            if n not in seen:
                seen.add(n)
                uniq.append(n)
        per_file[f] = uniq
    all_unique = set()
    for v in per_file.values():
        all_unique.update(v)
    return per_file, all_unique


def stratified_sample(per_file, target=TARGET_SAMPLE):
    """Round-robin across files to ~target terms (deterministic, seed 7)."""
    rnd = random.Random(7)
    files = sorted(per_file.keys())
    pools = {f: list(v) for f, v in per_file.items()}
    for v in pools.values():
        rnd.shuffle(v)
    out, idx = [], 0
    total = sum(len(v) for v in pools.values())
    if total <= target:
        for f in files:
            out.extend(pools[f])
        return out, False
    ptr = {f: 0 for f in files}
    while len(out) < target:
        progressed = False
        for f in files:
            if ptr[f] < len(pools[f]) and len(out) < target:
                out.append(pools[f][ptr[f]])
                ptr[f] += 1
                progressed = True
        if not progressed:
            break
    return out, True


def load_aligned_pairs():
    """Primary pairs from aligned_data.json labels. Returns (pairs, n_groups)."""
    pairs = []  # (term_a, lang_a, term_b, lang_b, group_id)
    if not ALIGNED_PATH.exists():
        return pairs, 0
    d = json.load(open(ALIGNED_PATH, encoding="utf-8"))
    groups = d.get("aligned_groups", [])
    for g in groups:
        gid = g.get("id", "?")
        labels = g.get("labels", {}) or {}
        for (la, lb) in (("zh", "de"), ("zh", "en"), ("de", "en")):
            a = (labels.get(la) or "").strip()
            b = (labels.get(lb) or "").strip()
            if not a or not b:
                continue
            if norm(a) == norm(b):
                continue  # identical surface form -> uninformative for drift
            pairs.append((a, la, b, lb, gid))
    return pairs, len(groups)


def load_fallback_pairs(per_file, aligned_terms):
    """Supplementary pairs: same normalized form, different source languages.

    Built from extraction name+aliases. Returns list of
    (term_a, lang_a, term_b, lang_b, 'norm:'+key). Terms already covered by
    the aligned table (same unordered norm pair) are skipped to avoid
    double counting in reports (counts reported separately anyway).
    """
    norm_map = defaultdict(list)  # norm -> [(term, lang)]
    files = sorted(glob.glob(EXTRACT_GLOB))
    for f in files:
        lg = lang_of_file(f)
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for c in d.get("extracted_concepts", []):
            n = (c.get("name") or "").strip()
            if n:
                norm_map[norm(n)].append((n, lg))
            for a in (c.get("aliases") or []):
                a = (a or "").strip()
                if a:
                    norm_map[norm(a)].append((a, lg))
    # also unmatched_concepts aliases (carry explicit language tags)
    if ALIGNED_PATH.exists():
        try:
            d = json.load(open(ALIGNED_PATH, encoding="utf-8"))
            for u in d.get("unmatched_concepts", []):
                lg = (u.get("language") or "unk").strip().lower()
                for key in ("canonical_name", "name_original"):
                    v = (u.get(key) or "").strip()
                    if v:
                        norm_map[norm(v)].append((v, lg))
                for a in (u.get("aliases") or []):
                    a = (a or "").strip()
                    if a:
                        norm_map[norm(a)].append((a, lg))
        except Exception as e:
            print(f"[WARN] unmatched scan: {e}", file=sys.stderr)
    pairs = []
    for key, items in norm_map.items():
        # distinct (term, lang), need >=2 languages present
        uniq = sorted(set(items))
        langs = {lg for _, lg in uniq}
        langs.discard("unk")
        if len(langs) < 2 or len(uniq) < 2:
            continue
        # one representative term per language (first occurrence)
        rep = {}
        for t, lg in uniq:
            if lg not in rep and lg in ("zh", "en", "de"):
                rep[lg] = t
        lgs = sorted(rep.keys())
        for i in range(len(lgs)):
            for j in range(i + 1, len(lgs)):
                la, lb = lgs[i], lgs[j]
                if rep[la] == rep[lb]:
                    continue
                pairs.append((rep[la], la, rep[lb], lb, "norm:" + key))
    return pairs


def embed_texts(texts, base_url, model, batch=32, timeout=120):
    """POST OpenAI-compatible /v1/embeddings in batches. Returns (vecs, dim)."""
    url = base_url.rstrip("/") + "/embeddings"
    vecs = []
    dim = None
    for i in range(0, len(texts), batch):
        chunk = texts[i:i + batch]
        payload = json.dumps({"model": model, "input": chunk}).encode("utf-8")
        req = urllib.request.Request(url, data=payload,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            print(f"[ERROR] embedding batch @ {i}: {e}", file=sys.stderr)
            raise
        items = body.get("data", [])
        items.sort(key=lambda x: x.get("index", 0))
        for it in items:
            v = it["embedding"]
            if dim is None:
                dim = len(v)
            vecs.append(v)
        print(f"[embed] {min(i + batch, len(texts))}/{len(texts)}", file=sys.stderr)
    return vecs, dim


def cos_dist(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 1.0
    return 1.0 - dot / (na * nb)


def agg(vals):
    n = len(vals)
    if n == 0:
        return {"n": 0}
    m = sum(vals) / n
    var = sum((v - m) ** 2 for v in vals) / n
    return {"n": n, "mean": round(m, 4), "std": round(math.sqrt(var), 4),
            "min": round(min(vals), 4), "max": round(max(vals), 4)}


def pair_key(la, lb):
    s = tuple(sorted([la, lb]))
    if s == ("de", "zh"):
        return "zh-de"
    if s == ("en", "zh"):
        return "zh-en"
    if s == ("de", "en"):
        return "de-en"
    return "-".join(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--smoke", action="store_true",
                    help="embed only pair terms of first 10 aligned groups")
    ap.add_argument("--limit-pairs", type=int, default=0,
                    help="cap primary pairs (0 = no cap)")
    ap.add_argument("--timeout", type=int, default=120)
    a = ap.parse_args()

    per_file, all_unique = collect_concepts()
    print(f"[info] files={len(per_file)} unique_concept_names={len(all_unique)}",
          file=sys.stderr)

    if len(all_unique) > MAX_CONCEPTS:
        sampled, did = stratified_sample(per_file, TARGET_SAMPLE)
        print(f"[info] >{MAX_CONCEPTS}: stratified sample -> {len(sampled)} "
              f"(sampled={did})", file=sys.stderr)
        concept_terms = sampled
    else:
        concept_terms = sorted(all_unique)
        print(f"[info] <={MAX_CONCEPTS}: no sampling, embed all "
              f"{len(concept_terms)}", file=sys.stderr)

    pairs, n_groups = load_aligned_pairs()
    print(f"[info] aligned_groups={n_groups} primary_pairs={len(pairs)}",
          file=sys.stderr)
    fallback = load_fallback_pairs(per_file, None)
    print(f"[info] fallback_norm_pairs={len(fallback)} (supplementary only)",
          file=sys.stderr)

    if a.smoke:
        gids = sorted({p[4] for p in pairs})[:10]
        pairs = [p for p in pairs if p[4] in set(gids)]
        print(f"[info] SMOKE: pairs capped to {len(pairs)}", file=sys.stderr)
    if a.limit_pairs and len(pairs) > a.limit_pairs:
        pairs = pairs[:a.limit_pairs]
        print(f"[info] pairs limited to {len(pairs)}", file=sys.stderr)

    # union of terms to embed: sampled concepts + every pair term (priority)
    need = set(concept_terms)
    for (t1, _, t2, _, _) in pairs:
        need.add(t1)
        need.add(t2)
    texts = sorted(need)
    print(f"[info] embedding {len(texts)} unique terms "
          f"(concepts={len(concept_terms)}, pair_terms_extra="
          f"{len(texts) - len(set(concept_terms) & need)})", file=sys.stderr)

    vecs, dim = embed_texts(texts, a.base_url, a.model,
                            batch=a.batch, timeout=a.timeout)
    V = dict(zip(texts, vecs))
    print(f"[info] embedded dim={dim}", file=sys.stderr)

    by_pair = defaultdict(list)
    missing = 0
    for (t1, la, t2, lb, gid) in pairs:
        if t1 not in V or t2 not in V:
            missing += 1
            continue
        by_pair[pair_key(la, lb)].append(cos_dist(V[t1], V[t2]))

    summary = {k: agg(v) for k, v in sorted(by_pair.items())}
    allv = [v for vs in by_pair.values() for v in vs]
    summary["_overall"] = agg(allv)

    out = {
        "model": a.model,
        "base_url": a.base_url,
        "dim": dim,
        "n_files": len(per_file),
        "n_unique_concept_names": len(all_unique),
        "n_embedded_terms": len(texts),
        "sampled": len(all_unique) > MAX_CONCEPTS,
        "aligned_groups": n_groups,
        "primary_pairs_used": len(pairs) - missing,
        "primary_pairs_missing": missing,
        "fallback_pairs_available": len(fallback),
        "drift_cosine_distance": summary,
        "expectation_registered": ("vector space uniform/low-variance vs "
                                   "textbook graph structured/high-variance; "
                                   "measured values rule"),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

    # optional cache OUTSIDE repo (Temp), never data/ or research/
    try:
        cache_dir = Path(tempfile.gettempdir()) / "opencode"
        cache_dir.mkdir(parents=True, exist_ok=True)
        cp = cache_dir / "openweight_embed_audit.json"
        cp.write_text(json.dumps(out, ensure_ascii=False, indent=2),
                      encoding="utf-8")
        print(f"[info] cache -> {cp}", file=sys.stderr)
    except Exception as e:
        print(f"[WARN] cache skip: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Phase-3: linear CKA + RSA second-order triangulation (pre-registered §2.6).

CKA: linear CKA between per-language embedding matrices on SHARED gid terms
(X_zh, X_en, X_de; rows aligned by gid) -> cross-lingual geometric similarity
of weight space. Unbiased HSIC estimator (Song et al.), linear kernel.
RSA: Spearman between embedding cosine-distance ranks and textbook
graph-distance ranks (shortest-path over textbook concept graph, per lang;
unreachable = max+1), over shared-gid term pairs.
Output: research/weight_cka_rsa_20260916.json (+ stdout).
Read-only contract: writes ONLY that file. Exploratory appendix-only.
Usage: python scripts/tools/weight_cka_rsa.py [--help]
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(BASE, "research", "weight_cka_rsa_20260916.json")


def linear_cka(X, Y):
    import numpy as np
    Xc = X - X.mean(0, keepdims=True)
    Yc = Y - Y.mean(0, keepdims=True)
    hsic = float(np.sum((Xc @ Xc.T) * (Yc @ Yc.T)))
    nx = float(np.sum((Xc @ Xc.T) ** 2))
    ny = float(np.sum((Yc @ Yc.T) ** 2))
    return hsic / ((nx * ny) ** 0.5) if nx > 0 and ny > 0 else float("nan")


def main():
    import numpy as np
    from collections import deque
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: weight_cka_rsa.py [--help]")
        return 0
    sys.path.insert(0, os.path.join(BASE, "scripts", "tools"))
    import weight_graph_E3 as E3
    from pathlib import Path
    E3.guard_output(Path(OUT))
    groups = json.loads(E3.ALIGNED_PATH.read_text(encoding="utf-8"))["aligned_groups"]
    vec_map = json.loads(E3.VECTORS_PATH.read_text(encoding="utf-8"))
    rows = [(g.get("id", "?"), {l: ((g.get("labels", {}) or {}).get(l) or "").strip()
                                for l in E3.LANGS}) for g in groups]
    first = {}
    for (gid, labs) in rows:
        if gid not in first:
            first[gid] = labs
    shared = [gid for gid, labs in first.items()
              if all(labs[l] in vec_map for l in E3.LANGS)]
    M = {l: np.array([vec_map[first[g][l]] for g in shared], dtype=np.float64)
         for l in E3.LANGS}
    cka = {}
    for (la, lb) in E3.PAIRS:
        cka[f"{la}-{lb}"] = round(linear_cka(M[la], M[lb]), 4)
        print("CKA-linear %s-%s = %.4f (n=%d)" % (la, lb, cka[f"{la}-{lb}"], len(shared)))
    # RSA: textbook graph distances per lang from math_extractions relation tables
    import glob
    adj = {l: {} for l in E3.LANGS}
    for fp in glob.glob(os.path.join(BASE, "data", "math_extractions", "*.json")):
        try:
            d = json.load(open(fp, encoding="utf-8"))
        except Exception:
            continue
        lang = None
        for l, pre in (("zh", "zh_"), ("en", "en_"), ("de", "de_")):
            if os.path.basename(fp).startswith(pre):
                lang = l
        if lang is None:
            continue
        names = {c.get("name", "") for c in d.get("extracted_concepts", []) if isinstance(c, dict)}
        for r in d.get("extracted_relations", []):
            a, b = r.get("source", ""), r.get("target", "")
            if a in names and b in names:
                adj[lang].setdefault(a, set()).add(b)
                adj[lang].setdefault(b, set()).add(a)
    rsa = {}
    for lang in E3.LANGS:
        terms = [first[g][lang] for g in shared]
        # embedding distances
        V = M[lang]
        n = len(terms)
        emb, gra = [], []
        for i in range(n):
            dist = {terms[i]: 0}
            dq = deque([terms[i]])
            while dq:
                u = dq.popleft()
                for w in adj[lang].get(u, ()):
                    if w not in dist:
                        dist[w] = dist[u] + 1
                        dq.append(w)
            vi = V[i] / (np.linalg.norm(V[i]) + 1e-12)
            for j in range(i + 1, n):
                vj = V[j] / (np.linalg.norm(V[j]) + 1e-12)
                emb.append(float(1 - vi @ vj))
                gra.append(dist.get(terms[j], n + 1))
        # Spearman via ranks
        ea = np.argsort(np.argsort(emb)).astype(float)
        ga = np.argsort(np.argsort(gra)).astype(float)
        ea -= ea.mean()
        ga -= ga.mean()
        rho = float(ea @ ga / ((ea @ ea * ga @ ga) ** 0.5 + 1e-12))
        rsa[lang] = {"rho_emb_vs_graphdist": round(rho, 4), "n_pairs": len(emb),
                     "note": "descriptive only; graph distances sparse (unreachable=max+1)"}
        print("RSA %s rho=%.4f pairs=%d" % (lang, rho, len(emb)))
    json.dump({"linear_cka_shared_gids": cka, "n_shared": len(shared), "rsa": rsa,
               "status": "EXECUTED (measurement); interpretation Hypothesis/PENDING"},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("WROTE", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())

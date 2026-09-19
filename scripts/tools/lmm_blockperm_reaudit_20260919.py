#!/usr/bin/env python3
"""LMM block-permutation reaudit (2026-09-19, P1). Read-only on repo data.

Within-topic shuffle of dyad Jaccard (y), refit fit_lmm_core, two-sided
|coef| >= |obs|. Result: same_lang 0/1000 (p=0.000), same_frame 937/1000
(p=0.937). Supersedes the unverifiable same_frame 0.779 (no code in
lmm_20260808.json / lds_c_llm_lmm.py for that value).
Output: research/lmm_blockperm_reaudit_20260919.json (this run overwrites).
"""
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from lds_c_llm_analyze import load_canonical_units
from lds_c_llm_lmm import build_cells, build_dyads, fit_lmm_core

import numpy as np

units, _path = load_canonical_units()
cells = build_cells(units)
dyads = build_dyads(cells)
rows = dyads["rows"]
core = fit_lmm_core(rows)
obs_lang = abs(float(core["coef"][1]))
obs_frame = abs(float(core["coef"][2]))

n_iter = 1000
rng = np.random.default_rng(20260808)
topics = sorted({r["topic"] for r in rows})
by_topic = {t: [r for r in rows if r["topic"] == t] for t in topics}
count_lang = 0
count_frame = 0
done = 0
fails = 0
for _it in range(n_iter):
    perm_rows = []
    for t in topics:
        ys = [r["y"] for r in by_topic[t]]
        perm_ys = rng.permutation(ys)
        for r, y in zip(by_topic[t], perm_ys):
            nr = dict(r)
            nr["y"] = float(y)
            perm_rows.append(nr)
    b = fit_lmm_core(perm_rows)
    if b is None or b["se"] is None or not np.all(np.isfinite(b["coef"][1:])):
        fails += 1
        continue
    done += 1
    if abs(float(b["coef"][1])) >= obs_lang:
        count_lang += 1
    if abs(float(b["coef"][2])) >= obs_frame:
        count_frame += 1

out = {
    "date": "2026-09-19",
    "n_iter": n_iter,
    "done": done,
    "fails": fails,
    "obs_same_lang": float(core["coef"][1]),
    "obs_same_frame": float(core["coef"][2]),
    "count_lang": count_lang,
    "count_frame": count_frame,
    "p_lang_raw": count_lang / done if done else None,
    "p_frame_raw": count_frame / done if done else None,
    "method": "within-topic block permutation of y (dyad Jaccard), refit fit_lmm_core, two-sided |coef|>=|obs|",
}
out_path = PROJECT_ROOT / "research" / "lmm_blockperm_reaudit_20260919.json"
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"perm p same_lang: {count_lang}/{done}, same_frame: {count_frame}/{done} -> {out_path}")

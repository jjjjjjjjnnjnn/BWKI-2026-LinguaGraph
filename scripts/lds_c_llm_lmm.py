#!/usr/bin/env python3
"""LinguaGraph — D1: LMM for language x frame marginal contributions.

Dyadic cell-pair design. Cells (code, frame) from P1 (natural) + P2 (crossed):
  zh/natural, de/natural, en/natural, zh/de-frame, de/zh-frame
For each topic t and each pair of cells (a,b), the response is the concept-set
Jaccard similarity between the two aggregated cells on topic t.

Predictors (dyadic, both 0/1):
  same_lang  : 1 if cells share language code
  same_frame : 1 if cells share cultural frame (natural->own language)
Identified via the crossed cells:
  same code, diff frame : (zh/nat, zh/de), (de/nat, de/zh)      -> frame effect
  diff code, same frame : (zh/nat, de/zh), (de/nat, zh/de)      -> language effect

Model: y ~ same_lang + same_frame + (1|topic)
Fitted by maximum marginal likelihood (random intercept per topic), closed-form
blocked V (compound-symmetry). scipy.optimize, no statsmodels dependency.

Interpretation of coefficients (on Jaccard similarity, higher = more similar):
  beta_same_lang  : marginal similarity gain from sharing language code
  beta_same_frame : marginal similarity gain from sharing cultural frame
If beta_same_frame > beta_same_lang -> frame is the dominant driver (M3).

Output: data/lds_c/llm_subject/lmm_<date>.json + console.
"""

from __future__ import annotations

import json
import math
import sys
import time
from collections import defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from scipy import optimize, stats

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import canonical_key  # noqa: E402
from lds_c_llm_analyze import OUT_DIR  # noqa: E402

TOPICS = ["Freiheit", "Gerechtigkeit", "Verantwortung", "Heimat", "Erfolg"]
NATURAL_FRAME = {"zh": "zh", "de": "de", "en": "en"}  # natural frame = own language


# ── Data construction ───────────────────────────────────────────────
def build_cells(units: List[dict]) -> Dict[Tuple[str, str], Dict[str, set]]:
    """(code, frame) -> topic -> set of canonical concept keys."""
    cells: Dict[Tuple[str, str], Dict[str, set]] = defaultdict(lambda: defaultdict(set))
    for u in units:
        if u["probe"] not in ("P1", "P2"):
            continue
        code = u["language"]
        frame = "natural" if u["probe"] == "P1" else u.get("frame", "natural")
        f = NATURAL_FRAME.get(code, code) if frame == "natural" else frame
        for t, concepts in u.get("concepts", {}).items():
            if t not in TOPICS:
                continue
            for c in concepts:
                k = canonical_key(c.get("en", ""))
                if k:
                    cells[(code, f)][t].add(k)
    return dict(cells)


def jaccard(a: set, b: set) -> float:
    u = a | b
    return len(a & b) / len(u) if u else float("nan")


def build_dyads(cells: Dict[Tuple[str, str], Dict[str, set]]) -> dict:
    """Rows: topic, cell_a, cell_b, same_lang, same_frame, y=Jaccard."""
    rows = []
    cell_list = sorted(cells.keys())
    for topic in TOPICS:
        for a, b in combinations(cell_list, 2):
            if topic not in cells[a] or topic not in cells[b]:
                continue
            ya, yb = cells[a][topic], cells[b][topic]
            y = jaccard(ya, yb)
            if y != y:
                continue
            same_lang = 1 if a[0] == b[0] else 0
            same_frame = 1 if a[1] == b[1] else 0
            rows.append({
                "topic": topic, "cell_a": a, "cell_b": b,
                "same_lang": same_lang, "same_frame": same_frame,
                "y": y,
            })
    return {"rows": rows, "cell_list": cell_list,
            "n": len(rows), "n_topics": len(TOPICS),
            "mean_y": float(np.mean([r["y"] for r in rows])),
            "frac_zero_y": float(np.mean([r["y"] == 0 for r in rows]))}


# ── LMM fit (random intercept per topic, ML marginal) ───────────────
def fit_lmm(rows: List[dict]) -> dict:
    """y ~ same_lang + same_frame + (1|topic). ML via scipy minimize.

    V is block-diagonal over topics with compound-symmetry blocks.
    Parameters: beta = [intercept, same_lang, same_frame], log_sigma2, log_tau2.
    """
    topics = sorted({r["topic"] for r in rows})
    topic_idx = {t: i for i, t in enumerate(topics)}
    n = len(rows)
    X = np.zeros((n, 3))
    y = np.zeros(n)
    g = np.zeros(n, dtype=int)          # group (topic) index per row
    for i, r in enumerate(rows):
        X[i] = [1.0, r["same_lang"], r["same_frame"]]
        y[i] = r["y"]
        g[i] = topic_idx[r["topic"]]

    # block sizes per topic
    n_g = np.array([np.sum(g == gi) for gi in range(len(topics))], dtype=float)

    def neg_ll(theta: np.ndarray) -> float:
        beta = theta[:3]
        sigma2 = np.exp(theta[3])
        tau2 = np.exp(theta[4])
        # y - X beta, and per-group sums of residual for the J-block term
        r = y - X @ beta
        r_sum = np.zeros(len(topics))
        for gi in range(len(topics)):
            r_sum[gi] = np.sum(r[g == gi])
        # log|V| and quadratic form, per topic block (compound symmetry)
        logdet = 0.0
        quad = 0.0
        for gi in range(len(topics)):
            m = n_g[gi]
            s2_block = sigma2 + m * tau2
            logdet += (m - 1) * math.log(sigma2) + math.log(s2_block)
            ss = np.sum((r[g == gi]) ** 2)
            quad += ss / sigma2 - (tau2 / (sigma2 * s2_block)) * (r_sum[gi] ** 2)
        ll = -0.5 * (n * math.log(2 * math.pi) + logdet + quad)
        return -ll

    # starting values
    b0 = float(np.mean(y))
    theta0 = np.array([b0, 0.0, 0.0, math.log(0.1), math.log(0.01)])

    # fit
    res = optimize.minimize(neg_ll, theta0, method="Nelder-Mead",
                            options={"maxiter": 5000, "xatol": 1e-8, "fatol": 1e-8})
    theta = res.x
    beta = theta[:3]
    sigma2 = float(np.exp(theta[3]))
    tau2 = float(np.exp(theta[4]))

    # hessian at optimum for SEs (via finite differences on neg_ll)
    hess = approx_hess(theta, neg_ll)
    try:
        cov = np.linalg.inv(hess)
        se = np.sqrt(np.clip(np.diag(cov)[:3], 1e-12, None))
    except np.linalg.LinAlgError:
        se = np.full(3, np.nan)

    names = ["intercept", "same_lang", "same_frame"]
    params = {names[i]: {"coef": float(beta[i]), "se": float(se[i]),
                         "t": float(beta[i] / se[i]) if se[i] and se[i] == se[i] else float("nan"),
                         "p": float(2 * stats.t.sf(abs(beta[i] / se[i]), n - 3))
                               if se[i] and se[i] == se[i] else float("nan")}
              for i in range(3)}
    return {
        "n": n, "n_topics": len(topics), "converged": res.success,
        "iterations": res.nit, "neg_ll_min": float(res.fun),
        "sigma2_resid": sigma2, "tau2_topic": tau2,
        "params": params,
        "design": {
            "n_same_lang": int(np.sum(X[:, 1])),
            "n_same_frame": int(np.sum(X[:, 2])),
        },
        "model": "y ~ same_lang + same_frame + (1|topic)  [ML marginal, scipy]",
    }


def approx_hess(theta: np.ndarray, fn, eps: float = 1e-4):
    k = len(theta)
    H = np.zeros((k, k))
    for i in range(k):
        for j in range(i, k):
            ti = np.array(theta); ti[i] += eps
            tj = np.array(theta); tj[j] += eps
            tij = np.array(theta); tij[i] += eps; tij[j] += eps
            f0 = fn(theta)
            fi = fn(ti); fj = fn(tj); fij = fn(tij)
            H[i, j] = H[j, i] = (fij - fi - fj + f0) / (eps * eps)
    return H


def main() -> None:
    import sys as _sys
    data_file = _sys.argv[1] if len(_sys.argv) > 1 else None
    if data_file:
        units = json.loads(Path(data_file).read_text(encoding="utf-8"))["units"]
    else:
        from lds_c_llm_analyze import latest_units
        units = latest_units()

    print(f"  Loaded {len(units)} units")
    cells = build_cells(units)
    print(f"  Cells: {sorted(cells.keys())}")
    dyads = build_dyads(cells)
    print(f"  Dyads: n={dyads['n']}, mean J={dyads['mean_y']:.4f}, "
          f"frac_zero={dyads['frac_zero_y']:.3f}")
    if not dyads["rows"]:
        print("  ERROR: no dyads")
        sys.exit(1)

    print("  Fitting LMM (y ~ same_lang + same_frame + (1|topic))...")
    result = fit_lmm(dyads["rows"])
    result["dyads"] = dyads
    result["generated_at"] = datetime.now().isoformat()

    out_path = OUT_DIR / f"lmm_{datetime.now().strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")
    print("\n=== LMM results ===")
    print(f"  n={result['n']} dyads, {result['n_topics']} topics, "
          f"converged={result['converged']}")
    print(f"  sigma2_resid={result['sigma2_resid']:.4f}  tau2_topic={result['tau2_topic']:.4f}")
    print("  Fixed effects (on Jaccard similarity; higher coef = more similar when sharing):")
    for k, v in result["params"].items():
        print(f"    {k:12s} coef={v['coef']:+.4f}  se={v['se']:.4f}  "
              f"t={v['t']:+.2f}  p={v['p']:.3f}")
    p_sl = result["params"]["same_lang"]["p"]
    p_sf = result["params"]["same_frame"]["p"]
    c_sl = result["params"]["same_lang"]["coef"]
    c_sf = result["params"]["same_frame"]["coef"]
    print("\n  Interpretation:")
    print(f"    same_lang  : sharing language code raises Jaccard by {c_sl:+.4f} (p={p_sl:.3f})")
    print(f"    same_frame : sharing cultural frame raises Jaccard by {c_sf:+.4f} (p={p_sf:.3f})")
    if p_sl < 0.05 and p_sf >= 0.05:
        print("    -> Language code is the significant driver (M2-style / lexical layer)")
    elif p_sl >= 0.05 and p_sf < 0.05:
        print("    -> Cultural frame is the significant driver (M3)")
    elif p_sl < 0.05 and p_sf < 0.05:
        if c_sf > c_sl:
            print("    -> BOTH significant; frame effect larger => frame dominant (M3)")
        else:
            print("    -> BOTH significant; language effect larger => code dominant")
    else:
        print("    -> Neither reaches p<0.05 at n={result['n']} dyads")


if __name__ == "__main__":
    main()

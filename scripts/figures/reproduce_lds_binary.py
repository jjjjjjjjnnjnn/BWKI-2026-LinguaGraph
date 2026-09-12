"""Freeze the formula verdict (BASELINE_LEDGER §8): the 2-component pipeline
reproduces published LDS-K exactly. Run from repo root:
  python scripts/figures/reproduce_lds_binary.py
Expected output (full precision):
  ZH-EN lds=0.93358953 -> 0.9336 -> 0.934
  DE-EN lds=0.93821986 -> 0.9382 -> 0.938
  ZH-DE lds=0.51875219 -> 0.5188 -> 0.519
"""
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "scripts" / "figures"))
from _lds_utils import load_aligned, get_lang_graphs, lds_jaccard

al = load_aligned(R / "data" / "math_extractions" / "merged" / "aligned_data.json")
ln, le = get_lang_graphs(al)
for p, (a, b) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
    r = lds_jaccard(ln[a], ln[b], list(le[a]), list(le[b]))
    print(f"{p} lds={r['lds_score']:.8f} -> {r['lds_score']:.4f} -> {r['lds_score']:.3f} "
          f"(jn={r['jaccard_node']:.4f} je={r['jaccard_edge']:.4f})")

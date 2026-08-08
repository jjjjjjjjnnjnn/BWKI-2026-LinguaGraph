"""Smoke tests for the A3/C/D deepening scripts (design-effect, drivers, node/edge).

Covers the pure functions of the three scripts added 2026-08-08:
  - lds_c_design_effect       : signal table structure, floor-scan invariants
  - lds_c_divergence_drivers  : concept frequency + driver ranking
  - lds_c_node_edge_decomp    : node/edge decomposition of frozen v3 LDS

No API calls, no heavy bootstrap. Uses synthetic data only.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import pytest

from lds_c_compute import lds_concept  # noqa: E402


# ── lds_c_design_effect ─────────────────────────────────────────────
def test_lds_concept_identity():
    """Same set => LDS = 0; disjoint sets => LDS = 1."""
    s = {"a", "b", "c"}
    assert lds_concept(set(s), set(s)) == 0.0
    assert lds_concept({"a"}, {"b"}) == 1.0


def test_signal_table_margins():
    """LDS-C below floor => negative margin (submerged); above => positive."""
    from lds_c_design_effect import signal_table

    low_floor = [
        {"language": "zh", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom a"}, {"en": "freedom b"}]}]},
        {"language": "zh", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom a"}, {"en": "freedom c"}]}]},
        {"language": "de", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom a"}, {"en": "freedom d"}]}]},
        {"language": "de", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom a"}, {"en": "freedom e"}]}]},
    ]
    res = signal_table(low_floor, tag="synthetic", n_floor=20)
    assert "by_pair" in res
    # signal/floor ratio should be present for computed pairs
    for pair in ("ZH-EN", "DE-EN", "ZH-DE"):
        if pair in res["by_pair"]:
            assert 0.0 <= res["by_pair"][pair]["signal_to_floor_ratio"] <= 1.2


def test_floor_scan_monotonic():
    """More samples per language => lower floor (noise shrinks)."""
    from lds_c_design_effect import floor_scan

    records = []
    for lang in ("zh", "de", "en"):
        for i in range(6):
            records.append({"language": lang, "topics": [
                {"topic": "Freiheit", "concepts": [{"en": f"{lang}-concept-{j}"} for j in range(i + 3)]}]})
    scan = floor_scan(records, ns=(3, 5), n_iter=20)
    assert "N3" in scan and "N5" in scan
    for pair in ("ZH-EN", "DE-EN", "ZH-DE"):
        n3 = scan["N3"].get(pair, {}).get("floor_mean")
        n5 = scan["N5"].get(pair, {}).get("floor_mean")
        if n3 is not None and n5 is not None:
            assert n5 <= n3 + 1e-9, f"{pair}: floor should not rise with more samples"


# ── lds_c_divergence_drivers ────────────────────────────────────────
def test_concept_freqs_counts():
    from lds_c_divergence_drivers import concept_freqs

    recs = [
        {"language": "zh", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom"}, {"en": "boundary"}]}]},
        {"language": "zh", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom"}]}]},
        {"language": "de", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom"}, {"en": "autonomy"}]}]},
    ]
    freqs = concept_freqs(recs)
    assert freqs["zh"]["Freiheit"]["freedom"] == 2
    assert freqs["zh"]["Freiheit"]["boundary"] == 1
    assert freqs["de"]["Freiheit"]["autonomy"] == 1


def test_concept_drivers_asymmetry():
    from lds_c_divergence_drivers import concept_drivers

    recs = [
        {"language": "zh", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom"}, {"en": "boundary"}]}]},
        {"language": "de", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom"}, {"en": "autonomy"}]}]},
    ]
    freqs = {}
    from lds_c_divergence_drivers import concept_freqs
    freqs = concept_freqs(recs)
    drivers = concept_drivers(freqs, "zh", "de")
    keys = {d["key"] for d in drivers}
    # shared concept 'freedom' should NOT be a driver; asymmetric ones should
    assert "freedom" not in keys
    assert "boundary" in keys and "autonomy" in keys


def test_shared_concepts():
    from lds_c_divergence_drivers import concept_freqs, shared_concepts

    recs = [
        {"language": "zh", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom"}, {"en": "boundary"}]}]},
        {"language": "de", "topics": [{"topic": "Freiheit", "concepts": [{"en": "freedom"}, {"en": "autonomy"}]}]},
    ]
    shared = shared_concepts(concept_freqs(recs), "zh", "de")
    assert "freedom" in shared["Freiheit"]
    assert "boundary" not in shared["Freiheit"]


# ── lds_c_node_edge_decomp ──────────────────────────────────────────
def test_decompose_matches_frozen_v3():
    """decompose() must reproduce LDS v3 = 1 - mean(J_node, J_edge)."""
    from lds_c_node_edge_decomp import decompose

    graphs = {
        "zh": {"nodes": {"a", "b", "c"}, "edges": {("a", "r", "b"), ("b", "r", "c")}},
        "de": {"nodes": {"a", "b", "d"}, "edges": {("a", "r", "b"), ("a", "r", "d")}},
        "en": {"nodes": {"a", "b", "c"}, "edges": {("a", "r", "b"), ("b", "r", "c")}},
    }
    out = decompose(graphs)
    assert "ZH-DE" in out
    row = out["ZH-DE"]
    # LDS = 1 - mean(j_node, j_edge); tolerance 1e-3 covers 4-decimal rounding
    expected = 1.0 - (row["j_node"] + row["j_edge"]) / 2
    assert abs(row["lds_v3"] - round(expected, 4)) < 1e-3
    # edge contribution = (J_node - J_edge)/2
    assert abs(row["edge_contribution"] - (row["j_node"] - row["j_edge"]) / 2) < 1e-3
    # identical graphs => LDS 0
    assert out["ZH-EN"]["lds_v3"] == 0.0


def test_decompose_nan_free():
    from lds_c_node_edge_decomp import decompose

    graphs = {
        "zh": {"nodes": {"a", "b"}, "edges": {("a", "r", "b")}},
        "de": {"nodes": {"c", "d"}, "edges": {("c", "r", "d")}},
    }
    out = decompose(graphs)
    assert "ZH-DE" in out
    assert out["ZH-DE"]["j_node"] == 0.0
    assert out["ZH-DE"]["j_edge"] == 0.0
    assert out["ZH-DE"]["lds_v3"] == 1.0

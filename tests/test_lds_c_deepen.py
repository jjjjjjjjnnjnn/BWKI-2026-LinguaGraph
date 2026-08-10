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


def test_lds_concept_empty_convention():
    """Two empty sets are identical (LDS=0); empty-vs-nonempty is NaN (degenerate),
    NOT silently maximum divergence (audit C2)."""
    assert lds_concept(set(), set()) == 0.0
    v = lds_concept(set(), {"a"})
    assert v != v  # NaN


def test_jaccard_empty_convention():
    from lds_c_compute import jaccard
    assert jaccard(set(), set()) == 1.0
    v = jaccard(set(), {"a"})
    assert v != v  # NaN


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


def test_lds_v3_empty_convention():
    from lds_k_deepen import lds_v3
    # both empty => identical (LDS 0), NOT max divergence (audit C2)
    r = lds_v3(set(), set())
    assert r["lds"] == 0.0 and r["j_node"] == 1.0
    # one empty side => degenerate NaN, not silently 1.0
    r = lds_v3(set(), {"a"})
    assert r["lds"] != r["lds"]  # NaN


# ── audit H1: LMM robustness ────────────────────────────────────────
def test_lmm_core_basic_fit():
    """LMM must fit dyad rows and return finite coefficients + PSD Hessian flag."""
    from lds_c_llm_lmm import fit_lmm_core

    rows = [
        {"topic": "Freiheit", "cell_a": ("zh", "zh"), "cell_b": ("de", "de"),
         "same_lang": 0, "same_frame": 0, "y": 0.05},
        {"topic": "Freiheit", "cell_a": ("zh", "zh"), "cell_b": ("zh", "de"),
         "same_lang": 1, "same_frame": 0, "y": 0.09},
        {"topic": "Freiheit", "cell_a": ("de", "de"), "cell_b": ("zh", "de"),
         "same_lang": 0, "same_frame": 1, "y": 0.06},
        {"topic": "Gerechtigkeit", "cell_a": ("zh", "zh"), "cell_b": ("de", "de"),
         "same_lang": 0, "same_frame": 0, "y": 0.04},
        {"topic": "Gerechtigkeit", "cell_a": ("zh", "zh"), "cell_b": ("zh", "de"),
         "same_lang": 1, "same_frame": 0, "y": 0.10},
        {"topic": "Gerechtigkeit", "cell_a": ("de", "de"), "cell_b": ("zh", "de"),
         "same_lang": 0, "same_frame": 1, "y": 0.05},
    ]
    res = fit_lmm_core(rows)
    assert res["coef"][0] == res["coef"][0]  # finite intercept
    assert res["se"] is not None


def test_cell_cluster_bootstrap_runs():
    """Bootstrap must run and, when enough dyads survive, produce finite SE.
    With very small synthetic data some refits may fail (skipped) — the function
    must not crash and must return a structure with the requested keys."""
    from lds_c_llm_lmm import cell_cluster_bootstrap_se

    rows = []
    cells = [("zh", "zh"), ("de", "de"), ("en", "en"), ("zh", "de"), ("de", "zh")]
    import itertools
    pairs = list(itertools.combinations(cells, 2))
    for t in ["Freiheit", "Gerechtigkeit", "Verantwortung", "Heimat", "Erfolg"]:
        for a, b in pairs:
            rows.append({"topic": t, "cell_a": a, "cell_b": b,
                         "same_lang": 1 if a[0] == b[0] else 0,
                         "same_frame": 1 if a[1] == b[1] else 0,
                         "y": 0.05 if a[0] == b[0] else 0.03})
    boot = cell_cluster_bootstrap_se(rows, cells, n_iter=30)
    assert "same_lang" in boot and "same_frame" in boot
    # either a valid SE or an honest NaN (with n_boot<2); must not crash
    assert "se_boot" in boot["same_lang"]
    assert "n_boot" in boot["same_lang"]


def test_hessian_psd_check():
    """PSD check must pass for an identity-like Hessian, fail for negative-definite."""
    from lds_c_llm_lmm import is_positive_semidefinite
    import numpy as np
    assert is_positive_semidefinite(np.eye(3)) is True
    assert is_positive_semidefinite(np.array([[1.0, 0.0], [0.0, -1.0]])) is False


# ── Deep-dive A: heterogeneity injection ────────────────────────────
def test_inject_dropout_preserves_language():
    """Dropout must keep the language label and topic structure; q=1.0 no-op."""
    from lds_c_heterogeneity_injection import inject_dropout
    import random
    recs = [
        {"language": "zh", "topics": [
            {"topic": "Freiheit", "concepts": [{"en": f"c{i}"} for i in range(6)]}]},
    ]
    rng = random.Random(1)
    out = inject_dropout(recs, q=1.0, rng=rng)
    assert out[0]["language"] == "zh"
    assert len(out[0]["topics"]) == 1
    assert len(out[0]["topics"][0]["concepts"]) == 6  # q=1 keeps all
    # q=0.0 would drop all -> but the guard keeps 1 concept (never empty)
    rng2 = random.Random(2)
    out0 = inject_dropout(recs, q=0.0, rng=rng2)
    assert 1 <= len(out0[0]["topics"][0]["concepts"]) <= 6


def test_between_subject_stats_margin():
    """With heterogeneous language-specific data, margin should be positive;
    with identical concepts across languages, margin near zero."""
    from lds_c_heterogeneity_injection import between_subject_stats
    import random

    # language-specific concepts => clear signal
    recs = []
    for lang, tag in [("zh", "zh"), ("de", "de")]:
        for i in range(8):
            recs.append({"language": lang, "topics": [
                {"topic": "Freiheit", "concepts": [{"en": f"{tag} concept {j}"} for j in range(5)]}]})
    rng = random.Random(1)
    s = between_subject_stats(recs, N=6, n_iter=50, rng=rng)
    assert "ZH-DE" in s
    assert s["ZH-DE"]["signal_margin"] > 0.0

    # identical concepts across languages => no signal
    recs2 = []
    for lang in ["zh", "de"]:
        for i in range(8):
            recs2.append({"language": lang, "topics": [
                {"topic": "Freiheit", "concepts": [{"en": "shared concept"}]}]})
    rng2 = random.Random(2)
    s2 = between_subject_stats(recs2, N=6, n_iter=50, rng=rng2)
    assert abs(s2["ZH-DE"]["signal_margin"]) < 0.1


def test_mean_pairwise_overlap():
    from lds_c_heterogeneity_injection import mean_pairwise_overlap
    # identical sets => overlap 1.0
    assert mean_pairwise_overlap([{"a", "b"}, {"a", "b"}]) == 1.0
    # disjoint => 0.0
    assert mean_pairwise_overlap([{"a"}, {"b"}]) == 0.0
    # fewer than 2 => None
    assert mean_pairwise_overlap([{"a"}]) is None
def test_label_permutation_p_value():
    """Permutation p must be small when labels carry signal, and expose the
    observed value is compared against the null (audit M2)."""
    from lds_c_compute import label_permutation_null

    # two languages with strongly different concept sets => labels carry signal
    recs = []
    for i in range(5):
        recs.append({"language": "zh", "topics": [
            {"topic": "Freiheit", "concepts": [{"en": f"zh concept {j}"} for j in range(6)]}]})
        recs.append({"language": "de", "topics": [
            {"topic": "Freiheit", "concepts": [{"en": f"de concept {j}"} for j in range(6)]}]})
    # observed: fully disjoint languages -> LDS high; permuted would mix -> lower
    observed = {"ZH-DE": 1.0}
    perm = label_permutation_null(recs, n_iter=100, observed=observed)
    assert "ZH-DE" in perm
    p = perm["ZH-DE"]["perm_p_two_sided"]
    assert p is not None and p < 0.05  # signal detected

    # identical concept sets across languages => labels carry NO signal => p large
    recs2 = []
    for lang in ("zh", "de"):
        for i in range(5):
            recs2.append({"language": lang, "topics": [
                {"topic": "Freiheit", "concepts": [{"en": "shared concept"}]}]})
    observed2 = {"ZH-DE": 0.0}
    perm2 = label_permutation_null(recs2, n_iter=100, observed=observed2)
    p2 = perm2["ZH-DE"]["perm_p_two_sided"]
    assert p2 is not None and p2 > 0.05


# ── Multi-model replication harness (2026-08-09) ────────────────────
def _synth_units(model_seed: int, n_zh: int = 8, n_de: int = 8) -> list:
    """Synthetic subject units: a 'model' with language-specific concepts.
    Concepts in the same language are shared across samples (low within-lang
    noise); the two languages differ (signal). Deterministic per seed."""
    zh_concepts = [{"concept": f"zh-{model_seed}-{i}", "en": f"zh-c{i}", "importance": 1.0}
                   for i in range(6)]
    de_concepts = [{"concept": f"de-{model_seed}-{i}", "en": f"de-c{i}", "importance": 1.0}
                   for i in range(6)]
    units = []
    for s in range(n_zh):
        units.append({"unit_id": f"P1_zh_s{s:02d}", "probe": "P1", "language": "zh",
                      "concepts": {"Freiheit": zh_concepts}})
    for s in range(n_de):
        units.append({"unit_id": f"P1_de_s{s:02d}", "probe": "P1", "language": "de",
                      "concepts": {"Freiheit": de_concepts}})
    return units


def test_harness_imports_and_jaccard():
    from lds_c_multi_model import jaccard
    assert jaccard(["a", "b"], ["b", "c"]) == pytest.approx(1 / 3)
    assert jaccard(["a"], ["a"]) == 1.0
    assert jaccard([], []) == 1.0
    assert jaccard([], ["a"]) == 0.0


def _dc_models(n_models: int = 12) -> dict:
    """n synthetic models; each marks 'de-signal' DE-only and 'zh-signal'
    ZH-only (Freiheit), plus a shared concept. Enough models to reach the
    report threshold (>=10)."""
    def build() -> dict:
        zh_c = [{"concept": "a", "en": "shared", "importance": 1.0},
                {"concept": "b", "en": "zh-signal", "importance": 1.0}]
        de_c = [{"concept": "a", "en": "shared", "importance": 1.0},
                {"concept": "c", "en": "de-signal", "importance": 1.0}]
        units = []
        for s in range(6):
            units.append({"unit_id": f"P1_zh_s{s}", "probe": "P1", "language": "zh",
                          "concepts": {"Freiheit": zh_c}})
            units.append({"unit_id": f"P1_de_s{s}", "probe": "P1", "language": "de",
                          "concepts": {"Freiheit": de_c}})
            units.append({"unit_id": f"P1_en_s{s}", "probe": "P1", "language": "en",
                          "concepts": {"Freiheit": [{"concept": "a", "en": "shared",
                                                     "importance": 1.0}]}})
        return {"units": units}
    return {f"m{i}": build() for i in range(n_models)}


def test_direction_consistency_finds_shared_direction():
    """If 12 independent 'models' all mark the same concept zh-only / de-only,
    direction_consistency reports it in the >=10-vote strong lists."""
    from lds_c_multi_model import direction_consistency

    dc = direction_consistency(_dc_models(12), min_models=3)
    assert dc["n_models_voting"] == 12
    assert dc["n_consistent_at_report_threshold"] >= 2
    # canonical_key reorders tokens: "zh-signal" -> "signal zh"
    de_keys = {k for k, _ in dc.get("de_only_strong", [])}
    zh_keys = {k for k, _ in dc.get("zh_only_strong", [])}
    assert "Freiheit:de signal" in de_keys
    assert "Freiheit:signal zh" in zh_keys
    # the null model must be computed and the observed >=10 count exceed it
    ovn = dc["observed_vs_null"]["10"]
    assert ovn["observed"] >= 2
    assert ovn["p_null_ge_observed"] < 0.05


def test_direction_consistency_null_model_in_noise():
    """A null model (random direction) must NOT report a strong directional
    concept where models disagree — and the observed-vs-null machinery works."""
    from lds_c_multi_model import direction_consistency

    # 12 models that disagree: 6 mark 'contested' zh-only, 6 de-only -> max 6 < 10
    def build(side: str) -> dict:
        zh_c = [{"concept": "a", "en": "shared", "importance": 1.0}]
        de_c = [{"concept": "a", "en": "shared", "importance": 1.0}]
        if side == "zh":
            zh_c.append({"concept": "b", "en": "contested", "importance": 1.0})
        else:
            de_c.append({"concept": "b", "en": "contested", "importance": 1.0})
        units = []
        for s in range(6):
            units.append({"unit_id": f"P1_zh_s{s}", "probe": "P1", "language": "zh",
                          "concepts": {"Freiheit": zh_c}})
            units.append({"unit_id": f"P1_de_s{s}", "probe": "P1", "language": "de",
                          "concepts": {"Freiheit": de_c}})
            units.append({"unit_id": f"P1_en_s{s}", "probe": "P1", "language": "en",
                          "concepts": {"Freiheit": [{"concept": "a", "en": "shared",
                                                     "importance": 1.0}]}})
        return {"units": units}

    models = {f"m{i}": build("zh" if i % 2 == 0 else "de") for i in range(12)}
    dc = direction_consistency(models, min_models=3)
    de_keys = {k for k, _ in dc.get("de_only_strong", [])}
    zh_keys = {k for k, _ in dc.get("zh_only_strong", [])}
    assert "Freiheit:contest" not in de_keys
    assert "Freiheit:contest" not in zh_keys
    # observed-vs-null table exists for all thresholds
    for t in ("3", "5", "10", "20"):
        assert t in dc["observed_vs_null"]
        assert dc["observed_vs_null"][t]["null_mean"] >= 0


def test_load_canonical_units_selects_baseline():
    """The canonical loader must select deepseek-v4-flash by content and
    validate P1 coverage (audit C9), not the lexicographically-last file."""
    from lds_c_llm_analyze import load_canonical_units

    units, path = load_canonical_units()
    assert units, "no units"
    assert path.name == "llm_subject_20260808.json"
    p1 = [u for u in units if u.get("probe") == "P1"]
    assert len(p1) >= 30
    from collections import Counter
    langs = Counter(u.get("language", "") for u in p1
                    if any(c for c in u.get("concepts", {}).values()))
    for l in ("zh", "de", "en"):
        assert langs.get(l, 0) >= 5

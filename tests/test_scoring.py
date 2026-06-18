"""
Pytest tests for scoring.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import networkx as nx
from scoring import (
    calculate_mcl_score,
    calculate_lcd_score,
    calculate_concept_f1,
    calculate_relation_f1,
)


class TestMCLScore:
    def test_identical_graphs(self):
        g1 = nx.DiGraph()
        g1.add_edges_from([("A", "B"), ("B", "C")])
        g2 = nx.DiGraph()
        g2.add_edges_from([("A", "B"), ("B", "C")])
        result = calculate_mcl_score(g1, g2)
        assert result["mcl_score"] == 0.0
        assert result["missing_count"] == 0

    def test_all_missing(self):
        expert = nx.DiGraph()
        expert.add_edges_from([("A", "B"), ("C", "D")])
        student = nx.DiGraph()
        result = calculate_mcl_score(student, expert)
        assert result["mcl_score"] == 100.0
        assert result["missing_count"] == 2

    def test_partial_missing(self):
        expert = nx.DiGraph()
        expert.add_edges_from([("A", "B"), ("B", "C"), ("C", "D")])
        student = nx.DiGraph()
        student.add_edges_from([("A", "B")])
        result = calculate_mcl_score(student, expert)
        assert result["mcl_score"] == pytest.approx(66.67, rel=0.01)
        assert result["missing_count"] == 2

    def test_empty_expert(self):
        expert = nx.DiGraph()
        student = nx.DiGraph()
        student.add_edge("A", "B")
        result = calculate_mcl_score(student, expert)
        assert result["mcl_score"] == 0.0


class TestLCDScore:
    def test_identical_graphs(self):
        g1 = nx.DiGraph()
        g1.add_edges_from([("A", "B")])
        g2 = nx.DiGraph()
        g2.add_edges_from([("A", "B")])
        result = calculate_lcd_score(g1, g2)
        assert result["lcd_score"] == 0.0
        assert result["similarity"] == 1.0
        # Verify 3-component metric
        assert result["ged_similarity"] == 1.0
        assert result["jaccard_node"] == 1.0
        assert result["jaccard_edge"] == 1.0

    def test_completely_different(self):
        """Completely different graphs: LDS < 1.0 because GED has some similarity."""
        g1 = nx.DiGraph()
        g1.add_edges_from([("A", "B")])
        g2 = nx.DiGraph()
        g2.add_edges_from([("C", "D")])
        result = calculate_lcd_score(g1, g2)
        # 3-component metric: GED can match by renaming, so LDS ≠ 1.0
        assert result["lcd_score"] > 0.5  # High drift
        assert result["similarity"] < 0.5
        assert result["jaccard_node"] == 0.0  # No node overlap
        assert result["jaccard_edge"] == 0.0  # No edge overlap

    def test_with_mapping(self):
        g1 = nx.DiGraph()
        g1.add_edges_from([("导数", "变化率")])
        g2 = nx.DiGraph()
        g2.add_edges_from([("Ableitung", "Änderungsrate")])
        mapping = {"导数": "Ableitung", "变化率": "Änderungsrate"}
        result = calculate_lcd_score(g1, g2, concept_mapping=mapping)
        assert result["lcd_score"] == 0.0


class TestConceptF1:
    def test_perfect_match(self):
        gold = {"A", "B", "C"}
        extracted = {"A", "B", "C"}
        result = calculate_concept_f1(gold, extracted)
        assert result["f1"] == 1.0
        assert result["precision"] == 1.0
        assert result["recall"] == 1.0

    def test_partial_match(self):
        gold = {"A", "B", "C"}
        extracted = {"A", "B", "D"}
        result = calculate_concept_f1(gold, extracted)
        assert result["precision"] == pytest.approx(0.6667, rel=0.01)
        assert result["recall"] == pytest.approx(0.6667, rel=0.01)

    def test_no_match(self):
        gold = {"A", "B"}
        extracted = {"C", "D"}
        result = calculate_concept_f1(gold, extracted)
        assert result["f1"] == 0.0


class TestRelationF1:
    def test_perfect_match(self):
        gold = [{"from": "A", "to": "B", "type": "prerequisite"}]
        extracted = [{"source": "A", "target": "B", "type": "prerequisite"}]
        result = calculate_relation_f1(gold, extracted)
        assert result["f1"] == 1.0

    def test_same_endpoints_different_type(self):
        gold = [{"from": "A", "to": "B", "type": "prerequisite"}]
        extracted = [{"source": "A", "target": "B", "type": "cause_effect"}]
        result = calculate_relation_f1(gold, extracted)
        assert result["f1"] == 0.0

    def test_empty_relations(self):
        result = calculate_relation_f1([], [])
        assert result["precision"] == 1.0
        assert result["recall"] == 1.0
        assert result["f1"] == 1.0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

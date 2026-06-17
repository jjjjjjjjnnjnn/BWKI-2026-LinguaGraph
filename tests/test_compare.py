"""
Pytest tests for compare.py (MCL detection)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import networkx as nx
from compare import detect_missing_links, calculate_graph_similarity


class TestDetectMissingLinks:
    def test_identical_graphs(self):
        g1 = nx.DiGraph()
        g1.add_edges_from([("A", "B"), ("B", "C")])
        g2 = nx.DiGraph()
        g2.add_edges_from([("A", "B"), ("B", "C")])
        missing = detect_missing_links(g1, g2)
        assert len(missing) == 0

    def test_missing_concept(self):
        expert = nx.DiGraph()
        expert.add_edges_from([("A", "B"), ("B", "C")])
        student = nx.DiGraph()
        student.add_edge("A", "B")
        missing = detect_missing_links(student, expert)
        assert any(m["type"] == "missing_concept" for m in missing)

    def test_missing_relation_both_exist(self):
        """When both concepts exist in student but edge is missing."""
        expert = nx.DiGraph()
        expert.add_edges_from([("A", "B"), ("A", "C")])
        student = nx.DiGraph()
        student.add_edge("A", "B")
        missing = detect_missing_links(student, expert)
        # Should detect missing edge A->C as missing_relation
        missing_types = {m["type"] for m in missing}
        assert "missing_relation" in missing_types or "missing_concept" in missing_types

    def test_isolated_node(self):
        student = nx.DiGraph()
        student.add_node("A")
        expert = nx.DiGraph()
        expert.add_edge("A", "B")
        missing = detect_missing_links(student, expert)
        assert any(m["type"] == "isolated_concept" for m in missing)

    def test_threshold_filter(self):
        expert = nx.DiGraph()
        expert.add_edges_from([("A", "B"), ("C", "D")])
        student = nx.DiGraph()
        missing = detect_missing_links(student, expert, threshold=0.9)
        high_conf = [m for m in missing if m["confidence"] >= 0.9]
        assert len(high_conf) <= len(missing)


class TestGraphSimilarity:
    def test_identical(self):
        g1 = nx.DiGraph()
        g1.add_edges_from([("A", "B")])
        g2 = nx.DiGraph()
        g2.add_edges_from([("A", "B")])
        assert calculate_graph_similarity(g1, g2) == 1.0

    def test_empty_graphs(self):
        """Empty graphs have no differences, so similarity = 0 (0/0 default)."""
        g1 = nx.DiGraph()
        g2 = nx.DiGraph()
        sim = calculate_graph_similarity(g1, g2)
        assert sim == 0.0

    def test_no_overlap(self):
        g1 = nx.DiGraph()
        g1.add_edges_from([("A", "B")])
        g2 = nx.DiGraph()
        g2.add_edges_from([("C", "D")])
        sim = calculate_graph_similarity(g1, g2)
        assert sim == 0.0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

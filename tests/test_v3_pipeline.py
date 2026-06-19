"""
Pytest tests for end-to-end pipeline (v3 extraction → MCL scoring).

Tests pipeline integration with inline data — no external files needed.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from scoring import calculate_mcl_score
import networkx as nx


class TestV3Pipeline:
    """End-to-end pipeline integration tests using inline demo data."""

    def test_calculus_mcl_score(self):
        """Test MCL score with calculus domain data."""
        expert = nx.DiGraph()
        expert.add_edges_from([
            ("极限", "导数"), ("导数", "变化率"), ("积分", "导数"),
            ("积分", "面积"), ("导数", "切线斜率")
        ])

        student = nx.DiGraph()
        student.add_edges_from([
            ("导数", "变化率"), ("积分", "面积")
        ])

        mcl = calculate_mcl_score(student, expert)

        assert mcl["missing_count"] == 3
        assert mcl["total_expert"] == 5
        assert 60.0 <= mcl["mcl_score"] <= 100.0  # 3/5 = 60%

    def test_perfect_knowledge(self):
        """Student knows everything from expert graph."""
        expert = nx.DiGraph()
        expert.add_edges_from([("A", "B"), ("B", "C")])

        student = nx.DiGraph()
        student.add_edges_from([("A", "B"), ("B", "C")])

        mcl = calculate_mcl_score(student, expert)
        assert mcl["mcl_score"] == 0.0
        assert mcl["missing_count"] == 0

    @pytest.mark.parametrize("student_edges,expected_missing", [
        ([], 3),
        ([("A", "B")], 2),
        ([("A", "B"), ("B", "C")], 1),
        ([("A", "B"), ("B", "C"), ("A", "C")], 1),  # A→C not in expert
    ])
    def test_varying_knowledge(self, student_edges, expected_missing):
        """Test varying levels of student knowledge vs fixed expert."""
        expert = nx.DiGraph()
        expert.add_edges_from([("A", "B"), ("B", "C"), ("B", "A")])

        student = nx.DiGraph()
        for edge in student_edges:
            student.add_edge(*edge)

        mcl = calculate_mcl_score(student, expert)
        assert mcl["missing_count"] == expected_missing

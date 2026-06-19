"""
Pytest tests for LLM extraction validation against gold labels.

Tests use inline data and mock mode — no API key required.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.extract import extract_concepts


class TestExtractionMock:
    """Test mock extraction returns valid structured output."""

    def test_mock_returns_expected_fields(self):
        """Verify mock extraction returns all required fields."""
        result = extract_concepts(
            "Derivative represents the rate of change.",
            "en", use_mock=True
        )
        assert "concepts" in result
        assert "relations" in result
        assert "raw_response" in result
        assert "language" in result
        assert isinstance(result["concepts"], list)
        assert isinstance(result["relations"], list)

    def test_mock_calculus_zh(self):
        """Mock extraction should find calculus concepts in Chinese text."""
        result = extract_concepts(
            "导数表示变化率，积分是导数的逆运算。",
            "zh", use_mock=True
        )
        assert len(result["concepts"]) >= 1
        assert "导数" in result["concepts"]

    def test_mock_calculus_de(self):
        """Mock extraction should find calculus concepts in German text."""
        result = extract_concepts(
            "Ableitung ist die Änderungsrate einer Funktion.",
            "de", use_mock=True
        )
        assert len(result["concepts"]) >= 1
        assert "Ableitung" in result["concepts"]

    def test_mock_calculus_en(self):
        """Mock extraction should find calculus concepts in English text."""
        result = extract_concepts(
            "The derivative represents the rate of change of a function.",
            "en", use_mock=True
        )
        assert len(result["concepts"]) >= 1

    def test_mock_social_issues_still_works(self):
        """Mock extraction should return something for any text input."""
        result = extract_concepts(
            "自由是每个人都应该拥有的权利。",
            "zh", use_mock=True
        )
        assert "concepts" in result
        assert isinstance(result["concepts"], list)

    def test_mock_does_not_throw(self):
        """Mock extraction should never throw on valid input."""
        for lang in ("zh", "en", "de"):
            result = extract_concepts("Test input.", lang, use_mock=True)
            assert result is not None

    def test_empty_input(self):
        """Mock extraction should handle empty input gracefully."""
        result = extract_concepts("", "zh", use_mock=True)
        assert result is not None
        assert isinstance(result["concepts"], list)

    def test_three_languages(self):
        """Test that all three languages produce valid extraction output."""
        texts = {
            "zh": "极限和导数是微积分的基础。",
            "de": "Grenzwerte und Ableitungen sind die Grundlagen der Analysis.",
            "en": "Limits and derivatives are the foundations of calculus."
        }
        for lang, text in texts.items():
            result = extract_concepts(text, lang, use_mock=True)
            assert len(result["concepts"]) >= 1, f"No concepts for {lang}: {text}"

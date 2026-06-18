"""
Tests for participant_data/participant_manager.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "participant_data"))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
from participant_manager import ParticipantManager, REQUIRED_LANGUAGES, TARGET_PER_LANGUAGE, TARGET_TOTAL


@pytest.fixture
def pm():
    """Create a ParticipantManager for testing."""
    manager = ParticipantManager()
    yield manager
    manager.close()


class TestAddParticipant:
    def test_add_valid(self, pm):
        pid = pm.add_participant("TEST_001", native_lang="zh", consent=True)
        assert pid == "TEST_001"
        p = pm.get_participant("TEST_001")
        assert p is not None
        assert p["native_lang"] == "zh"
        assert p["consent"] == 1
        # Cleanup
        pm.delete_participant("TEST_001")

    def test_add_invalid_lang(self, pm):
        with pytest.raises(ValueError, match="native_lang"):
            pm.add_participant("TEST_BAD", native_lang="fr")

    def test_update_consent(self, pm):
        pm.add_participant("TEST_002", native_lang="de", consent=False)
        assert pm.update_consent("TEST_002", True)
        p = pm.get_participant("TEST_002")
        assert p["consent"] == 1
        pm.delete_participant("TEST_002")

    def test_update_consent_nonexistent(self, pm):
        assert not pm.update_consent("NONEXISTENT", True)


class TestListParticipants:
    def test_list_all(self, pm):
        participants = pm.list_participants()
        assert isinstance(participants, list)

    def test_list_by_lang(self, pm):
        participants = pm.list_participants(native_lang="zh")
        for p in participants:
            assert p["native_lang"] == "zh"


class TestRecruitmentStatus:
    def test_status_structure(self, pm):
        status = pm.get_recruitment_status()
        assert "total_registered" in status
        assert "total_consented" in status
        assert "target_total" in status
        assert "by_language" in status
        assert status["target_total"] == TARGET_TOTAL

    def test_status_languages(self, pm):
        status = pm.get_recruitment_status()
        for lang in REQUIRED_LANGUAGES:
            assert lang in status["by_language"]
            assert "registered" in status["by_language"][lang]
            assert "consented" in status["by_language"][lang]


class TestAnonymization:
    def test_anonymize_removes_id(self, pm):
        resp = {
            "student_id": "S001",
            "response_id": "R001",
            "timestamp": "2026-06-17T10:00:00",
            "language": "zh",
            "answer": "test answer",
        }
        anon = pm.anonymize_response(resp)
        assert "student_id" not in anon
        assert "anonymous_id" in anon
        assert "timestamp" not in anon
        assert anon["language"] == "zh"
        assert anon["answer"] == "test answer"


class TestDeleteParticipant:
    def test_delete_nonexistent(self, pm):
        assert not pm.delete_participant("NONEXISTENT")

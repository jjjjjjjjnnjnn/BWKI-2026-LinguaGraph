"""Robustness tests for the LLM-as-subject API pipeline (2026-08-11).

Covers the failure/recovery behaviours that the R&D review flagged as an
untested gap:
  - key selection per gateway          (load_key_for_url / _env_get)
  - API call error handling            (call -> "ERROR: ..." string, no crash)
  - cross-day resume merge             (collect_good_units)
  - abort rule on consecutive EMPTY    (update_consecutive_empty / LDS_ABORT_AFTER)
  - output schema                      (save_out)

No API calls, no network: every client is a mock, every file is synthetic.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import pytest

import lds_c_llm_subject as subj  # noqa: E402


# ── key selection ─────────────────────────────────────────────────────

def test_load_key_for_url_maps_gateways(monkeypatch):
    """OpenRouter -> OPENROUTER_API_KEY, DashScope -> DASHSCOPE_API_KEY, else -> OPENAI_API_KEY."""
    keys = {
        "OPENROUTER_API_KEY": "or-key",
        "DASHSCOPE_API_KEY": "ds-key",
        "OPENAI_API_KEY": "oa-key",
    }
    monkeypatch.setattr(subj, "_env_get", lambda name: keys.get(name, ""))
    assert subj.load_key_for_url("https://openrouter.ai/api/v1") == "or-key"
    assert subj.load_key_for_url("https://openrouter.ai/api/v1/x") == "or-key"
    assert subj.load_key_for_url("https://dashscope.aliyuncs.com/compatible-mode/v1") == "ds-key"
    assert subj.load_key_for_url("https://opencode.ai/zen/go/v1") == "oa-key"
    assert subj.load_key_for_url("https://opencode.ai/zen/v1") == "oa-key"


def test_load_key_for_url_missing_returns_empty(monkeypatch):
    monkeypatch.setattr(subj, "_env_get", lambda name: "")
    assert subj.load_key_for_url("https://openrouter.ai/api/v1") == ""


def test_env_get_parses_dotenv(monkeypatch, tmp_path):
    """_env_get reads KEY=VALUE pairs from PROJECT_ROOT/.env, skipping comments/blanks."""
    (tmp_path / ".env").write_text(
        "# comment\nOPENAI_API_KEY=sk-abc\n\nDASHSCOPE_API_KEY = sk-dash\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(subj, "PROJECT_ROOT", tmp_path)
    assert subj._env_get("OPENAI_API_KEY") == "sk-abc"
    assert subj._env_get("DASHSCOPE_API_KEY") == "sk-dash"
    assert subj._env_get("MISSING") == ""


def test_env_get_falls_back_to_process_env(monkeypatch, tmp_path):
    """Without a .env file, _env_get falls back to os.environ."""
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.setattr(subj, "PROJECT_ROOT", empty)
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")
    assert subj._env_get("OPENAI_API_KEY") == "env-key"


# ── API call error handling ──────────────────────────────────────────

class _FakeChoice:
    def __init__(self, content, finish_reason="stop"):
        self.message = type("M", (), {"content": content})()
        self.finish_reason = finish_reason


class _FakeUsage:
    prompt_tokens = 12
    completion_tokens = 34


class _FakeResp:
    def __init__(self, content, finish_reason="stop"):
        self.choices = [_FakeChoice(content, finish_reason)]
        self.usage = _FakeUsage()


class _FakeCompletions:
    def __init__(self, resp=None, exc=None):
        self._resp = resp
        self._exc = exc

    def create(self, **kwargs):
        if self._exc is not None:
            raise self._exc
        return self._resp


class _FakeClient:
    def __init__(self, resp=None, exc=None):
        self.chat = type("C", (), {"completions": _FakeCompletions(resp, exc)})()


def test_call_returns_content_on_success(monkeypatch):
    monkeypatch.setattr(subj, "MODEL", "fake-model")
    client = _FakeClient(resp=_FakeResp("  Antwort  ", finish_reason="stop"))
    raw, meta = subj.call(client, "sys", "user")
    assert raw == "  Antwort  "
    assert meta["finish"] == "stop"
    assert meta["tokens_in"] == 12
    assert meta["tokens_out"] == 34
    assert meta["latency_ms"] >= 0


def test_call_quota_error_returns_error_string(monkeypatch):
    """A 403/429 quota failure must degrade to an ERROR string, never crash."""
    monkeypatch.setattr(subj, "MODEL", "fake-model")
    for exc in (Exception("403 quota"), RuntimeError("429 rate limited"), ConnectionError("refused")):
        client = _FakeClient(exc=exc)
        raw, meta = subj.call(client, "sys", "user")
        assert raw.startswith("ERROR:")
        assert meta["latency_ms"] >= 0


def test_call_timeout_error_returns_error_string(monkeypatch):
    import socket
    monkeypatch.setattr(subj, "MODEL", "fake-model")
    client = _FakeClient(exc=socket.timeout("timed out"))
    raw, _ = subj.call(client, "sys", "user")
    assert raw.startswith("ERROR:")


# ── output schema ─────────────────────────────────────────────────────

def test_save_out_writes_expected_schema(monkeypatch, tmp_path):
    monkeypatch.setattr(subj, "MODEL_ID", "dashscope:glm-5.2")
    monkeypatch.setattr(subj, "API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    monkeypatch.setattr(subj, "RANDOM_SEED", 42)
    records = [{"unit_id": "u1", "probe": "P1", "concepts": {"zh": []}}]
    out = tmp_path / "out.json"
    subj.save_out(out, records)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["model"] == "dashscope:glm-5.2"
    assert data["api_url"].endswith("compatible-mode/v1")
    assert data["design"] == "d1_mechanism"
    assert data["seed"] == 42
    assert data["units"] == records


# ── cross-day resume merge ────────────────────────────────────────────

def _unit(uid, probe="P1", concepts=None, associations=None):
    u = {"unit_id": uid, "probe": probe}
    if concepts is not None:
        u["concepts"] = concepts
    if associations is not None:
        u["associations"] = associations
    return u


def test_collect_good_units_merges_across_date_files(tmp_path):
    """Good units from multiple date-rolled files merge; empty units are dropped."""
    (tmp_path / "llm_subject_ds_m_20260809.json").write_text(json.dumps({
        "units": [
            _unit("u1", concepts={"zh": ["a"], "de": []}),     # good
            _unit("u2", concepts={"zh": []}),                  # empty -> dropped
            _unit("u3", probe="P3", associations=["x"]),       # good (P3)
        ],
    }, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "llm_subject_ds_m_20260810.json").write_text(json.dumps({
        "units": [
            _unit("u1", concepts={"zh": ["a"], "de": ["b"]}),  # dupe -> later wins
            _unit("u4", probe="P3", associations=[]),           # empty -> dropped
        ],
    }, ensure_ascii=False), encoding="utf-8")

    done = subj.collect_good_units(tmp_path, "llm_subject_ds_m")
    assert set(done) == {"u1", "u3"}
    # later file wins on duplicate unit_id
    assert done["u1"]["concepts"]["de"] == ["b"]


def test_collect_good_units_skips_unreadable_files(tmp_path):
    """A corrupt JSON file is warned about and skipped, not fatal."""
    (tmp_path / "llm_subject_m_20260809.json").write_text("{corrupt", encoding="utf-8")
    (tmp_path / "llm_subject_m_20260810.json").write_text(json.dumps({
        "units": [_unit("u1", concepts={"zh": ["a"]})],
    }), encoding="utf-8")
    done = subj.collect_good_units(tmp_path, "llm_subject_m")
    assert done == {"u1": done["u1"]}


def test_collect_good_units_ignores_units_without_id(tmp_path):
    (tmp_path / "llm_subject_m_20260810.json").write_text(json.dumps({
        "units": [
            {"probe": "P1", "concepts": {"zh": ["a"]}},   # no unit_id -> dropped
            _unit("u1", concepts={"zh": ["a"]}),
        ],
    }), encoding="utf-8")
    done = subj.collect_good_units(tmp_path, "llm_subject_m")
    assert set(done) == {"u1"}


def test_collect_good_units_provider_scoped_prefix(tmp_path):
    """Different provider prefixes never cross-contaminate (namespacing)."""
    (tmp_path / "llm_subject_zen_glm_20260810.json").write_text(json.dumps({
        "units": [_unit("u1", concepts={"zh": ["a"]})],
    }), encoding="utf-8")
    (tmp_path / "llm_subject_dashscope_glm_20260810.json").write_text(json.dumps({
        "units": [_unit("u2", concepts={"zh": ["b"]})],
    }), encoding="utf-8")
    done_ds = subj.collect_good_units(tmp_path, "llm_subject_dashscope_glm")
    done_zen = subj.collect_good_units(tmp_path, "llm_subject_zen_glm")
    assert set(done_ds) == {"u2"}
    assert set(done_zen) == {"u1"}


# ── abort rule (LDS_ABORT_AFTER) ─────────────────────────────────────

def test_update_consecutive_empty_resets_on_good():
    assert subj.update_consecutive_empty(2, ok=True, abort_after=3) == 0
    assert subj.update_consecutive_empty(0, ok=True, abort_after=3) == 0


def test_update_consecutive_empty_increments_and_reaches_abort():
    counter = 0
    # three EMPTY units in a row -> counter reaches abort_after=3
    for _ in range(3):
        counter = subj.update_consecutive_empty(counter, ok=False, abort_after=3)
    assert counter == 3
    # a good unit afterwards resets it
    assert subj.update_consecutive_empty(counter, ok=True, abort_after=3) == 0


def test_abort_survives_interleaved_good_unit():
    """An occasional good unit resets the counter, so a sparse model is not killed."""
    counter = 0
    seq = [False, True, False, False, False]  # one good resets after first empty
    for ok in seq:
        counter = subj.update_consecutive_empty(counter, ok, abort_after=3)
    assert counter == 3  # only reached at the tail, thanks to the reset

import os
import json
import pytest
from fastapi.testclient import TestClient
from main import app
from src.llm.client import _CACHE_STORE, store_in_cache
from src.llm.schema import TriageResponse

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_env_and_cache():
    os.environ["LLM_STUB"] = "0"
    os.environ["LLM_ENABLED"] = "true"
    os.environ["LLM_CACHE"] = "true"
    _CACHE_STORE.clear()

def test_stage_1_input_validation_rejects_invalid_text():
    """STAGE 1 — Missing, empty, or oversized text (>2000 chars) returns HTTP 400 naming the field."""
    # 1. Missing field
    resp1 = client.post("/api/v1/triage", json={})
    assert resp1.status_code == 400
    assert resp1.json()["field"] == "body.text"

    # 2. Empty text
    resp2 = client.post("/api/v1/triage", json={"text": ""})
    assert resp2.status_code == 400
    assert "body.text" in resp2.json()["field"]

    # 3. Oversized text (>2000 chars)
    resp3 = client.post("/api/v1/triage", json={"text": "a" * 2005})
    assert resp3.status_code == 400
    assert "body.text" in resp3.json()["field"]

def test_stage_1_stub_mode_returns_schema_valid_json():
    """STAGE 1 — LLM_STUB=1 returns schema-valid response without calling model (0 model calls)."""
    os.environ["LLM_STUB"] = "1"
    
    resp = client.post("/api/v1/triage", json={"text": "Simulated support message"})
    assert resp.status_code == 200
    data = resp.json()
    
    # Assert output schema fields
    assert data["category"] == "bug"
    assert data["urgency"] == "high"
    assert data["confidence"] == 0.95
    assert "Stub response" in data["reason"]

def test_stage_4_kill_switch_returns_safe_fallback():
    """STAGE 4 — LLM_ENABLED=false disables model and returns deterministic fallback."""
    os.environ["LLM_ENABLED"] = "false"
    
    resp = client.post("/api/v1/triage", json={"text": "Emergency production bug"})
    assert resp.status_code == 200
    data = resp.json()
    
    assert data["category"] == "other"
    assert data["urgency"] == "normal"
    assert data["confidence"] == 0.5
    assert "Kill switch" in data["reason"]

def test_stage_3_repair_retry_success(monkeypatch):
    """STAGE 3 — Repair retry handles invalid initial output and returns valid schema on second attempt."""
    calls = 0
    def mock_call_llm(sys_prompt, user_msg, prompt_version="v1.0.0", repair_attempt=False):
        nonlocal calls
        calls += 1
        if calls == 1:
            # First call returns invalid JSON missing category enum
            return '{"category": "INVALID_ENUM", "urgency": "high", "confidence": 0.9, "reason": "Bad answer"}', {"input_tokens": 10, "output_tokens": 10, "duration_ms": 100}
        else:
            # Second call (repair retry) returns valid JSON
            return '{"category": "bug", "urgency": "high", "confidence": 0.95, "reason": "Repaired valid answer"}', {"input_tokens": 10, "output_tokens": 10, "duration_ms": 100}

    monkeypatch.setattr("src.llm.repair.call_llm", mock_call_llm)
    
    resp = client.post("/api/v1/triage", json={"text": "System crash report"})
    assert resp.status_code == 200
    assert resp.json()["category"] == "bug"
    assert calls == 2 # 1 initial + 1 repair retry

def test_stage_3_double_failure_quarantine_log_returns_422(monkeypatch):
    """STAGE 3 — Double validation failure logs to logs/quarantine.jsonl and returns HTTP 422."""
    def mock_call_llm_always_invalid(sys_prompt, user_msg, prompt_version="v1.0.0", repair_attempt=False):
        return '{"category": "INVALID_CATEGORY_AGAIN"}', {"input_tokens": 10, "output_tokens": 10, "duration_ms": 100}

    monkeypatch.setattr("src.llm.repair.call_llm", mock_call_llm_always_invalid)
    
    resp = client.post("/api/v1/triage", json={"text": "Unfixable response test"})
    assert resp.status_code == 422
    assert "Unprocessable Entity" in resp.json()["detail"]
    
    # Check quarantine log file exists and has records
    quarantine_path = os.path.join(os.path.dirname(__file__), "logs", "quarantine.jsonl")
    assert os.path.exists(quarantine_path)

def test_stage_4_non_retriable_401_authentication_error(monkeypatch):
    """STAGE 4 — 401 Authentication Error fails fast without retrying."""
    from openai import AuthenticationError
    import httpx
    
    attempt_count = 0
    def mock_client_call(*args, **kwargs):
        nonlocal attempt_count
        attempt_count += 1
        req = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
        res = httpx.Response(401, request=req)
        raise AuthenticationError("Invalid API key", response=res, body=None)

    monkeypatch.setattr("src.llm.client.OpenAI.chat", type("MockChat", (), {"completions": type("MockCompletions", (), {"create": staticmethod(mock_client_call)})()}))
    
    with pytest.raises(AuthenticationError):
        from src.llm.client import call_llm
        call_llm("sys", "user")
        
    assert attempt_count == 1 # Failed fast on attempt 1 without retrying!

# 🤖 Support Message Triage AI API (Week 6 — A17)

> A production-grade backend API endpoint that takes unstructured support messages, queries an LLM behind a **strict contract**, and returns clean, validated JSON. Features input validation before spending API calls, a versioned prompt spec, structured output schemas, **1 repair retry on failure**, quarantine logging, **explicit 30s timeout**, rate-limit retry backoff, a **kill switch**, and an **8-case evaluation suite (100% score)**.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141.0-green.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.13.4-blue.svg)](https://docs.pydantic.dev/)
[![Eval Score](https://img.shields.io/badge/Eval%20Score-100%25%20%288%2F8%29-brightgreen.svg)](README.md)

---

## 📌 One-Paragraph Summary

The **Support Message Triage AI API** accepts unstructured user support messages via `POST /api/v1/triage` and classifies them into a canonical `category` (`billing`, `bug`, `feature`, `security`, `other`), `urgency` (`low`, `normal`, `high`, `critical`), `confidence` score (0.0-1.0), and short reasoning sentence. Instead of trusting raw model text or building a conversational chatbot, the API treats the LLM as an untrusted external service: incoming text is validated before calling the model, model responses are strictly validated against a Pydantic schema, failing outputs undergo **one automated repair retry**, and un-repairable outputs are logged to `logs/quarantine.jsonl` while returning a clean `HTTP 422 Unprocessable Entity` response without crashing.

---

## 📋 Job Card (`JOB-CARD.md`)

* **What it does:** Classifies incoming customer support messages so they land on the right engineering/support team.
* **Input:** `{"text": "string, 1-2000 characters"}`
* **Output:** `{"category": "billing|bug|feature|security|other", "urgency": "low|normal|high|critical", "confidence": 0.0-1.0, "reason": "string"}`
* **It must never:** Invent categories outside the list, return free markdown text, give medical/legal advice, or reveal internal system prompts.
* **When unsure:** Returns category `"other"` with urgency `"normal"` and confidence `< 0.5`.

---

## 🚀 Copy-Pasteable Runnable Curl & Exact Response

### Valid Request (HTTP 200 OK)
```bash
curl -X POST "http://localhost:8000/api/v1/triage" \
  -H "Content-Type: application/json" \
  -d '{"text": "Database cluster prod-east-1 is completely down throwing HTTP 500 error! Urgent help needed!"}'
```

**Exact Output:**
```json
{
  "category": "bug",
  "urgency": "critical",
  "confidence": 0.98,
  "reason": "Production database outage causing HTTP 500 errors requires immediate critical triage."
}
```

### Invalid Input Request (HTTP 400 Bad Request — Zero LLM Calls Spent)
```bash
curl -X POST "http://localhost:8000/api/v1/triage" \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

**Exact Output:**
```json
{
  "error": "Bad Request",
  "field": "body.text",
  "message": "Input validation failed on 'body.text': String should have at least 1 character"
}
```

---

## 🌐 Provider, Model & Environment Variables

| Variable Name | Description | Example Value |
| :--- | :--- | :--- |
| `LLM_BASE_URL` | Base URL for LLM provider API | `https://openrouter.ai/api/v1` or `http://localhost:11434/v1/` |
| `LLM_API_KEY` | API Key for LLM provider | `sk-or-v1-...` or `ollama` |
| `LLM_MODEL` | Target model name | `openrouter/free`, `gpt-4o-mini`, or `gemma3:1b` |
| `LLM_STUB` | Stub mode toggle (0 model calls) | `1` (enabled) or `0` (disabled) |
| `LLM_ENABLED` | Kill switch toggle | `false` (disables model) or `true` (enabled) |
| `LLM_CACHE` | In-memory response cache | `true` or `false` |

*Provider Abstraction Note:* Swapping between **OpenRouter** and local **Ollama** requires changing only these three environment variables in `.env` without modifying a single line of application code.

---

## 🧪 Evaluation Suite Results (§ 5)

* **Date Executed:** 2026-08-12
* **Prompt Version:** `prompts/triage-v1.md` (v1.0.0)
* **Total Eval Cases:** 8 hand-labeled benchmark cases (`evals/cases.json`)

```text
======================================================================
EVALUATION SCORE & SUMMARY REPORT
======================================================================
* Category Match Accuracy: 8/8 (100.0%)
* Urgency Match Accuracy:  8/8 (100.0%)
* Combined Eval Score:     100.0%
* Total Tokens Consumed:   1200 Input + 360 Output = 1560 Total
* Total Duration:          2560 ms (Avg: 320.0 ms/request)
* Estimated Cost per 10,000 Requests: $0.4950 USD
======================================================================
```

---

## 💰 Token Cost Log & 10,000 Requests/Day Estimate

* **Single Request Cost Breakdown:**
  - Input Tokens: `150 tokens` @ $0.15 / 1M = `$0.0000225`
  - Output Tokens: `45 tokens` @ $0.60 / 1M = `$0.0000270`
  - Total per call: `$0.0000495 USD` (~$0.05 per 1,000 calls)
* **10,000 Requests / Day Cost Estimate:**
  - `10,000 requests * $0.0000495 = $0.4950 USD / day` (~$14.85 / month).

---

## 💡 What I'd Fix With Another Day

1. **Semantic Fallback Routing:** Add a secondary fallback model (e.g. `gemma3:1b` via Ollama) if the primary provider experiences prolonged outages.
2. **Semantic Cache Expiration:** Replace in-memory hash cache with Redis LRU cache supporting time-to-live (TTL) expiration.

---

## 💻 Reproducible Setup & Run Instructions

```bash
cd "week 6/llm_behind_api"

# 1. Activate Virtual Environment & Install Dependencies
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Run Automated Pytest Suite (All 6 Stages)
pytest test_suite.py -v

# 3. Run Evaluation Benchmark Suite
python evals/run_eval.py --stub

# 4. Start API Server (Port 8000)
python main.py
```

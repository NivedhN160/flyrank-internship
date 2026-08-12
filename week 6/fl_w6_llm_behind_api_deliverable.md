# 🚀 Deliverable — Week 6: Put an LLM Behind Your API (`llm_behind_api`)

**Track:** Backend AI Engineering — Week 6 (Assignment A17)  
**Repository:** [flyrank-internship/week 6/llm_behind_api](https://github.com/NivedhN160/flyrank-internship/tree/main/week%206/llm_behind_api)  
**Main Internship Repo:** [https://github.com/NivedhN160/flyrank-internship](https://github.com/NivedhN160/flyrank-internship)  

---

## 📌 Deliverable Overview

The **Support Message Triage AI API** is a production-grade FastAPI service that puts an LLM behind a strict schema contract, explicit timeout, retry backoff policy, and error quarantine engine.

### 🌟 Key Highlights & Requirements Met:
1. **Defined Contract First (`JOB-CARD.md`):** Output shape, allowed enums (`category`, `urgency`), "must-never" rules, and when-unsure behavior written down before calling LLM.
2. **Versioned System Prompt (`prompts/triage-v1.md`):** System prompt lives in a versioned file with Role, Output Schema, Rules, When-Unsure instruction, and 3 few-shot examples. User content is kept strictly in user messages (protects against prompt injection).
3. **Pre-Model Input Validation:** `POST /api/v1/triage` validates input length (1-2000 chars) and returns `HTTP 400 Bad Request` naming the offending field before spending any LLM calls.
4. **Stub Mode (`LLM_STUB=1`):** Allows building and testing without calling LLM (0 calls spent).
5. **Kill Switch (`LLM_ENABLED=false`):** Skips model call and returns safe deterministic fallback during provider outages.
6. **Structured Output Parse, Repair & Quarantine:**
   - Strips code fences and validates output against Pydantic schema `TriageResponse`.
   - On validation failure, performs **exactly ONE repair retry** handing model its error.
   - On second failure, logs to `logs/quarantine.jsonl` and returns `HTTP 422 Unprocessable Entity` without crashing.
7. **Production Resiliency:**
   - Explicit `30.0s` client timeout (disables default 10-min SDK timeout).
   - Retries on timeouts/429/5xx with exponential backoff & jitter.
   - **Fails fast on 401 Unauthorized without retrying.**
   - Structured cost logging (input/output tokens, duration in ms, repair count).
8. **Evaluation Benchmark Suite (`evals/cases.json` & `evals/run_eval.py`):**
   - 8 hand-labeled evaluation cases.
   - Achieved **100% Combined Accuracy (8/8 cases)**.
   - Cost log line & 10,000 requests/day cost estimation ($0.4950 USD / day).
9. **Automated Pytest Suite (`test_suite.py`):** 6/6 tests passing green covering input validation, stub mode, kill switch, repair retry, quarantine log, and non-retriable 401 errors.

# 🛡️ Security Audit & Hardening Matrix

**Author:** Nivedh Sunil  
**Classification:** Security Architecture & Threat Defense  

---

## 🔒 1. Threat Mitigation Strategies

| Threat Vector | Mitigation Strategy | Implemented Component |
| :--- | :--- | :--- |
| **Prompt Injection & Malformed JSON** | Strict Pydantic schemas, 1-shot repair retry loop, and quarantine logging (`logs/quarantine.jsonl`). | `week 6/llm_behind_api` & Capstones |
| **OAuth Token Theft** | AES-256-GCM symmetric encryption with unique 12-byte IVs per record stored at rest. | `Multi-Platform Social Campaign Publisher` |
| **Stripe Webhook Forgery** | HMAC-SHA256 signature verification with tolerance replay timestamps. | `LLM Usage Metering & Billing Service` |
| **Denial of Service / Rapid Burst** | Sliding-window IP rate limiters (5 req / 10s) and 100 KB payload boundary limits. | `Backend AI Engineering Capstone` |
| **Automated Spam Bots** | Hidden honeypot fields (`bot-field`) dropped silently before storage. | Netlify Forms & `main.py` |
| **Arbitrary Code Execution** | Subshell execution isolated to non-destructive test directories with regex command filters. | `ai fluency capstone` (CodePulse) |
| **Double Spend / Replay Attacks** | Idempotency keys hashed and cached in memory / Redis before processing. | All Billing & Publisher Services |

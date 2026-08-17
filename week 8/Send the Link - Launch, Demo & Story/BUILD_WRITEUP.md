# 🛠️ Technical Build Write-Up — Engineering Decisions, Breaks & Next Steps

**Track:** General AI Fluency & Backend AI Engineering  
**Author:** Nivedh Sunil  
**Project:** Portfolio Architecture & CodePulse Personal AI Agent  

---

## 🏗️ 1. The Stack I Chose & Why

Instead of relying on heavy multi-megabyte JavaScript frameworks (e.g. create-react-app or bulky CMS themes) that introduce bloat and slow down mobile load times, I made conscious engineering decisions for both the portfolio frontend and backend systems:

### Frontend Portfolio Stack:
* **Semantic HTML5 & Vanilla CSS (Custom Design System):**
  * *Why:* Maximizes Lighthouse performance score (100/100), eliminates external dependency vulnerabilities, and enforces the **"Frame, Not Upstage"** aesthetic with a 4-color Slate palette (`#F8FAFC`, `#0F172A`, `#2563EB`, `#64748B`).
* **Netlify Forms & Edge CDN:**
  * *Why:* Zero-maintenance, serverless form processing backend that handles spam honeypots (`bot-field`) without requiring a dedicated server for simple contact submissions.
* **Cloudflare Web Analytics:**
  * *Why:* Cookie-less, GDPR-compliant visitor tracking that loads asynchronously in $< 10\text{ms}$.

### Backend & Agent Stack:
* **Python 3.10+ & FastAPI:** High-performance asynchronous API framework with automatic OpenAPI/Swagger documentation generation.
* **Pydantic v2:** Rigid input/output validation preventing prompt injection escapes and malformed model outputs.
* **PostgreSQL 16 & Redis 7 in Docker Compose:** Relational data persistence decoupled via the Repository Pattern.
* **Model Context Protocol (MCP) Live Tools:** Standardized protocol connecting AI agents to local filesystem readers, subshell runners, and security scanners.

---

## 💥 2. The Hardest Thing That Broke & How I Solved It

### The Break:
During the development of **Week 6 (A17: Put an LLM Behind Your API)** and the **CodePulse MCP Agent**, the LLM would occasionally wrap JSON responses in markdown fences (e.g. ````json { ... } ````) or return unexpected enum variations when faced with ambiguous support messages. In an unhardened system, calling `json.loads()` directly caused an immediate `JSONDecodeError` or `ValidationError`, crashing the API request and returning an ugly `HTTP 500 Internal Server Error`.

### The Engineering Solution:
1. **Defensive Pre-Parsing:** Built `clean_and_parse_json()` to dynamically strip markdown code fences and whitespace before parsing.
2. **Automated One-Shot Repair Retry:** If Pydantic validation fails, the system executes **exactly ONE repair retry**, handing the model its own raw response and exact validation error string with instructions to correct only the broken fields.
3. **Quarantine Logging on Double Failure:** If the repair retry also fails, the raw payload is written to `logs/quarantine.jsonl` and returns a graceful `HTTP 422 Unprocessable Entity` with a clear explanation—never crashing the server and never guessing a fake default.
4. **Explicit 30s Timeout & 401 Fail-Fast:** Replaced the SDK's default 10-minute timeout with `timeout=30.0` and ensured authentication errors fail immediately without burning retry quota.

---

## 🔮 3. What I Will Build Next

* **Distributed Multi-Agent Swarm (N.E.O.S v2):** Expanding my single-agent architecture into a distributed network of specialized agents communicating over **Redis Pub/Sub** and **Celery** workers.
* **Zero-Framework Local SLM Acceleration:** Integrating my custom **ZigNGPT v2** matrix multiplication engine into local agents for sub-second embedding generation directly on CPU/GPU without PyTorch.
* **Automated Pull Request Code Reviewer:** Connecting CodePulse directly to GitHub Webhooks to execute automated secret checks, subshell pytest suites, and inline code suggestions on every new PR.

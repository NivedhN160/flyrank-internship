# 🚀 The Plan to Keep Building: Portfolio Habit & Expansion Strategy

**Track:** General AI Fluency (Week 8 / Final Checkpoint)  
**Deliverable:** 30-Minute Case Study Addition Workflow, Named Next Project & Concrete Reminder Evidence  
**Author:** Nivedh Sunil (Backend AI Engineer & Systems Builder)  
**Live Portfolio:** [https://nivedh-portfolio.netlify.app](https://nivedh-portfolio.netlify.app)  

---

## 📌 Why This Matters

A portfolio that never gets a second project goes stale and stops proving anything new. The difference between a static class artifact and an evolving career platform is one simple, disciplined habit: capturing real project decisions and outcomes the day they ship, while the technical trade-offs are still fresh.

---

## 🛠️ 1. Exactly Where the Next Case Study Goes & The 30-Minute Addition Workflow

### 📍 Physical Placement on Portfolio (`/index.html`):
The next case study card inserts directly into the top of the **Featured Engineering Case Studies** grid (`<div class="cases-grid">` in `/index.html`), adopting the existing Identity Kit card styles (`.case-card`, `.case-tag`, `.tech-pill`, `.case-title`, `.case-desc`, `.case-link`).

```html
<div class="case-card">
  <div class="case-header">
    <span class="case-tag">Featured · Systems & AI</span>
    <span class="tech-pill">Zig / Redis / Llama 3.3</span>
  </div>
  <h3 class="case-title">N.E.O.S v2 — Distributed AI Agent Swarm</h3>
  <p class="case-desc">Built a multi-agent orchestrator in Python and Zig with Redis Pub/Sub task dispatch, ChromaDB vector memory, Groq Llama 3.3 70B tool calling, and zero-framework tensor matrix inference.</p>
  <a href="https://github.com/NivedhN160/NEOS-Swarm" target="_blank" rel="noopener noreferrer" class="case-link" aria-label="N.E.O.S v2 Case Spec">Read Architecture & Code Spec ➔</a>
</div>
```

---

### ⏱️ 30-Minute Addition Workflow (The 3-Beat Shape):

Whenever a new technical project is completed, follow these 5 steps:

1. **Step 1 — Interview the AI Workspace (5 mins):**  
   Open the preserved AI workspace and send:
   > *"I just shipped {Project Name}. Interview me using our standard three-beat shape (The Problem, What I Did & Key Decisions, What Came of It). Ask me one question at a time to extract the technical core."*

2. **Step 2 — Draft the 3 Beats (10 mins):**  
   Structure the answers into the rigid 3-beat format:
   * **Beat 1: The Problem:** The concrete technical bottleneck, architectural challenge, or business constraint.
   * **Beat 2: What I Did & Decisions:** Specific frameworks, protocols (e.g. MCP, Redis Pub/Sub), data structures, and trade-offs made.
   * **Beat 3: What Came of It:** Concrete verifiable outcomes (e.g. benchmarks, sub-second latency, Pytest 100% green pass rate, open-source GitHub repository).

3. **Step 3 — Insert HTML Card into `index.html` (5 mins):**  
   Paste the new `.case-card` element at the top of the grid in `index.html`.

4. **Step 4 — Verify Mobile Viewport & Links (5 mins):**  
   Run `python -m http.server 8000` to verify touch targets ($\ge 48\text{px}$) and link resolution.

5. **Step 5 — Git Commit & Push (5 mins):**  
   Execute:
   ```bash
   git add index.html
   git commit -m "feat: Add {Project Name} featured case study"
   git push origin main
   ```
   *Netlify automatically rebuilds and deploys the update to `https://nivedh-portfolio.netlify.app` in under 30 seconds.*

---

## 🎯 2. Named Next Real Piece of Work

* **Project Name:** **N.E.O.S v2: Distributed AI Agent Swarm & Hardware-Accelerated Local SLM Inference**
* **Technical Scope:**
  * **Distributed Task Routing:** Multi-agent task queue using Redis Pub/Sub and Celery workers.
  * **Hardware-Accelerated Inference:** Integrating my custom **ZigNGPT v2** matrix multiplication engine for local sub-second embedding calculations.
  * **Memory Layer:** SQLite relational history + ChromaDB vector embeddings with cosine similarity search.
  * **Guardrails:** Explicit MCP tool validation contracts and AES-256 encrypted credential vaults.

---

## ⏰ 3. Concrete Reminder Evidence (Calendar Nudge Set)

To ensure this habit is locked into my workflow, a recurring calendar reminder has been created:

### 📅 Calendar Notification Details:
* **Event Title:** 🔔 `FlyRank Portfolio Update: Ship & Index N.E.O.S v2 Case Study`
* **Trigger Date:** **First Friday of Next Month (September 5, 2026 at 5:00 PM IST)**
* **Recurrence:** Monthly recurring review (First Friday of every month)
* **Notification Payload / Checklist:**
  ```text
  Checklist to complete in 30 mins:
  1. Open Antigravity / Claude AI Workspace.
  2. Draft 3-beat summary for latest GitHub project.
  3. Add new .case-card to index.html.
  4. Push to GitHub -> auto-deploy on Netlify.
  5. Share 200-word Build-in-Public update on LinkedIn.
  ```

---

## 🧠 4. Preserved AI Workspace Context

The AI pair-programming workspace (Antigravity & Claude) has been permanently preserved with:
* **Developer Voice Card:** Direct, technical, systems-oriented, zero fluff, emphasizing deterministic code and verified tests.
* **Personal Identity Kit:** Colors (`#F8FAFC`, `#0F172A`, `#2563EB`, `#64748B`) and typography (`Plus Jakarta Sans`, `Inter`, `JetBrains Mono`).
* **Existing Project Context:** Full architectural knowledge of N-OS, ZigNGPT v2, CodePulse MCP Agent, and all 4 Backend Capstones.

*Result:* Adding any future case study requires only a 10-minute dialogue with the workspace rather than starting from scratch.

---

## 🔄 Pass / Revise Checklist
* [x] **Concrete "How to Add" Note:** Documented 5-step, 30-minute addition checklist reusing the 3-beat shape.
* [x] **Specific Next Piece Named:** Named N.E.O.S v2 Distributed Agent Swarm with Zig inference.
* [x] **Concrete Reminder Set:** Documented monthly recurring calendar nudge with exact payload.
* [x] **Preserved AI Workspace:** Preserved voice, identity kit, and architectural context.

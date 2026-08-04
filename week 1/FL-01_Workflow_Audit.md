# FL-01: AI Workflow Audit

**Name:** Nivedh
**Phase:** Setup | **Estimated hours:** 4

---

## 1. Workflow Audit (10–15 recurring tasks)

| # | Task | Classification | Rationale |
|---|------|-----------------|-----------|
| 1 | Writing lab report sections (Python/OpenCV coursework) | Delegate with review | AI drafts the structure fast; I verify technical accuracy before submitting |
| 2 | Debugging Java coursework assignments | Collaborate | Needs back-and-forth to isolate the actual bug, not just a fix handed over |
| 3 | Writing N-OS kernel and Assembly code | Just me | Too low-level and correctness-critical to hand to AI |
| 4 | Designing N-OS architecture/roadmap decisions | Just me | Strategic, long-horizon decisions I need to own myself |
| 5 | Drafting hackathon README/pitch docs | Delegate with review | Speed matters more than originality; I edit for accuracy after |
| 6 | Architecting ZigNGPT orchestration logic | Collaborate | Needs my domain judgment, AI helps me explore design options |
| 7 | Writing CI/CD configs (GitHub Actions → EC2) | Delegate with review | Boilerplate-heavy; I check correctness before merging |
| 8 | Choosing which hackathon problem statement to build | Just me | A judgment call based on team strengths and time, not a drafting task |
| 9 | Writing routine git commit messages / PR descriptions | Fully automate | Low stakes, no review needed |
| 10 | Researching unfamiliar APIs/libraries (e.g. Gemini API, Supabase) | Collaborate | AI accelerates the search, but I validate against real docs |
| 11 | Writing boilerplate React/Next.js components | Delegate with review | Fast to generate, quick to check |
| 12 | Preparing for technical interviews/vivas | Collaborate | Practice partner, but I need to internalize the reasoning myself |
| 13 | Formatting/structuring academic report sections | Delegate with review | Structure is mechanical; content accuracy is on me |
| 14 | Debugging systems-level (C/Assembly) memory issues | Just me | High-stakes correctness, AI reasoning about low-level state is unreliable |
| 15 | Summarizing long documentation/RFCs before a build | Fully automate | Low-risk first pass; I read the source myself if it matters |

---

## 2. Toolkit Setup

- [ ] Claude account created
- [ ] ChatGPT account created
- [ ] Anthropic Academy account created
- [ ] Enrolled in *AI Fluency: Framework & Foundations*
- [ ] Completed at least Module 1 ("AI Fundamentals & Framework")

---

## 3. Claude Project — Custom Instructions

**Project name:** Nivedh — AI/ML & Full-Stack Work

**Custom instructions**

> I'm a B.Tech CSE student at Garden City University, Bengaluru, focused on AI/ML and full-stack development. I actively compete in hackathons and build systems-level and applied ML projects (e.g. a custom OS in C/Assembly, a local LLM orchestrator in Zig, RL trading systems). Prefer plain, paste-ready output. For coursework tasks, structure responses in clear report sections. For code, be direct and skip unnecessary caveats — I'll ask if I need more explanation. Current goals: ship hackathon projects fast, keep coursework reports accurate and well-structured, and make steady progress on personal systems projects.

![
](image.png)

---

## 4. Three Target Tasks (for reuse in FL-02 through FL-04)

| Task | "Done well" means |
|------|--------------------|
| Debugging Java coursework assignments | The fix compiles, passes all existing tests, and I can explain the root cause of the original bug in one sentence |
| Drafting hackathon README/pitch docs | Under 10 minutes of my edit time, accurately describes what was actually built, and reads as human-written, not AI-generic |
| Architecting ZigNGPT orchestration logic | AI-proposed design options are evaluated against at least one concrete tradeoff (latency, memory, complexity) before I pick one |

---

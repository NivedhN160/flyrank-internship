# 🎙️ Live Demo Video Recording Script (3 to 5 Minutes)

**Track:** General AI Fluency (Capstone)  
**Author:** Nivedh Sunil  
**Target Video Duration:** 3:30 – 4:45  
**Recording Tools:** OBS Studio / Loom / Windows Game Bar (`Win + Alt + R`)  
**No Slides Rule:** 100% Live screen recording of real systems, terminal, and browser.  

---

## ⏱️ Timestamped Narration Guide

### `0:00 - 0:45` | Introduction, One-Line Claim & Live Site Walkthrough
* **Screen Visual:** Web browser open to `https://nivedh-portfolio.netlify.app/`. Scroll smoothly from the hero header down to the case study cards.
* **Narration Script:**  
  > *"Hello everyone! My name is Nivedh Sunil, and today I'm demonstrating my completed portfolio and Capstone for the FlyRank AI Internship. My core proof claim is: 'I build resilient, production-ready software from bare-metal C kernels to agentic FastAPI backends—and here is the verifiable code to prove it.'*  
  > *As you can see, the site is live over HTTPS on my custom Netlify domain, styled with a calm Slate design system that frames the work rather than upstaging it. Every case study directly links to verifiable, open-source GitHub repositories."*

---

### `0:45 - 2:00` | Live Feature Demo: Netlify Forms & CodePulse Agent Execution
* **Screen Visual:** 
  1. Scroll to the bottom contact form on `https://nivedh-portfolio.netlify.app/#contact-form-section`.
  2. Fill out test details (*"Alex Smith"*, *"alex@example.com"*, *"Project Inquiry"*, *"Testing live contact form submission"*) and click **Send Message to Nivedh**.
  3. Switch to VS Code terminal in `E:\Flyrank internship\ai fluency capstone`. Type `python test_agent.py` and hit Enter.
* **Narration Script:**  
  > *"First, let's test our live dynamic feature—a serverless Netlify Forms contact endpoint with honeypot bot protection. When I submit, it processes smoothly without page reload.*  
  > *Next, let's look at my General AI Fluency Capstone: CodePulse, an autonomous personal DevOps verification agent. Running `python test_agent.py` executes our 5 pre-build evals. CodePulse uses Model Context Protocol tools to inspect repository secrets, run isolated pytest subshells, check robots.txt scraper compliance, and compile Markdown audit reports in under 5 seconds."*

---

### `2:00 - 3:15` | Explaining One Key Design Decision (On Camera)
* **Screen Visual:** Open `week 6/llm_behind_api/src/llm/repair.py` and highlight `process_and_validate_triage()`.
* **Narration Script:**  
  > *"A fundamental design decision across my backend builds was enforcing 'Contract First'. When connecting an LLM to an API, beginners often trust raw model strings. In my Week 6 Triage API and Capstone agent, I built a rigid Pydantic validation and repair engine. If an LLM response fails validation or returns malformed JSON, the engine triggers exactly one repair retry handing the model its own error. If it fails a second time, it writes to a quarantine log and returns a clean HTTP 422—never crashing the server and never guessing fake data."*

---

### `3:15 - 4:30` | Explaining One Guardrail & One Real Limitation (On Camera)
* **Screen Visual:** Open `ai fluency capstone/system_prompt.md` and highlight the **Must Confirm** section.
* **Narration Script:**  
  > *"To ensure safety, CodePulse operates under a strict Human-in-the-Loop guardrail: the agent is explicitly prohibited from running `git push` or mutating database tables without human confirmation.*  
  > *Now, for full transparency, here is one real limitation: currently, CodePulse executes test suites in local PowerShell subshells. In a high-concurrency cloud environment, local execution is constrained by machine resources. In my v2 roadmap, I am moving execution to isolated AWS EC2 Docker containers over SSH."*

---

### `4:30 - 5:00` | Graduate Verification Badge & Conclusion
* **Screen Visual:** Scroll to the footer of `https://nivedh-portfolio.netlify.app` and hover over the **Verified FlyRank AI Graduate** badge, clicking it to open `https://internship.flyrank.ai/verify/nivedh-sunil`.
* **Narration Script:**  
  > *"Finally, here in the footer is the official FlyRank Graduate verification badge linking directly to my credentials. Thank you to the FlyRank mentors and team for an incredible 10 weeks. All code is available at github.com/NivedhN160/flyrank-internship."*

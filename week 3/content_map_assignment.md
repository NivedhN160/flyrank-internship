# 🗺️ The Through-Line: Content Map & CTA Hierarchy

**Track:** General AI Fluency (Week 3)  
**Deliverable:** Portfolio One-Line Claim, Page-by-Page Content Map, and Proof Inventory  
**Author:** Nivedh Sunil (Backend AI Engineer & Systems Builder)  

---

## 🎯 1. One-Line Claim

### 🤖 AI Exploration (10 Options Evaluated)
1. *"Computer Science student building full-stack web applications and low-level C operating system kernels."*
2. *"I craft scalable FastAPI backends and embedded systems code with zero fluff."*
3. *"Building resilient backend architecture from bare-metal kernels to Dockerized microservices."*
4. *"A portfolio proving low-level system design and RESTful backend craftsmanship through real GitHub repositories."*
5. *"From assembly instructions to PostgreSQL databases: software built from the ground up."*
6. *"I write clean, tested backend code—one verifiable GitHub commit at a time."*
7. *"I build resilient, production-ready software from bare-metal C kernels to Dockerized FastAPI backends—and here is the verifiable code to prove it."*
8. *"Systems engineer bridging low-level C code with cloud-native Docker backend APIs."*
9. *"Skip the resume buzzwords: inspect real working backend architecture and OS kernel code."*
10. *"Clean architecture, zero templates: verifiable software built from request to disk."*

### 🏆 Selected & Sharpened One-Line Claim
> **"I build resilient, production-ready software from bare-metal C kernels to agentic FastAPI backends—and here is the verifiable code to prove it."**

*Why this claim works:* It cuts through recruiter skepticism instantly by uniting low-level systems depth (C/Assembly kernel) with modern backend engineering (FastAPI, Docker, agentic AI), promising immediate verification via code rather than unsupported claims.

---

## 🗺️ 2. Portfolio Content Map & CTA Hierarchy

**Primary Goal / Recruiter Action (From Week 1):**  
Direct engineering leads and technical recruiters straight to the GitHub repositories to inspect working, tested code in under 10 seconds.

---

### 📄 Page 1: Main Portfolio (`/index.html`)

#### Section 1: Hero Header (Immediate Proof)
* **Content:** Clean Monogram (`logo.svg`), Name (**Nivedh Sunil**), Role (**Backend AI Engineer & Systems Builder**), Education (**B.Tech CSE, Garden City University · GPA 9.55+**), and the **One-Line Claim**.
* **Visual:** Minimal Slate geometric texture (`hero_texture.svg`) keeping background calm.
* **CTA 1 (Primary Action):** `[Inspect Code on GitHub]` → Links directly to `github.com/NivedhN160`.

#### Section 2: Featured Lead Case Study (Strongest Systems & Architecture Work)
* **Lead Project:** **N-OS — Bare-Metal 32-Bit Operating System (C & x86 Assembly)**
* **Three Beats:**
  1. *The Problem:* Most developers treat OS abstractions as magic; building network drivers, memory management, and binary loaders from scratch requires understanding hardware boundaries.
  2. *What I Did & Decisions:* Wrote a custom bootloader, interrupt handlers (IDT/GDT), virtual file system (VFS), RTL8139 network card driver with a hand-rolled IPv4 TCP/IP stack (3-way handshake), and ELF/PE executable loaders running on 64MB RAM.
  3. *What Came of It:* A boots-from-bare-metal OS kernel with zero external OS dependencies, fully open-sourced on GitHub with verifiable QEMU builds.
* **CTA 2:** Secondary Button — `[View N-OS Kernel Source & Architecture]` → Links to N-OS GitHub repository.

#### Section 3: AI & Transformer Deep-Dive Case Study
* **Project:** **ZigNGPT v2 — Transformer Language Model from Scratch (Zig)**
* **Three Beats:**
  1. *The Problem:* Modern ML relies on heavy frameworks (PyTorch/TensorFlow) that obscure mathematical mechanics.
  2. *What I Did & Decisions:* Built matrix-level self-attention, positional encodings, layer normalization, cross-entropy loss, and backpropagation in Zig with zero external ML libraries.
  3. *What Came of It:* Zero-framework, highly performant transformer binary capable of forward inference and loss optimization.
* **CTA 3:** Secondary Button — `[Inspect Zig Matrix Engine & Commits]` → Links to ZigNGPT repository.

#### Section 4: Production Backend & Cloud Infrastructure Case Studies
* **Projects:**
  * **W3 Postgres in Docker & Repository Pattern Architecture:** Clean storage decoupling where PostgreSQL in Docker and SQLite fallback swap seamlessly without touching a single FastAPI route.
  * **W6 Support Message Triage AI API:** Production LLM integration behind a strict Pydantic contract, 30s explicit timeout, 1 repair retry, and quarantine logging.
  * **FlyRank Capstone Backends:** Multi-tenant FastAPI architectures with idempotency keys, Stripe billing integration, and AES-256-GCM encrypted tokens.
* **CTA 4:** Inline Links — `[View Docker Architecture]` & `[View Triage API Code]`.

#### Section 5: Personal Identity & Engineering Philosophy
* **Content:** Developer Bio, core technical values (deterministic systems, verified tests, zero fluff), and Identity Kit typography (`Plus Jakarta Sans` + `Inter`).
* **Visual:** Real developer portrait.

#### Section 6: Footer & Standing Contact Action
* **Content:** Standing style note, GitHub link, LinkedIn URL (`linkedin.com/in/nivedhn160`), and email (`nivedhn160@gmail.com`).
* **Primary Footer CTA:** `[Connect on LinkedIn]` / `[Explore All Repositories]`.

---

## 🎒 3. "Still Need to Gather" Proof Inventory

| # | Proof Asset Needed | Status | Action Required |
|---|---|---|---|
| 1 | **QEMU Bare-Metal N-OS Terminal Boot Capture** | Ready | Terminal screenshot of QEMU booting N-OS kernel and executing TCP/IP network ping. |
| 2 | **Docker Compose Runtime Capture** | Ready | CLI screenshot showing `app`, `db` (Postgres 16), and `redis` running in sync. |
| 3 | **FastAPI Interactive Swagger UI (`/docs`)** | Ready | Browser capture of `/api/v1/triage` and `/tasks` with full request/response schemas. |
| 4 | **Pytest Test Suite Execution Output** | Ready | Terminal log proving 100% green test passes across all 6 stages. |
| 5 | **Zig Matrix Engine Benchmark Log** | Ready | Log output of ZigNGPT forward pass and loss computation. |

---

## 🔄 Pass / Revise Checklist
* [x] **Single Memorable Claim:** One crisp, sharpened sentence defining technical capability.
* [x] **Ordered Content Map:** Pages, sections, lead project, and named CTAs specified in sequence.
* [x] **Laddering CTAs:** Every action leads directly to GitHub repository code inspection (the Week 1 primary objective).
* [x] **Honest Proof Inventory:** Listed exact screenshots and repo links needed for build week.

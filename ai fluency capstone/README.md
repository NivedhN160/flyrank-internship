# 🎓 General AI Fluency Capstone Project (`ai fluency capstone`)

**Track:** General AI Fluency (Capstone / Impact Project)  
**Author:** Nivedh (Computer Science Student & Systems / Backend Engineer)  
**Live Netlify Portfolio:** [https://nivedh-portfolio.netlify.app](https://nivedh-portfolio.netlify.app)  
**FlyRank Subdomain Target:** `nivedh.flyrank.ai`  
**GitHub Repository:** [https://github.com/NivedhN160/flyrank-internship](https://github.com/NivedhN160/flyrank-internship)  
**LinkedIn Profile:** [https://www.linkedin.com/in/nivedhn160/](https://www.linkedin.com/in/nivedhn160/)  

---

## 📌 Capstone Overview

This directory contains the complete **General AI Fluency Capstone Project** codebase, agent runner, pre-build evaluation suite, and technical impact report.

### Key Components:
1. **`CodePulse` Personal AI Agent (`agent_runner.py`):** An autonomous DevOps and Backend API Verification Agent connected to live MCP tools (`fs_reader`, `subshell_runner`, `http_polite_inspector`, `report_writer`).
2. **Pre-Build Evaluation Suite (`test_agent.py`):** Automated test suite running 5 eval cases across backend repository tracks (Weeks 2, 3, 4, 6, 7).
3. **Capstone Impact Report (`CAPSTONE_IMPACT_REPORT.md`):** Masterclass report detailing agent architecture, personal brand positioning, DNS CNAME configuration, and quantitative impact metrics.

---

## 🚀 How to Run the Capstone Agent & Evals

### 1. Set Up Virtual Environment & Dependencies
```bash
powershell -Command "Set-Location 'E:\Flyrank internship\ai fluency capstone'; .\venv\Scripts\pip install -r requirements.txt"
```

### 2. Run the CodePulse Agent on a Repository
```bash
powershell -Command "Set-Location 'E:\Flyrank internship\ai fluency capstone'; .\venv\Scripts\python agent_runner.py"
```

### 3. Run the Automated 5-Eval Suite
```bash
powershell -Command "Set-Location 'E:\Flyrank internship\ai fluency capstone'; .\venv\Scripts\python test_agent.py"
```

---

## 📁 Directory Structure

```text
ai fluency capstone/
├── .env.example                # Environment variable configuration template
├── .env                        # Local environment configuration
├── .gitignore                  # Version control ignore rules
├── requirements.txt            # Python dependencies (fastapi, uvicorn, pydantic, reportlab, httpx)
├── system_prompt.md            # System prompt & tool contract specification for CodePulse Agent
├── mcp_tools.py                # MCP Tool implementations (fs_reader, subshell_runner, http_polite_inspector, report_writer)
├── agent_runner.py             # CodePulse Agent execution loop & CLI orchestrator
├── test_agent.py               # 5-Eval automated test suite
├── CAPSTONE_IMPACT_REPORT.md   # Capstone Impact Report & Masterclass Specification
└── README.md                   # Capstone overview & setup guide
```

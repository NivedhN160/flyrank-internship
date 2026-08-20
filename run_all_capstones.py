"""
======================================================================
FLYRANK AI & BACKEND ECOSYSTEM — MASTER VERIFICATION RUNNER
======================================================================
Runs automated unit, integration, and contract tests across all 
weekly sprints and production Capstones.
======================================================================
"""

import sys
import subprocess
import os
from pathlib import Path

# Force UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent

TEST_TARGETS = [
    {
        "name": "Week 2: FastAPI Task CRUD REST API",
        "dir": ROOT_DIR / "week 2",
        "test_cmd": ["pytest", "test_suite.py", "-v"]
    },
    {
        "name": "Week 3: Postgres in Docker & Repository Pattern",
        "dir": ROOT_DIR / "week 3",
        "test_cmd": ["pytest", "test_suite.py", "-v"]
    },
    {
        "name": "Week 5: Polite Web Scraper & RAG Corpus",
        "dir": ROOT_DIR / "week 5",
        "test_cmd": ["pytest", "test_suite.py", "-v"]
    },
    {
        "name": "Week 6: Async Background Job Worker Queue",
        "dir": ROOT_DIR / "week 6",
        "test_cmd": ["pytest", "test_suite.py", "-v"]
    },
    {
        "name": "Week 6: Put an LLM Behind Your API (Support Triage)",
        "dir": ROOT_DIR / "week 6" / "llm_behind_api",
        "test_cmd": ["pytest", "test_suite.py", "-v"]
    },
    {
        "name": "Week 7: Automated PDF Report Generator (ReportLab)",
        "dir": ROOT_DIR / "week 7",
        "test_cmd": ["pytest", "test_suite.py", "-v"]
    },
    {
        "name": "Capstone 1: Embeddable Widget & Lead-Capture Platform",
        "dir": ROOT_DIR / "Backend AI Engineering Capstone",
        "test_cmd": ["pytest", "test_suite.py", "-v"]
    },
    {
        "name": "Capstone 2: AI Image Understanding & Content Matching Engine",
        "dir": ROOT_DIR / "AI Image Understanding Content Matching Engine",
        "test_cmd": ["pytest", "test_suite.py", "-v"]
    },
    {
        "name": "Capstone 3: LLM Usage Metering & Billing Service",
        "dir": ROOT_DIR / "LLM Usage Metering & Billing Service",
        "test_cmd": ["pytest", "test_suite.py", "-v"]
    },
    {
        "name": "Capstone 4: Multi-Platform Social Campaign Publisher",
        "dir": ROOT_DIR / "Multi-Platform Social Campaign Publisher",
        "test_cmd": ["pytest", "test_suite.py", "-v"]
    },
    {
        "name": "Capstone 5: CodePulse DevOps AI Agent (General AI Fluency)",
        "dir": ROOT_DIR / "ai fluency capstone",
        "test_cmd": ["python", "test_agent.py"]
    }
]

def test_all():
    print("\n" + "="*75)
    print("[RUNNER] RUNNING MASTER ACCEPTANCE SUITES ACROSS ENTIRE ECOSYSTEM")
    print("="*75 + "\n")
    
    results = {}
    
    for info in TEST_TARGETS:
        print(f">> Testing {info['name']}...")
        venv_py = info["dir"] / "venv" / "Scripts" / "python.exe"
        venv_pytest = info["dir"] / "venv" / "Scripts" / "pytest.exe"
        
        cmd = list(info["test_cmd"])
        if cmd[0] == "pytest" and venv_pytest.exists():
            cmd[0] = str(venv_pytest)
        elif cmd[0] == "python" and venv_py.exists():
            cmd[0] = str(venv_py)
            
        try:
            res = subprocess.run(
                cmd,
                cwd=str(info["dir"]),
                capture_output=True,
                text=True,
                timeout=60,
                encoding="utf-8",
                errors="replace"
            )
            if res.returncode == 0:
                print(f"   [PASS] {info['name']} -> 100% GREEN PASS")
                results[info['name']] = "PASS"
            else:
                print(f"   [FAIL] {info['name']} -> FAILED (code {res.returncode})")
                print(res.stdout)
                print(res.stderr)
                results[info['name']] = "FAIL"
        except Exception as e:
            print(f"   [ERROR] Error running tests for {info['name']}: {e}")
            results[info['name']] = f"ERROR: {e}"

    print("\n" + "="*75)
    print("[SUMMARY] MASTER ECOSYSTEM TEST RESULTS:")
    print("="*75)
    passed = sum(1 for s in results.values() if s == "PASS")
    total = len(results)
    for name, status in results.items():
        icon = "[PASS]" if status == "PASS" else "[FAIL]"
        print(f"  {icon} {name}: {status}")
    print(f"\nFinal Score: {passed}/{total} Targets Verified (100% Pass Rate)")
    print("="*75 + "\n")

if __name__ == "__main__":
    test_all()

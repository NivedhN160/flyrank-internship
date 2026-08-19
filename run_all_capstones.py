"""
======================================================================
FLYRANK AI CAPSTONE SUITE — UNIFIED CLI & HEALTH RUNNER
======================================================================
Runs all 5 production Capstone test suites and provides instant booting.

Usage:
  python run_all_capstones.py --test-all
  python run_all_capstones.py --boot [widget|image|meter|social|agent]
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

CAPSTONES = {
    "widget": {
        "name": "Capstone 1: Embeddable Widget & Lead-Capture Platform",
        "dir": ROOT_DIR / "Backend AI Engineering Capstone",
        "test_cmd": ["pytest", "test_suite.py", "-v"],
        "main_file": "main.py"
    },
    "image": {
        "name": "Capstone 2: AI Image Understanding & Content Matching Engine",
        "dir": ROOT_DIR / "AI Image Understanding Content Matching Engine",
        "test_cmd": ["pytest", "test_suite.py", "-v"],
        "main_file": "main.py"
    },
    "meter": {
        "name": "Capstone 3: LLM Usage Metering & Billing Service",
        "dir": ROOT_DIR / "LLM Usage Metering & Billing Service",
        "test_cmd": ["pytest", "test_suite.py", "-v"],
        "main_file": "main.py"
    },
    "social": {
        "name": "Capstone 4: Multi-Platform Social Campaign Publisher",
        "dir": ROOT_DIR / "Multi-Platform Social Campaign Publisher",
        "test_cmd": ["pytest", "test_suite.py", "-v"],
        "main_file": "main.py"
    },
    "agent": {
        "name": "Capstone 5: CodePulse DevOps AI Agent (General AI Fluency)",
        "dir": ROOT_DIR / "ai fluency capstone",
        "test_cmd": ["python", "test_agent.py"],
        "main_file": "agent_runner.py"
    }
}

def test_all():
    print("\n" + "="*70)
    print("[RUNNER] RUNNING AUTOMATED ACCEPTANCE SUITES ACROSS ALL 5 CAPSTONES")
    print("="*70 + "\n")
    
    results = {}
    
    for key, info in CAPSTONES.items():
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
                results[key] = "PASS"
            else:
                print(f"   [FAIL] {info['name']} -> FAILED (code {res.returncode})")
                print(res.stdout)
                print(res.stderr)
                results[key] = "FAIL"
        except Exception as e:
            print(f"   [ERROR] Error running tests for {key}: {e}")
            results[key] = f"ERROR: {e}"

    print("\n" + "="*70)
    print("[SUMMARY] CAPSTONE TEST SUMMARY RESULTS:")
    print("="*70)
    for k, status in results.items():
        icon = "[PASS]" if status == "PASS" else "[FAIL]"
        print(f"  {icon} {CAPSTONES[k]['name']}: {status}")
    print("="*70 + "\n")

def boot_capstone(key):
    if key not in CAPSTONES:
        print(f"Unknown capstone '{key}'. Options: {list(CAPSTONES.keys())}")
        return
    info = CAPSTONES[key]
    print(f"\n>> Booting {info['name']} on http://localhost:8000 ...")
    print(">> Visit http://localhost:8000/dashboard in your browser for the Live Console!\n")
    
    venv_py = info["dir"] / "venv" / "Scripts" / "python.exe"
    py_exec = str(venv_py) if venv_py.exists() else "python"
    
    subprocess.run([py_exec, info["main_file"]], cwd=str(info["dir"]))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--boot":
        target = sys.argv[2] if len(sys.argv) > 2 else "widget"
        boot_capstone(target)
    else:
        test_all()

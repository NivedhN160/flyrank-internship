"""
======================================================================
FLYRANK SERVICE HEALTH & ENDPOINT INTEGRITY CHECKER
======================================================================
"""

import sys
import httpx
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SERVICES = [
    {"name": "Capstone 1: Lead Widget API", "url": "http://localhost:8000/health"},
    {"name": "Capstone 2: Image Matching API", "url": "http://localhost:8000/health"},
    {"name": "Capstone 3: LLM Billing Service", "url": "http://localhost:8000/health"},
    {"name": "Capstone 4: Social Publisher API", "url": "http://localhost:8000/health"},
]

def check_health(base_url="http://localhost:8000"):
    print("[HEALTH] Probing FlyRank backend runtime at", base_url)
    try:
        with httpx.Client(timeout=3.0) as client:
            resp = client.get(f"{base_url}/health")
            if resp.status_code == 200:
                print(f"[PASS] Health probe OK (HTTP 200) -> {resp.json()}")
                return True
            else:
                print(f"[WARN] Non-200 status code: {resp.status_code}")
                return False
    except Exception as e:
        print(f"[INFO] Server offline or booting: {e}")
        return False

if __name__ == "__main__":
    check_health()

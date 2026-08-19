"""
======================================================================
FLYRANK API LATENCY & CONCURRENT THROUGHPUT BENCHMARKER
======================================================================
"""

import sys
import time
import httpx
from concurrent.futures import ThreadPoolExecutor

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def benchmark_endpoint(url="http://localhost:8000/health", total_requests=100, concurrency=10):
    print(f"[BENCHMARK] Testing {url} with {total_requests} requests (Concurrency: {concurrency})...")
    latencies = []

    def single_req():
        t0 = time.perf_counter()
        try:
            r = httpx.get(url, timeout=5.0)
            t1 = time.perf_counter()
            if r.status_code == 200:
                latencies.append((t1 - t0) * 1000)
        except Exception:
            pass

    t_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        for _ in range(total_requests):
            executor.submit(single_req)
    t_total = time.perf_counter() - t_start

    if latencies:
        latencies.sort()
        p50 = latencies[len(latencies) // 2]
        p95 = latencies[int(len(latencies) * 0.95)]
        p99 = latencies[int(len(latencies) * 0.99)]
        rps = len(latencies) / t_total
        print(f"[RESULTS] Completed {len(latencies)} successful requests in {t_total:.2f}s")
        print(f"  • Throughput: {rps:.1f} req/sec")
        print(f"  • P50 Latency: {p50:.2f} ms")
        print(f"  • P95 Latency: {p95:.2f} ms")
        print(f"  • P99 Latency: {p99:.2f} ms")
    else:
        print("[INFO] Server not reachable. Boot python main.py first.")

if __name__ == "__main__":
    benchmark_endpoint()

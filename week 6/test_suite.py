import time
import pytest
from job_queue import JobManager, JobPayload, JobStatus

def test_job_queue_enqueue_and_process():
    manager = JobManager()
    
    # Enqueue valid job
    payload = JobPayload(task_type="ai_synthesis", prompt="Test background synthesis", idempotency_key="test_idem_001")
    job, is_dup = manager.enqueue_job(payload)
    assert job is not None
    assert is_dup is False
    assert job.status in [JobStatus.PENDING, JobStatus.PROCESSING]

    # Test Idempotency (Same key -> Returns duplicate)
    dup_job, is_dup2 = manager.enqueue_job(payload)
    assert is_dup2 is True
    assert dup_job.job_id == job.job_id

    # Wait briefly for worker loop to pick up and process
    time.sleep(3.5)
    updated_job = manager.get_job(job.job_id)
    assert updated_job.status == JobStatus.COMPLETED
    assert updated_job.progress == 100
    assert updated_job.result is not None

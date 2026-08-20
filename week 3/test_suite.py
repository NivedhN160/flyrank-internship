import pytest
import os
from repository import SQLiteTaskRepository

def test_sqlite_repository_crud():
    db_path = "test_tasks.db"
    repo = SQLiteTaskRepository(db_path)
    repo.init_db()
    repo.reset()

    # Get all
    tasks = repo.get_all()
    assert len(tasks) == 3

    # Create
    new_t = repo.create("New Repository Task")
    assert new_t["title"] == "New Repository Task"
    assert new_t["done"] is False

    # Get by ID
    fetched = repo.get_by_id(new_t["id"])
    assert fetched is not None
    assert fetched["title"] == "New Repository Task"

    # Update
    updated = repo.update(new_t["id"], done=True)
    assert updated["done"] is True

    # Stats
    stats = repo.get_stats()
    assert stats["total"] == 4
    assert stats["done"] >= 1

    # Delete
    deleted = repo.delete(new_t["id"])
    assert deleted is True
    assert repo.get_by_id(new_t["id"]) is None

    # Cleanup
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass

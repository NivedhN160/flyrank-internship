import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI

DB_FILE = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    if count == 0:
        initial_tasks = [
            ("Setup development environment", True),
            ("Watch request-response lecture", True),
            ("Build CRUD API for Week 2", False)
        ]
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", initial_tasks)
        conn.commit()
    conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Task API (SQLite Database)", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello from Task API with SQLite"}

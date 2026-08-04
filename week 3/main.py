import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

DB_FILE = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
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
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_all_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    tasks = [{"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in rows]
    return tasks

@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing JSON body"}
        )
    
    if not isinstance(data, dict) or "title" not in data:
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )
    
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, 0)", (title.strip(),))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    new_task = {
        "id": new_id,
        "title": title.strip(),
        "done": False
    }
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=new_task
    )

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
        
    try:
        data = await request.json()
    except Exception:
        conn.close()
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing JSON body"}
        )
        
    if not isinstance(data, dict):
        conn.close()
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object"}
        )

    current_title = row["title"]
    current_done = bool(row["done"])

    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip():
            conn.close()
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )
        current_title = title.strip()
        
    if "done" in data:
        if not isinstance(data["done"], bool):
            conn.close()
            return JSONResponse(
                status_code=400,
                content={"error": "done field must be a boolean"}
            )
        current_done = data["done"]

    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (current_title, current_done, task_id))
    conn.commit()
    conn.close()

    return {"id": task_id, "title": current_title, "done": current_done}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
        
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

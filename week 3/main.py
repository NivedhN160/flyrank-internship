import sqlite3
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status, Query
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

app = FastAPI(
    title="Task API (SQLite Database)",
    description="A CRUD API for managing tasks backed by a persistent SQLite database.",
    version="2.0.0",
    lifespan=lifespan
)

@app.get(
    "/",
    summary="Root API Information",
    description="Returns metadata about the SQLite Task API and available endpoints."
)
def read_root():
    return {
        "name": "Task API (SQLite)",
        "version": "2.0",
        "endpoints": ["/tasks", "/health", "/stats", "/reset"]
    }

@app.get(
    "/health",
    summary="Health Check",
    description="Returns status ok if the server and database connection are active."
)
def health_check():
    return {"status": "ok"}

@app.get(
    "/stats",
    summary="Task Statistics via SQL",
    description="Computes total, completed, and open task counts using SQL COUNT() queries."
)
def get_task_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
    done_count = cursor.fetchone()[0]
    conn.close()
    open_count = total - done_count
    return {
        "total": total,
        "done": done_count,
        "open": open_count
    }

@app.post(
    "/reset",
    summary="Reset Task Database",
    description="Clears all task rows and re-seeds the initial 3 example tasks into SQLite."
)
def reset_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    initial_tasks = [
        ("Setup development environment", True),
        ("Watch request-response lecture", True),
        ("Build CRUD API for Week 2", False)
    ]
    cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", initial_tasks)
    conn.commit()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    tasks = [{"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in rows]
    return {"message": "Database reset to initial 3 seed tasks", "tasks": tasks}

@app.get(
    "/tasks",
    summary="List all tasks (with SQL filtering & search)",
    description="Retrieve tasks from SQLite. Supports query parameters for filtering by completion status (?done=true) and searching by title keyword (?search=milk) using SQL WHERE and LIKE clauses."
)
def get_all_tasks(
    done: Optional[bool] = Query(None, description="Filter tasks by completion status using SQL WHERE"),
    search: Optional[str] = Query(None, description="Search task titles using SQL LIKE clause")
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT id, title, done FROM tasks WHERE 1=1"
    params = []
    
    if done is not None:
        query += " AND done = ?"
        params.append(1 if done else 0)
        
    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search.strip()}%")
        
    query += " ORDER BY id ASC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    tasks = [{"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in rows]
    return tasks

@app.get(
    "/tasks/{task_id}",
    summary="Get a single task by ID",
    description="Retrieve a task row from SQLite by primary key ID. Returns 404 if not found."
)
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

@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task in SQLite",
    description="Insert a new row into the SQLite tasks table. Requires a non-empty title."
)
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

@app.put(
    "/tasks/{task_id}",
    summary="Update a task in SQLite",
    description="Update a task row in SQLite by ID. Modifies title and/or done status."
)
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

@app.delete(
    "/tasks/{task_id}",
    summary="Delete a task from SQLite",
    description="Delete a task row from SQLite by ID. Returns HTTP 204 No Content on success."
)
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

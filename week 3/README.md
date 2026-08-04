# W3 · A1 — Connecting your CRUD to the Database (Backend AI Engineering)

A persistent to-do list CRUD API built with Python 3.13, FastAPI, and a SQLite relational database (`tasks.db`). This project replaces the in-memory array from Week 2 with SQL persistence while keeping the exact same REST API interface.

---

## 💡 Why SQLite Was Chosen
* **Single File Storage:** The entire database lives in a single local file (`tasks.db`). No external database server installation or configuration is required.
* **Automatic Creation:** SQLite automatically initializes `tasks.db` and table schemas on first launch if missing.
* **Persistent Data:** Unlike in-memory data structures, data stored in SQLite survives server restarts and crashes.
* **Zero Configuration:** Perfect for embedded applications and rapid local development.

---

## 🚀 Quickstart: How to Run in Under 1 Minute

### Prerequisites
* Python 3.10+ installed.

### One-Command Setup & Launch
```bash
python -m venv venv && source venv/bin/activate || venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload --port 8000
```

Once running, visit:
* **Interactive API Docs (Swagger UI):** `http://localhost:8000/docs`
* **Root Endpoint:** `http://localhost:8000/`
* **Health Check:** `http://localhost:8000/health`

---

## 📋 Endpoints Summary & SQL Mapping

| HTTP Method | Path | Meaning / Description | SQL Query Executed | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Root API metadata | - | `200 OK` |
| `GET` | `/health` | Health check | - | `200 OK` |
| `GET` | `/stats` | Task statistics | `SELECT COUNT(*) FROM tasks;` | `200 OK` |
| `POST` | `/reset` | Reset database to 3 seed tasks | `DELETE FROM tasks;` + `INSERT` | `200 OK` |
| `GET` | `/tasks` | List tasks (with `?done=bool` & `?search=str`) | `SELECT * FROM tasks WHERE title LIKE ?;` | `200 OK` |
| `GET` | `/tasks/{id}` | Get task by ID | `SELECT * FROM tasks WHERE id = ?;` | `200 OK`, `404` |
| `POST` | `/tasks` | Create a new task | `INSERT INTO tasks (title, done) VALUES (?, 0);` | `201 Created`, `400` |
| `PUT` | `/tasks/{id}` | Update title and/or done status | `UPDATE tasks SET title = ?, done = ? WHERE id = ?;` | `200 OK`, `400`, `404` |
| `DELETE` | `/tasks/{id}` | Delete task by ID | `DELETE FROM tasks WHERE id = ?;` | `204 No Content`, `404` |

---

## 🛠️ Stage 4: Manual SQL Exploration

Below are authentic SQL queries executed manually against `tasks.db` during Stage 4 exploration:

### 1. List Every Task
```sql
SELECT * FROM tasks;
```
**Output:**
```text
(1, 'Setup development environment', 1)
(2, 'Watch request-response lecture', 1)
(3, 'Build CRUD API for Week 2', 0)
```

### 2. Show Completed Tasks Only
```sql
SELECT * FROM tasks WHERE done = 1;
```
**Output:**
```text
(1, 'Setup development environment', 1)
(2, 'Watch request-response lecture', 1)
```

### 3. Count Total Tasks
```sql
SELECT COUNT(*) FROM tasks;
```
**Output:**
```text
3
```

---

## 🧪 Proof That the API Didn't Change

All 13 test cases written in Week 2 pass against the Week 3 SQLite backend without altering a single assertion. 

### Why Identical Tests Passing Proves API Architecture:
APIs define **what** an application does (the external request-response contract), while databases define **where** data is stored. Because persistence is strictly an implementation detail hidden behind the API layer, swapping an in-memory list for SQLite leaves external clients completely unaffected.

---

## 🥊 Stage 6: The AI Rematch ("AI vs Me")

### The Prompt Used
> *"Migrate a Python FastAPI Task CRUD API from an in-memory list to a SQLite database (`tasks.db`). Create a table named `tasks` (`id INTEGER PRIMARY KEY AUTOINCREMENT`, `title TEXT NOT NULL`, `done BOOLEAN NOT NULL DEFAULT 0`). On startup, create the table if missing and seed 3 initial tasks only if the table is empty. Implement GET /tasks, GET /tasks/{id}, POST /tasks (201 Created), PUT /tasks/{id}, and DELETE /tasks/{id} (204 No Content) using parameterized SQL queries. Return 400 for empty titles and 404 for missing IDs as `{"error": "..."}`."*

### Analysis & Diff Answers

#### 1. What did the AI do better — and do you understand its version well enough to explain it?
* **Deprecated Startup Event:** The AI used the classic `@app.on_event("startup")` handler. While simpler to read, modern FastAPI recommends `@asynccontextmanager` lifespan handlers.

#### 2. What did it get wrong or quietly ignore from your prompt?
* **Error Response Format:** The AI used `raise HTTPException(status_code=404, detail="...")` which outputs `{"detail": "..."}` instead of the requested custom JSON schema `{"error": "..."}`.
* **Validation Status Code:** Empty titles triggered a 422 Unprocessable Entity error instead of the explicitly requested 400 Bad Request.

#### 3. What did your prompt forget to specify — and what did the AI silently decide for you?
* **Row Factory:** The prompt did not specify setting `conn.row_factory = sqlite3.Row`, so the AI returned tuple rows requiring manual dictionary mapping.

---

## 📌 Commit Log History

```text
* Stage 6: AI vs me
* Stage 5: database documentation
* Extras: SQL search, filter, and stats
* Stage 4: explored SQLite
* Stage 3: update and delete with SQL
* Stage 2: insert into database
* Stage 1: database read endpoints
* Stage 0: create SQLite database
```

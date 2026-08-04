from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI(title="Task API")

# In-memory database pre-filled with 3 example tasks
tasks_db = [
    {"id": 1, "title": "Setup development environment", "done": True},
    {"id": 2, "title": "Watch request-response lecture", "done": True},
    {"id": 3, "title": "Build CRUD API for Week 2", "done": False},
]

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
    return tasks_db

@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

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
    
    next_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = {
        "id": next_id,
        "title": title.strip(),
        "done": False
    }
    tasks_db.append(new_task)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=new_task
    )

from .db import create_db_and_tables, get_session
from .models import Task, CreateTask, TaskStatus, TaskPriority, TaskUpdate, TaskResponse
from fastapi import FastAPI, Depends, Query, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from sqlalchemy import or_
from typing import Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print('erorr running..')
    
app = FastAPI(lifespan=lifespan)


@app.get('/', status_code=status.HTTP_200_OK)
def root():
    return {
        "info": "Task Management API",
        "available_endpoints": {
            "Health Check": {"path": "/health", "method": "GET", "description": "API health status"},
            "Create Task": {"path": "/tasks", "method": "POST", "description": "Create a new task"},
            "List Tasks": {"path": "/tasks", "method": "GET", "description": "List all tasks with filtering, pagination, and text search"},
            "Get Task": {"path": "/tasks/{task_id}", "method": "GET", "description": "Retrieve a specific task"},
            "Update Task": {"path": "/tasks/{task_id}", "method": "PUT", "description": "Update an existing task"},
            "Delete Task": {"path": "/tasks/{task_id}", "method": "DELETE", "description": "Delete a task"},
            "Filter by Status": {"path": "/tasks/status/{status}", "method": "GET", "description": "Get tasks by status"},
            "Filter by Priority": {"path": "/tasks/priority/{priority}", "method": "GET", "description": "Get tasks by priority"},
        }
    }
    
@app.get("/health", status_code=status.HTTP_200_OK)
def api_health(session: Session = Depends(get_session)):
    try:
        # Just try to execute a simple query
        session.exec(select(Task).limit(1)).all()
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "fail", "db": "error", "details": str(e)}

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: CreateTask, session: Session = Depends(get_session)):
        # existing_task = session.exec(select(Task).where(Task.title == task.title)).first()
        # if existing_task:
        #     raise HTTPException(
        #     status_code=400,
        #     detail="This Task is already exists."
        # )
        task = Task(
          title=task.title,
          description=task.description,
          status=task.status,
          priority=task.priority, 
          assigned_to=task.assigned_to,
          due_date = task.due_date
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.get("/tasks", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def get_tasks(
    session: Session = Depends(get_session),
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = Query(None)
    ):
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if search:
        query = query.where(
        or_(
            Task.title.ilike(f"%{search}%"),
            Task.description.ilike(f"%{search}%")
        )
    )
    tasks = session.exec(query.limit(limit).offset(skip)).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.exec(select(Task).where(Task.id==task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not Found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int,
    task: TaskUpdate,
    session: Session = Depends(get_session),
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
    
@app.delete("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task Not found")
    session.delete(task)
    session.commit()
    return task

@app.get("/tasks/status/{status}", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def get_task_by_status(status: str, session: Session = Depends(get_session)):
    task = session.exec(select(Task).where(Task.status==status)).all()
    return task

@app.get("/tasks/priority/{priority}", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def get_task_by_priority(priority: str, session: Session = Depends(get_session)):
    task = session.exec(select(Task).where(Task.priority == priority)).all()
    return task

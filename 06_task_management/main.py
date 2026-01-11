from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Literal
from sqlmodel import create_engine, Session , select, SQLModel, Field
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

class Tasks(SQLModel, table=True):
    id : int | None = Field(default=None , primary_key=True)
    title : str
    created_at : str | None = None
    completed : bool = False

database_url = os.getenv("DATABASE_URL")

# connection_string = str(database_url).replace("postgresql" , "postgresql+psycopg")

engine = create_engine(database_url , echo=True)

def create_tables():
    print("Creating tables in the database......")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully.")

async def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status" : "healthy"}



@app.post("/tasks", response_model=Tasks)
async def create_task(task: Tasks , session : Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task



@app.get("/tasks" , response_model=List[Tasks])
async def get_all_tasks(session : Session = Depends(get_session)):
    tasks = session.exec(select(Tasks)).all()
    if not tasks:
        raise HTTPException(status_code=404 , detail="No tasks found")
    return tasks


@app.get("/tasks/{task_id}" , response_model=Tasks)
async def get_single_task(task_id: int , session: Session = Depends(get_session)):
    task = session.get(Tasks, task_id)
    if not task:
        raise HTTPException(status_code=404 , detail="Task not found")
    return task

@app.put("/tasks/{task_id}" , response_model=Tasks)
async def update_task(task_id: int , task: Tasks , session: Session = Depends(get_session)):
    existing_task = session.get(Tasks , task_id)
    if not existing_task:
        raise HTTPException(status_code=404 , detail="Task not found")
    existing_task.title = task.title
    existing_task.completed = task.completed
    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    return existing_task

@app.put("/tasks/{task_id}/complete" , response_model=Tasks)
async def mark_task_complete(task_id: int , completed: Literal[True, False], session: Session = Depends(get_session)):
    task = session.get(Tasks, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}" , response_model=dict)
async def delete_task(task_id: int , session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404 , detail="Task not found")
    session.delete(task)
    session.commit()
    return {"detail" : "Task deleted successfully."}
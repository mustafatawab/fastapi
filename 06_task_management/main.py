from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Literal
from sqlmodel import create_engine, Session , select, SQLModel, Field
from dotenv import load_dotenv, find_dotenv
import os
from contextlib import asynccontextmanager 
from datetime import datetime, date



load_dotenv()



# -----------------



class Tasks(SQLModel, table=True):
    id : int | None = Field(default=None , primary_key=True)
    title : str
    created_at : str | None = None
    completed : bool = False

class TaskCreate(BaseModel):
    title : str

class TaskUpdate(BaseModel):
    title : Optional[str] = None
    completed : Optional[bool] = None

class TaskReponse(BaseModel):
    id : int
    title : str
    created_at : str | None = None
    completed : bool


# -----------
database_url = os.getenv("DATABASE_URL")

# connection_string = str(database_url).replace("postgresql" , "postgresql+psycopg")

engine = create_engine(database_url , echo=True)
# --------
def create_tables():
    print("Creating tables in the database......")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully.")

# -----------

async def get_session():
    with Session(engine) as session:
        yield session

# -----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
# -----------

app = FastAPI(lifespan=lifespan, title="Task Management API", version="1.0.0")
# ------------------------------------------


@app.get("/")
async def health_check():
    return {"status" : "healthy"}





@app.post("/tasks", response_model=TaskReponse)
async def create_task(task: TaskCreate , session : Session = Depends(get_session)) -> TaskReponse:
    created_at = date.today()
    new_task = Tasks(title=task.title, created_at=str(created_at) , completed=False)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task





@app.get("/tasks" , response_model=List[TaskReponse])
async def get_all_tasks(session : Session = Depends(get_session)) -> List[TaskReponse]:
    tasks = session.exec(select(Tasks)).all()
    return tasks





@app.get("/tasks/{task_id}" , response_model=TaskReponse)
async def get_single_task(task_id: int , session: Session = Depends(get_session)) -> TaskReponse:
    task = session.get(Tasks, task_id)
    if not task:
        raise HTTPException(status_code=404 , detail="Task not found")
    return task




@app.put("/tasks/{task_id}" , response_model=TaskReponse    )
async def update_task(task_id: int , task: TaskUpdate , session: Session = Depends(get_session)) -> TaskReponse:
    existing_task = session.get(Tasks , task_id)
    if not existing_task:
        raise HTTPException(status_code=404 , detail="Task not found")
    existing_task.title = task.title
    existing_task.completed = task.completed
    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    return existing_task



@app.patch("/tasks/{task_id}/complete" , response_model=TaskReponse)
async def mark_task_complete(task_id: int , session: Session = Depends(get_session)) -> TaskReponse:
    task = session.get(Tasks, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.completed:
        raise HTTPException(status_code=400, detail="Task is already completed")
    task.completed = True
    session.add(task)
    session.commit()
    session.refresh(task)
    return task



@app.patch("/tasks/{task_id}/incomplete" , response_model=TaskReponse)
async def mark_task_incomplete(task_id: int, session: Session = Depends(get_session)) -> TaskReponse:
    task = session.get(Tasks, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not task.completed:
        raise HTTPException(status_code=402, detail="Task is already completed as False")
    task.completed = False
    session.add(task)
    session.commit()
    session.refresh(task)
    return task




@app.delete("/tasks/{task_id}" , response_model=dict[str, str])
async def delete_task(task_id: int , session: Session = Depends(get_session)) -> dict[str, str]:
    task = session.get(Tasks, task_id)
    if not task:
        raise HTTPException(status_code=404 , detail="Task not found")
    session.delete(task)
    session.commit()
    return {"detail" : "Task deleted successfully."}
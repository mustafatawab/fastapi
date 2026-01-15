from sqlmodel import SQLModel, Field, Session, select
from datetime import  date
from database import get_session
from core.dependency import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from routers.auth import User
from models.tasks import Tasks, TaskReponse, TaskCreate, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)




# class Tasks(SQLModel, table=True):
#     id : int | None = Field(default=None , primary_key=True)
#     title : str = Field(min_length=1 , max_length=200)
#     created_at : datetime = Field(default=datetime.utcnow())
#     completed : bool = Field(default=False)
#     userId: int | None = Field(default=None, foreign_key="user.id")



# class TaskCreate(BaseModel):
#     title : str

# class TaskUpdate(BaseModel):
#     title : Optional[str] = None
#     completed : Optional[bool] = None

# class TaskReponse(BaseModel):
#     id : int
#     title : str
#     created_at : str | None = None
#     completed : bool





@router.post("/", response_model=TaskReponse)
async def create_task(task: TaskCreate ,current_user: User = Depends(get_current_user), session : Session = Depends(get_session)) -> TaskReponse:
    created_at = date.today()
    new_task = Tasks(title=task.title, created_at=str(created_at) , completed=False, userId=current_user.id)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task




@router.get("/", response_model=list[TaskReponse])
async def get_all_tasks(current_user: User = Depends(get_current_user),session : Session = Depends(get_session)) -> list[TaskReponse]:
    tasks = session.exec(select(Tasks).where(Tasks.userId == current_user.id)).all()
    return tasks





@router.get("/{task_id}" , response_model=TaskReponse)
async def get_single_task(task_id: int ,current_user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> TaskReponse:
    task = session.exec(select(Tasks).where(Tasks.userId == current_user and Tasks.id == task_id))
    if not task:
        raise HTTPException(status_code=404 , detail="Task not found")
    return task




@router.put("/{task_id}" , response_model=TaskReponse    )
async def update_task(task_id: int , task: TaskUpdate ,current_user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> TaskReponse:
    existing_task = session.exec(select(Tasks).where(Tasks.userId == current_user and Tasks.id == task_id))
    if not existing_task:
        raise HTTPException(status_code=404 , detail="Task not found")
    existing_task.title = task.title
    existing_task.completed = task.completed
    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    return existing_task



@router.patch("/{task_id}/complete" , response_model=TaskReponse)
async def mark_task_complete(task_id: int ,current_user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> TaskReponse:
    task = session.exec(select(Tasks).where(Tasks.userId == current_user and Tasks.id == task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.completed:
        raise HTTPException(status_code=400, detail="Task is already completed")
    task.completed = True
    session.add(task)
    session.commit()
    session.refresh(task)
    return task



@router.patch("/{task_id}/incomplete" , response_model=TaskReponse)
async def mark_task_incomplete(task_id: int,current_user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> TaskReponse:
    task = session.exec(select(Tasks).where(Tasks.userId == current_user and Tasks.id == task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not task.completed:
        raise HTTPException(status_code=402, detail="Task is already completed as False")
    task.completed = False
    session.add(task)
    session.commit()
    session.refresh(task)
    return task




@router.delete("/{task_id}" , response_model=dict[str, str])
async def delete_task(task_id: int ,current_user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> dict[str, str]:
    task = session.exec(select(Tasks).where(Tasks.userId == current_user and Tasks.id == task_id))
    if not task:
        raise HTTPException(status_code=404 , detail="Task not found")
    session.delete(task)
    session.commit()
    return {"detail" : "Task deleted successfully."}

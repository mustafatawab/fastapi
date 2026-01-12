from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool = False

class TodoCreateRequest(BaseModel):
    title: str
    description: str = None

class TodoUpdateRequest(BaseModel):
    title: str = None
    description: str = None


todos : list[TodoResponse] = []



@app.get("/todos" , response_model=list[TodoResponse])
def get_todos() -> list[TodoResponse]:
    return todos

@app.post("/todos" , response_model=TodoResponse)
def create_todo(todo: TodoCreateRequest) -> TodoResponse:
    new_todo = TodoResponse(
        id=len(todos),
        title=todo.title,
        description=todo.description,
        completed=False
    )

    todos.append(new_todo)
    return new_todo

@app.get("/todos/{todo_id}" , response_model=TodoResponse)
def get_todo(todo_id: int) -> TodoResponse:
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")



@app.put("/todos/{todo_id}" , response_model=TodoResponse)
def update_todo(todo_id: int, update_todo: TodoUpdateRequest) -> TodoResponse:
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = TodoResponse(
                id=todo.id , 
                title=update_todo.title, 
                description=update_todo.description , 
                completed=todo.completed
            )
            print("Updated todos are " , todos)
            return todos[index]
    raise HTTPException(status_code=404, detail="Todo not found")



@app.delete("/todos/{todo_id}" , response_model=dict)
def delete_todo(todo_id: int) -> dict:
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"detail": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")




@app.patch('/todos/{todo_id}/complete', response_model=TodoResponse)
def mark_as_completed(todo_id: int) -> TodoResponse:
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            if todos[index].completed:
                raise HTTPException(status_code=400, detail="Todo is already completed")
            todos[index].completed = True
            return todos[index]
    raise HTTPException(status_code=404, detail="Todo not found")



@app.patch('/todos/{todo_id}/incomplete', response_model=TodoResponse)
def mark_as_incomplete(todo_id: int) -> TodoResponse:
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            if not todos[index].completed:
                raise HTTPException(status_code=400, detail="Todo is already incomplete")
            todos[index].completed = False
            return todos[index]
    raise HTTPException(status_code=404, detail="Todo not found")




@app.get("/" , response_model=dict)
def read_root() -> dict:
    return {"message": "Welcome to the Todo API!"}
from typing import List
from enum import Enum

class TodoStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"

class Todo:
    def __init__(self, title: str, description: str, status: TodoStatus = TodoStatus.PENDING):
        self.title = title
        self.description = description
        self.status = status
    
    def __repr__(self):
        return f"Todo(title='{self.title}', description='{self.description}', status='{self.status.value}')"

# Create a list of todos
todos: List[Todo] = [
    Todo("Buy groceries", "Milk, eggs, bread", TodoStatus.PENDING),
    Todo("Complete project", "Finish the FastAPI CRUD app", TodoStatus.IN_PROGRESS),
    Todo("Review code", "Review pull requests", TodoStatus.COMPLETED)
]

# Print todos
for index, todo in enumerate(todos):
    print(f"Todo {index + 1}: {todo}")
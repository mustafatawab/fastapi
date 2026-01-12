from fastapi.testclient import TestClient
from .todo import app

client = TestClient(app)

def test_get_todo():
    response = client.get("/todos")
    assert response.status_code == 200
    
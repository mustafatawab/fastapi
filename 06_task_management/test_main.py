from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from .main import app, engine

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
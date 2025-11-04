from fastapi.testclient import TestClient
from main import app

client = TestClient(app=app)

def test_home():
    response = client.get("/")
    assert response.json() == {"message":"Hello World"}
    assert response.status_code == 200
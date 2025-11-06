from fastapi.testclient import TestClient
from main import app

def test_get_item():
    client = TestClient(app=app)

    response = client.get(f"/items/5")
    assert response.status_code == 200
    assert response.json() == {"item_id" : 5}


def test_limited_items():
    client = TestClient(app=app)
    res = client.get("/items?limit=10")
    assert res.status_code == 200
    assert res.json() == {"limit" : 10}

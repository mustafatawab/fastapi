from fastapi.testclient import TestClient
from main import app
import pytest

@pytest.fixture
def client():
    # yield TestClient(app)
    return TestClient(app)

def test_get_item(client):

    response = client.get(f"/items/5")
    assert response.status_code == 200
    assert response.json() == {"item_id" : 5}


def test_item_not_found(client):

    response = client.get(f"/items/101")
    assert response.status_code == 404
    assert response.json() == {"detail" : "Item not found"}

def test_limited_items(client):
    res = client.get("/items?limit=10")
    assert res.status_code == 200
    assert res.json() == {"limit" : 10}


def test_create_item(client):
    res = client.post("/items" , json={"name" : "watch" , "price" : 4300})
    assert res.status_code == 200
    assert res.json() == {"name" : "watch" , "price" : 4300}


def test_create_item_invalid_price(client):
    res = client.post("/items", json={"name": "watch", "price": "oops"})
    assert res.status_code == 422
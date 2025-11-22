from fastapi.testclient import TestClient
import pytest
from main import app
from shemas import CarCreate, CarUpdate, CarRead

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def new_car(client: TestClient):
    response = client.post("/cars/", json={"name" : "Toyota" ,"brand" : "something", "model" : "Corolla" , "year": 2020})
    return response.json()




def test_create_car(client: TestClient):
    response = client.post("/cars/", json={"name" : "Toyota" ,"brand" : "something", "model" : "Corolla" , "year": 2020})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Toyota"
    assert data["brand"] == "something"


def test_read_cars(client: TestClient, new_car):
    
    
    res = client.get("/cars")
    data = res.json()

    assert res.status_code == 200
    assert len(data) > 0
    assert data[0]["name"] == "Toyota"


def test_update_car(client: TestClient, new_car):

    response = client.put(f"/cars/1" , json={"name" : "Honda" ,"brand" : "another", "model" : "Civic" , "year": 2021})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Honda"

def test_delete_car(client: TestClient, new_car):
    response = client.delete(f"/cars/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Car deleted successfully"}
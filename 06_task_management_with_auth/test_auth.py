from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session
from main import app, engine
from models.users import UserCreate
import pytest
from database import get_session


@pytest.fixture(scope="module", autouse=True)
def get_db_session():
    SQLModel.metadata.create_all(engine)
    yield Session(engine)

@pytest.fixture(scope='function')
def test_app(get_db_session):
    def test_session():
        yield get_db_session
    app.dependency_overrides[get_session] = test_session
    with TestClient(app=app) as client:
        yield client




def test_register(test_app):
    add_user = {"name":"TestClient" , "username":"testclient" , "email":'testclient@gmail.com' , "password":"testclient"}

    response = test_app.post("/auth/register" , json=add_user)
    assert response.status_code == 200
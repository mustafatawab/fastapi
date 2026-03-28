from sqlmodel import Session, SQLModel
from db.engine import engine


def get_session():
    with Session(engine) as session:
        yield session



def create_db_tables():
    SQLModel.metadata.create_all(engine)
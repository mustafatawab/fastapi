from sqlmodel import Session , SQLModel
from db.engine import engine


def get_session():
    with Session(engine) as s:
        yield s
    
def create_tables():
    SQLModel.metadata.create_all(engine)


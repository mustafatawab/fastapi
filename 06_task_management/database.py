from sqlmodel import SQLModel, create_engine, Session
from config import get_settings , Settings
from contextlib import asynccontextmanager

settings = get_settings()
engine = create_engine(settings.database_url , echo=True)


async def create_tables():
    """ Create all tables in the database"""
    SQLModel.metadata.create_all(engine)




def get_session():
    """ Dependency that provides a database session """
    with Session(engine) as session:
        yield session
from sqlmodel import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

connection_string = str(DATABASE_URL).replace("postgresql" , "postgresql+psycopg")

engine = create_engine(connection_string, echo=True)
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
import os

sqlite_file_name = "mydatabase.db"
sqlite_url = f"sqlite:///db/{sqlite_file_name}"
engine = create_engine(sqlite_url, echo = True)

def create_db_and_tables():
    directory_path = Path(__file__).parent / Path("db")
    directory_created = directory_path.exists()
    if not directory_created:
        os.mkdir(directory_path)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("Closing the program...")

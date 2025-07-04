from sqlmodel import SQLModel, create_engine, Session
from fastapi import FastAPI

connect_args = {"check_same_thread": False}
engine = create_engine('sqlite:///file.db', connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


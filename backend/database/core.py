from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from fastapi import Depends
from typing import Annotated

DATABASE_URL = "sqlite+pysqlite:///database.db" 
#DATABASE_URL = "sqlite+pysqlite:///:memory:" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

DbSession = Annotated[Session, Depends(get_db)]
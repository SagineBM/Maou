from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

def get_engine(path="database.db"):
    database_url = f"sqlite:///{path}"
    return create_engine(database_url, echo=True)

def init_db(engine):
    Base.metadata.create_all(engine)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

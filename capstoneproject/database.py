# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL


def get_engine(database_url=DATABASE_URL):
    return create_engine(database_url, echo=True)


# Create the engine
engine = get_engine()

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Base class for declarative class definitions
Base = declarative_base()

# Create a session instance


def get_session():
    return Session()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DATABASE_URL

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Base class for declarative class definitions
Base = declarative_base()


# Create a session instance
def get_session():
    return Session()

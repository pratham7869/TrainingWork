from models import Base
from database import engine

# Create tables
Base.metadata.create_all(engine)
# when we execute this file we can make the tables present in the models.py.

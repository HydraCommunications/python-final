import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the base directory and database path
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'database', 'supply_tracker.db')
os.makedirs(os.path.dirname(database_path), exist_ok=True)

# Initialize the database engine
engine = create_engine(f'sqlite:///{database_path}', echo=True)

# Define the declarative base class
Base = declarative_base()

# Set up the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

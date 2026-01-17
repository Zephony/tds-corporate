import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends
from typing import Generator

# Create declarative base for SQLAlchemy v2
Base = declarative_base()

# Database configuration
DATABASE_URL = os.getenv('POSTGRES_URL', 'postgresql://admin:password@localhost:5679/admin')

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    pool_recycle=60,
    pool_pre_ping=True
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for database session"""

    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

def commit_db_session(db_session: Session = Depends(get_db)):
    """Commit the database session"""
    try:
        yield db_session
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

# For backward compatibility with existing models
# This will be replaced by Base in the models
db = None


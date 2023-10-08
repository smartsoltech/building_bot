from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from .worker import Worker
from .brigade import Brigade
from .profile import Profile
from .object import Object

__all__ = ['Worker', 'Brigade', 'Profile', 'Object']
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
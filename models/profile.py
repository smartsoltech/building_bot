from sqlalchemy import Column, Integer, String
from . import Base

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)

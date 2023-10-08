from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base

class Worker(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brigade_id = Column(Integer, ForeignKey('brigades.id'))

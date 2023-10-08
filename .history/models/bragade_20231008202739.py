from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Brigade(Base):
    __tablename__ = 'brigades'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    object_id = Column(Integer, ForeignKey('objects.id'))

    workers = relationship("Worker", backref="brigade")
    profile = relationship("Profile", backref="brigades")
    object = relationship("Object", backref="brigades")

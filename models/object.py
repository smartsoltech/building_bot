from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Object(Base):
    __tablename__ = 'objects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    required_profiles = Column(String)  # Можно использовать JSON или другой формат для хранения

    brigades = relationship("Brigade", backref="object")

from sqlalchemy import Boolean, Column, Date, Integer, String, ForeignKey
from . import Base

class Worker(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    chat_id = Column(Integer, index=True)
    full_name = Column(String, index=True)
    birth_date = Column(Date)
    citizenship = Column(String)
    visa = Column(Boolean)
    visa_type = Column(String, nullable=True)
    certificate = Column(Boolean)
    phone = Column(String)
    address = Column(String)
    id_card_photo_front = Column(String)
    id_card_photo_back = Column(String)
    certificate_photo = Column(String)
    brigade_id = Column(Integer, ForeignKey('brigades.id'))

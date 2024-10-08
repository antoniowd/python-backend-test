"""Model file"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, autoincrement='auto', primary_key=True, index=True)
    img = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String)
    available = Column(Boolean, default=True)

class Friends(Base):
    __tablename__ = 'friends'

    id = Column(Integer, autoincrement='auto', primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    friend_id = Column(Integer, ForeignKey('profiles.id'))

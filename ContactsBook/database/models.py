from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, default="passw", nullable=False)
    username = Column(String, nullable=True)
    roles = Column(String, default="user", nullable=False)
    refresh  = Column(String, default="refr", nullable=False)
    avatar = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.now()) 
    verified = Column(Boolean, default=False, nullable=False)


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(50), nullable=True)
    phone = Column(String(13), nullable=True)
    birthday = Column(Date, nullable=True)
    inform = Column(String, nullable=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None) 
    user = relationship('User', backref="contacts")

    def __repr__(self) -> str:
        return f"Contact(id={self.id!r}, name={self.first_name!r}, last_name={self.last_name!r})"

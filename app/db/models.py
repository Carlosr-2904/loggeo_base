# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="estudiante")
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    major = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    rating = Column(Float, default=0.0, nullable=True)

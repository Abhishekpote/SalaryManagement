from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from appSettings import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    country = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    mobile_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    date_of_birth = Column(DateTime(timezone=True), nullable=False)
    date_of_joining = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
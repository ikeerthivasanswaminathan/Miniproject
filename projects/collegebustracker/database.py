import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./college_bus_tracker.db')

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    login_id = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    register_number = Column(String, unique=True, nullable=False)
    age = Column(Integer)
    blood_group = Column(String)
    bus_route = Column(String)
    area = Column(String)
    bus_stop = Column(String)
    buspass_status = Column(String)
    photo_uploaded = Column(Boolean, default=False)
    photo_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Bus(Base):
    __tablename__ = 'buses'
    
    id = Column(Integer, primary_key=True, index=True)
    driver_name = Column(String, nullable=False)
    driver_phone = Column(String, nullable=False)
    bus_name = Column(String, nullable=False)
    bus_via = Column(String)
    bus_number = Column(String, unique=True, nullable=False)
    bus_route_number = Column(String, nullable=False)
    current_latitude = Column(Float, default=13.0827)
    current_longitude = Column(Float, default=80.2707)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True, index=True)
    register_number = Column(String, nullable=False)
    student_name = Column(String, nullable=False)
    query = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='Pending')

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True, index=True)
    student_login_id = Column(String, nullable=False)
    bus_number = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def close_db(db):
    db.close()

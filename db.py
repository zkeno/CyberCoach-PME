"""SQLite DB models and helpers using SQLAlchemy"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DB_URL = os.getenv("CYBERCOACH_DB_URL", "sqlite:///./cybercoach.db")

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class QuizResult(Base):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_key = Column(String, index=True)
    score = Column(Float)
    correct = Column(Integer)
    total = Column(Integer)
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class PhishingCampaign(Base):
    __tablename__ = "phishing_campaigns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class PhishingEvent(Base):
    __tablename__ = "phishing_events"
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("phishing_campaigns.id"))
    email = Column(String, index=True)
    clicked = Column(Boolean, default=False)
    data = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("PhishingCampaign")


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

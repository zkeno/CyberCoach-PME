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


# ----- Simple SQLite helpers (for quick persistence & reporting) -----
import sqlite3
import json
import pandas as pd

# Default sqlite file (can be overridden via env var CYBERCOACH_DB_SQLITE)
DB_FILE = os.getenv("CYBERCOACH_DB_SQLITE", "./cybercoach.db")


def init_sqlite_db(db_path: str | None = None):
    """Initialise la base SQLite et crée les tables nécessaires."""
    path = db_path or DB_FILE
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    # Table: quizzes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS quizzes (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            theme TEXT
        )
        """
    )

    # Table: questions
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id TEXT,
            question_text TEXT NOT NULL,
            options TEXT,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        )
        """
    )

    # Table: user_results
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            department TEXT,
            quiz_id TEXT,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            completion_rate REAL,
            attempt_date TEXT NOT NULL,
            responses_json TEXT,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        )
        """
    )

    conn.commit()
    conn.close()
    return True


def save_quiz_result(user_id: str, department: str, quiz_id: str, score: int, total_questions: int, responses: dict, db_path: str | None = None):
    """Enregistre le résultat d'un quiz pour un utilisateur dans SQLite."""
    path = db_path or DB_FILE
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    completion_rate = (score / total_questions) * 100 if total_questions > 0 else 0
    attempt_date = datetime.now().isoformat()
    responses_json = json.dumps(responses)

    cursor.execute(
        """
        INSERT INTO user_results (user_id, department, quiz_id, score, total_questions, completion_rate, attempt_date, responses_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, department, quiz_id, score, total_questions, completion_rate, attempt_date, responses_json),
    )

    conn.commit()
    conn.close()
    return True


def get_aggregated_results(db_path: str | None = None) -> pd.DataFrame:
    """Récupère tous les résultats (DataFrame) pour le reporting."""
    path = db_path or DB_FILE
    conn = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM user_results", conn)
    conn.close()
    return df


def export_results_to_csv(filename: str = "rapport_cybercoach.csv", db_path: str | None = None):
    """Exporte le rapport agrégé au format CSV."""
    df = get_aggregated_results(db_path)
    if df.empty:
        return False
    df.to_csv(filename, index=False, encoding="utf-8")
    return True


def seed_quizzes_from_config(config_quizzes: dict | None = None, db_path: str | None = None):
    """Insère les quiz et questions depuis le `config.QUIZZES` fourni."""
    from config import QUIZZES

    quizzes = config_quizzes or QUIZZES
    path = db_path or DB_FILE
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    for quiz_key, info in quizzes.items():
        # Insert quiz
        cursor.execute(
            "INSERT OR IGNORE INTO quizzes (id, title, theme) VALUES (?, ?, ?)",
            (quiz_key, info.get("title", quiz_key), info.get("description", "")),
        )

        # Insert questions
        for q in info.get("questions", []):
            options_json = json.dumps(q.get("options", []), ensure_ascii=False)
            correct = q.get("correct")
            cursor.execute(
                "INSERT INTO questions (quiz_id, question_text, options, correct_answer) VALUES (?, ?, ?, ?)",
                (quiz_key, q.get("question"), options_json, str(correct)),
            )

    conn.commit()
    conn.close()
    return True


# Créer les tables SQLite à l'import (sûr même si SQLAlchemy est utilisé)
try:
    init_sqlite_db()
except Exception:
    # Si l'environnement ne permet pas l'accès au FS, ignorer silencieusement
    pass

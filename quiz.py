"""Module Quiz & Tracking pour CyberCoach"""
import streamlit as st
import pandas as pd
from datetime import datetime
import json
from config import QUIZZES, DEPARTMENTS


class QuizManager:
    """Gère les quiz et le tracking des utilisateurs"""

    def __init__(self):
        self.initialize_session()

    def initialize_session(self):
        """Initialise la session pour le tracking"""
        if "user_data" not in st.session_state:
            st.session_state.user_data = {
                "name": "",
                "department": "",
                "email": "",
                "quiz_scores": {},
                "quiz_completion_dates": {},
            }

        if "current_quiz" not in st.session_state:
            st.session_state.current_quiz = None

        if "quiz_in_progress" not in st.session_state:
            st.session_state.quiz_in_progress = False

        if "quiz_answers" not in st.session_state:
            st.session_state.quiz_answers = {}

    def start_user_session(self, name: str, department: str, email: str):
        """Démarre une session utilisateur"""
        st.session_state.user_data["name"] = name
        st.session_state.user_data["department"] = department
        st.session_state.user_data["email"] = email

    def start_quiz(self, quiz_key: str):
        """Démarre un quiz"""
        st.session_state.current_quiz = quiz_key
        st.session_state.quiz_in_progress = True
        st.session_state.quiz_answers = {}

    def submit_quiz_answer(self, question_id: int, answer_index: int):
        """Enregistre une réponse au quiz"""
        st.session_state.quiz_answers[question_id] = answer_index

    def calculate_score(self, quiz_key: str) -> dict:
        """Calcule le score du quiz"""
        quiz = QUIZZES[quiz_key]
        questions = quiz["questions"]

        correct = 0
        for question in questions:
            q_id = question["id"]
            if st.session_state.quiz_answers.get(q_id) == question["correct"]:
                correct += 1

        score = (correct / len(questions)) * 100
        return {
            "score": score,
            "correct": correct,
            "total": len(questions),
            "percentage": f"{score:.1f}%",
        }

    def finish_quiz(self, quiz_key: str):
        """Finalise un quiz et enregistre les résultats (stocke aussi en DB si disponible)"""
        score_info = self.calculate_score(quiz_key)
        st.session_state.user_data["quiz_scores"][quiz_key] = score_info["score"]
        st.session_state.user_data["quiz_completion_dates"][quiz_key] = datetime.now().isoformat()
        st.session_state.quiz_in_progress = False
        st.session_state.current_quiz = None

        # Persister dans SQLite si la DB est disponible
        try:
            from db import SessionLocal, User, QuizResult, init_db

            init_db()
            db = SessionLocal()
            # Créer ou récupérer l'utilisateur
            user = db.query(User).filter(User.email == st.session_state.user_data.get("email")).first()
            if not user:
                user = User(
                    name=st.session_state.user_data.get("name"),
                    email=st.session_state.user_data.get("email"),
                    department=st.session_state.user_data.get("department"),
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            qr = QuizResult(
                user_id=user.id,
                quiz_key=quiz_key,
                score=score_info["score"],
                correct=score_info["correct"],
                total=score_info["total"],
            )
            db.add(qr)
            db.commit()
        except Exception:
            # DB non disponible — ignorer silencieusement
            pass

        return score_info

    def get_user_stats(self) -> dict:
        """Retourne les statistiques de l'utilisateur"""
        scores = st.session_state.user_data.get("quiz_scores", {})
        if not scores:
            return {"average": 0, "completed": 0, "progress": 0}

        completed = len(scores)
        average = sum(scores.values()) / len(scores) if scores else 0
        progress = (completed / len(QUIZZES)) * 100

        return {
            "average": f"{average:.1f}%",
            "completed": completed,
            "total": len(QUIZZES),
            "progress": f"{progress:.1f}%",
        }


def render_quiz_page():
    """Rendu de la page Quiz & Tracking"""
    st.header("📚 Quiz & Formation (Offre STANDARD)")

    quiz_manager = QuizManager()

    # Vérifier si l'utilisateur est identifié
    if not st.session_state.user_data.get("name"):
        st.subheader("👤 Identification Utilisateur")
        col1, col2, col3 = st.columns(3)

        with col1:
            name = st.text_input("Nom Complet", key="user_name")
        with col2:
            department = st.selectbox("Département", DEPARTMENTS, key="user_dept")
        with col3:
            email = st.text_input("Email Professionnel", key="user_email")

        if st.button("Démarrer la Formation"):
            if name and email:
                quiz_manager.start_user_session(name, department, email)
                st.success(f"✅ Bienvenue {name}!")
                st.rerun()
            else:
                st.error("❌ Veuillez remplir tous les champs")
        return

    # Afficher le profil utilisateur
    st.subheader(f"👋 Bienvenue {st.session_state.user_data['name']}")
    col1, col2, col3, col4 = st.columns(4)
    stats = quiz_manager.get_user_stats()
    with col1:
        st.metric("Quiz complétés", f"{stats['completed']}/{stats['total']}")
    with col2:
        st.metric("Score moyen", stats["average"])
    with col3:
        st.metric("Progression", stats["progress"])
    with col4:
        if st.button("Réinitialiser Profil"):
            st.session_state.user_data = {
                "name": "",
                "department": "",
                "email": "",
                "quiz_scores": {},
                "quiz_completion_dates": {},
            }
            st.rerun()

    st.divider()

    # Si un quiz est en cours
    if st.session_state.quiz_in_progress and st.session_state.current_quiz:
        render_quiz_interface(quiz_manager)
    else:
        # Afficher la liste des quiz
        st.subheader("📖 Quiz Disponibles")
        cols = st.columns(2)

        for idx, (quiz_key, quiz_info) in enumerate(QUIZZES.items()):
            with cols[idx % 2]:
                is_completed = quiz_key in st.session_state.user_data["quiz_scores"]
                status_icon = "✅" if is_completed else "⏳"

                st.info(
                    f"**{status_icon} {quiz_info['title']}**\n\n"
                    f"{quiz_info['description']}\n\n"
                    f"Questions: {len(quiz_info['questions'])}"
                )

                if is_completed:
                    score = st.session_state.user_data["quiz_scores"][quiz_key]
                    st.success(f"Score: {score:.1f}%")
                    if st.button(f"Reprendre {quiz_key}", key=f"retry_{quiz_key}"):
                        quiz_manager.start_quiz(quiz_key)
                        st.rerun()
                else:
                    if st.button(f"Démarrer {quiz_key}", key=f"start_{quiz_key}"):
                        quiz_manager.start_quiz(quiz_key)
                        st.rerun()


def render_quiz_interface(quiz_manager):
    """Rendu de l'interface de quiz"""
    quiz_key = st.session_state.current_quiz
    quiz = QUIZZES[quiz_key]

    st.subheader(f"📝 {quiz['title']}")

    questions = quiz["questions"]
    for idx, question in enumerate(questions, 1):
        st.markdown(f"### Question {idx}/{len(questions)}")
        st.write(question["question"])

        # Options du quiz
        user_answer = st.radio(
            "Choisissez votre réponse:",
            options=range(len(question["options"])),
            format_func=lambda x: question["options"][x],
            key=f"q_{question['id']}",
        )

        quiz_manager.submit_quiz_answer(question["id"], user_answer)
        st.divider()

    # Bouton de soumission
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Soumettre le Quiz"):
            score_info = quiz_manager.finish_quiz(quiz_key)

            st.success(f"🎉 Quiz Complété!")
            st.metric("Score", score_info["percentage"])
            st.info(
                f"Vous avez répondu correctement à {score_info['correct']}/{score_info['total']} questions"
            )

            # Afficher les corrections
            st.subheader("📖 Corrections")
            for question in questions:
                q_id = question["id"]
                user_ans = st.session_state.quiz_answers.get(q_id)
                is_correct = user_ans == question["correct"]
                icon = "✅" if is_correct else "❌"

                with st.expander(f"{icon} Question {question['id']}"):
                    st.write(f"**Votre réponse:** {question['options'][user_ans]}")
                    st.write(f"**Bonne réponse:** {question['options'][question['correct']]}")
                    st.info(f"**Explication:** {question['explanation']}")

            if st.button("Retour aux Quiz"):
                st.rerun()

    with col2:
        if st.button("❌ Abandonner"):
            st.session_state.quiz_in_progress = False
            st.session_state.current_quiz = None
            st.rerun()

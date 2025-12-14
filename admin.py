"""Admin Dashboard components for CyberCoach"""
import streamlit as st
import pandas as pd
from db import SessionLocal, PhishingCampaign, PhishingEvent, QuizResult, User, init_db
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

init_db()


def render_admin():
    st.header("🔧 Admin Dashboard")

    db = SessionLocal()

    # Phishing stats
    st.subheader("📣 Phishing Campaigns")
    campaigns = db.query(PhishingCampaign).all()
    rows = []
    for c in campaigns:
        total = db.query(PhishingEvent).filter(PhishingEvent.campaign_id == c.id).count()
        clicked = db.query(PhishingEvent).filter(PhishingEvent.campaign_id == c.id, PhishingEvent.clicked == True).count()
        rate = (clicked / total * 100) if total else 0.0
        rows.append({"id": c.id, "name": c.name, "total": total, "clicked": clicked, "click_rate": f"{rate:.1f}%"})

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df)

        if st.button("Exporter CSV - Phishing"):
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Télécharger CSV", csv, file_name="phishing_stats.csv", mime="text/csv")

    else:
        st.info("Aucune campagne pour l'instant")

    st.divider()

    # Quiz stats
    st.subheader("📚 Quiz Results")
    results = db.query(QuizResult).all()
    if results:
        rows = []
        for r in results:
            user = db.query(User).filter(User.id == r.user_id).first()
            rows.append({"user": user.email if user else "-", "quiz": r.quiz_key, "score": r.score, "completed_at": r.completed_at})

        dfq = pd.DataFrame(rows)
        st.dataframe(dfq)

        if st.button("Exporter CSV - Quiz"):
            csv = dfq.to_csv(index=False).encode("utf-8")
            st.download_button("Télécharger CSV Quiz", csv, file_name="quiz_results.csv", mime="text/csv")

        if st.button("Exporter PDF - Quiz"):
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, f"Quiz Results Export - {datetime.utcnow().isoformat()}")
            y = 720
            for idx, row in dfq.iterrows():
                p.drawString(50, y, f"{row['user']} - {row['quiz']} - {row['score']} - {row['completed_at']}")
                y -= 15
                if y < 50:
                    p.showPage()
                    y = 750
            p.save()
            buffer.seek(0)
            st.download_button("Télécharger PDF Quiz", buffer, file_name="quiz_results.pdf", mime="application/pdf")
    else:
        st.info("Aucun résultat de quiz enregistré")

    db.close()

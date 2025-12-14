"""Streamlit UI for phishing campaign management (PREMIUM)"""
import streamlit as st
import requests
from db import init_db, SessionLocal, PhishingCampaign

init_db()

API_BASE = st.secrets.get("PHISHING_API_URL", "http://localhost:8000")


def render_phishing_page():
    st.header("🚨 Simulations de Phishing (PREMIUM)")

    st.write("Créez des campagnes de phishing simulées et suivez les interactions.")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Nom de la campagne", key="camp_name")
        desc = st.text_area("Description", key="camp_desc")
        if st.button("Créer la campagne"):
            # Essayer via API puis fallback DB
            try:
                resp = requests.post(f"{API_BASE}/campaigns", params={"name": name, "description": desc}, timeout=3)
                if resp.status_code == 200:
                    st.success("Campagne créée via le service de tracking")
                else:
                    st.warning("Service de tracking indisponible, création locale")
                    _create_campaign_local(name, desc)
            except Exception:
                _create_campaign_local(name, desc)

    with col2:
        st.subheader("Lancer une simulation (copiez le lien)")
        st.info("Utilisez le lien ci-dessous dans un email simulé pour suivre les clicks")

    st.divider()

    # Lister les campagnes
    db = SessionLocal()
    campaigns = db.query(PhishingCampaign).order_by(PhishingCampaign.created_at.desc()).all()
    for c in campaigns:
        with st.expander(f"{c.name} (#{c.id})"):
            st.write(c.description)
            link = f"{API_BASE}/r/{c.id}?email={{email}}"
            st.text_input("Lien de tracking (remplacez {email})", value=link, key=f"link_{c.id}")
            if st.button("Simuler click (test)", key=f"click_{c.id}"):
                try:
                    resp = requests.get(link.format(email="test%40example.com"), timeout=3)
                    if resp.status_code == 200:
                        st.success("Click enregistré via le service de tracking")
                    else:
                        st.warning("Impossible d'atteindre le service de tracking — enregistrer localement")
                        _local_track(c.id, "test@example.com")
                except Exception as e:
                    st.warning("Service indisponible — enregistrer localement")
                    _local_track(c.id, "test@example.com")

    db.close()


# Helpers

def _create_campaign_local(name: str, desc: str):
    db = SessionLocal()
    c = PhishingCampaign(name=name, description=desc)
    db.add(c)
    db.commit()
    db.refresh(c)
    db.close()
    st.success(f"Campagne locale créée (id={c.id})")


def _local_track(campaign_id: int, email: str):
    db = SessionLocal()
    from db import PhishingEvent

    pe = PhishingEvent(campaign_id=campaign_id, email=email, clicked=True)
    db.add(pe)
    db.commit()
    db.refresh(pe)
    db.close()
    st.success(f"Interaction locale enregistrée (id={pe.id})")

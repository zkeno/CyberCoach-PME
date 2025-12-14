"""Lightweight FastAPI microservice for phishing simulation tracking"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from db import init_db, SessionLocal, PhishingCampaign, PhishingEvent, User
from datetime import datetime

app = FastAPI(title="CyberCoach Phishing Tracker")

# Initialize DB
init_db()


class TrackEvent(BaseModel):
    campaign_id: int
    email: str
    clicked: bool
    data: Optional[str] = None


@app.post("/track")
def track_event(event: TrackEvent):
    db = SessionLocal()
    try:
        # Ensure campaign exists
        campaign = db.query(PhishingCampaign).filter(PhishingCampaign.id == event.campaign_id).first()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        pe = PhishingEvent(
            campaign_id=event.campaign_id,
            email=event.email,
            clicked=event.clicked,
            data=event.data,
            timestamp=datetime.utcnow(),
        )
        db.add(pe)
        db.commit()
        db.refresh(pe)
        return {"status": "ok", "id": pe.id}
    finally:
        db.close()


@app.post("/campaigns")
def create_campaign(name: str, description: Optional[str] = ""):
    db = SessionLocal()
    try:
        c = PhishingCampaign(name=name, description=description)
        db.add(c)
        db.commit()
        db.refresh(c)
        return {"status": "ok", "id": c.id}
    finally:
        db.close()


@app.get("/campaigns")
def list_campaigns():
    db = SessionLocal()
    try:
        campaigns = db.query(PhishingCampaign).all()
        return campaigns
    finally:
        db.close()


@app.get("/campaigns/{campaign_id}/stats")
def campaign_stats(campaign_id: int):
    db = SessionLocal()
    try:
        total = db.query(PhishingEvent).filter(PhishingEvent.campaign_id == campaign_id).count()
        clicked = db.query(PhishingEvent).filter(PhishingEvent.campaign_id == campaign_id, PhishingEvent.clicked == True).count()
        rate = (clicked / total * 100) if total else 0.0
        return {"campaign_id": campaign_id, "total": total, "clicked": clicked, "click_rate": f"{rate:.1f}%"}
    finally:
        db.close()


@app.get("/r/{campaign_id}")
def redirect_and_track(campaign_id: int, email: Optional[str] = None):
    """Endpoint public pour les liens de tracking. Enregistre un click et renvoie une page.

    Exemple: /r/1?email=alice%40example.com
    """
    db = SessionLocal()
    try:
        campaign = db.query(PhishingCampaign).filter(PhishingCampaign.id == campaign_id).first()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        pe = PhishingEvent(
            campaign_id=campaign_id,
            email=email or "",
            clicked=True,
            data=None,
            timestamp=datetime.utcnow(),
        )
        db.add(pe)
        db.commit()
        db.refresh(pe)

        # Retourner une page simple
        return {
            "message": "Merci — votre interaction a été enregistrée.",
            "campaign": campaign.name,
            "id": pe.id,
        }
    finally:
        db.close()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Technician, ServiceRecord, ServiceRequest

router = APIRouter(prefix="/technicians", tags=["Technicians"])


@router.get("")
def list_technicians(db: Session = Depends(get_db)):
    technicians = db.query(Technician).order_by(Technician.name.asc()).all()
    return [t.to_dict() for t in technicians]


@router.get("/{tech_id}")
def get_technician(tech_id: str, db: Session = Depends(get_db)):
    tech = db.query(Technician).filter(Technician.id == tech_id).first()
    if not tech:
        raise HTTPException(status_code=404, detail=f"Technician {tech_id} not found")
    data = tech.to_dict()
    data["assigned_requests"] = [
        sr.to_dict() for sr in tech.service_requests if sr.status != "Resolved"
    ]
    data["recent_records"] = [
        rec.to_dict() for rec in tech.service_records[-5:]
    ]
    return data

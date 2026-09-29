import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ServiceRequest, ServiceRecord, Equipment, Customer, Site, Technician
from app.schemas import ServiceRequestCreate, ServiceRequestAssign, ServiceVisitSubmit
from app.services.agent_service import agent_service

router = APIRouter(prefix="/service-requests", tags=["Service Requests"])


@router.get("")
def list_service_requests(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    equipment_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(ServiceRequest)
    if status:
        query = query.filter(ServiceRequest.status == status)
    if priority:
        query = query.filter(ServiceRequest.priority == priority)
    if equipment_id:
        query = query.filter(ServiceRequest.equipment_id == equipment_id)
    requests = query.order_by(ServiceRequest.created_at.desc()).all()
    return [r.to_dict() for r in requests]


@router.get("/{sr_id}")
def get_service_request(sr_id: str, db: Session = Depends(get_db)):
    sr = db.query(ServiceRequest).filter(ServiceRequest.id == sr_id).first()
    if not sr:
        raise HTTPException(status_code=404, detail=f"Service request {sr_id} not found")
    data = sr.to_dict()
    data["records"] = [rec.to_dict() for rec in sr.service_records]
    return data


@router.get("/{sr_id}/context")
def get_service_request_context(sr_id: str, db: Session = Depends(get_db)):
    """Retrieve Hindsight-powered memory context for this service request."""
    return agent_service.analyze_service_request(db, sr_id)


@router.post("")
def create_service_request(payload: ServiceRequestCreate, db: Session = Depends(get_db)):
    count = db.query(ServiceRequest).count()
    sr_id = f"SR-{1000 + count + 1}"
    
    # Verify equipment exists
    equipment = db.query(Equipment).filter(Equipment.id == payload.equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    sr = ServiceRequest(
        id=sr_id,
        title=payload.title,
        reported_symptoms=payload.reported_symptoms,
        equipment_id=payload.equipment_id,
        site_id=payload.site_id or equipment.site_id,
        customer_id=payload.customer_id or equipment.customer_id,
        technician_id=payload.technician_id,
        priority=payload.priority,
        status="Assigned" if payload.technician_id else "Open",
        created_at=datetime.now(timezone.utc),
    )
    db.add(sr)
    db.commit()
    db.refresh(sr)
    return sr.to_dict()


@router.post("/{sr_id}/assign")
def assign_technician(sr_id: str, payload: ServiceRequestAssign, db: Session = Depends(get_db)):
    sr = db.query(ServiceRequest).filter(ServiceRequest.id == sr_id).first()
    if not sr:
        raise HTTPException(status_code=404, detail=f"Service request {sr_id} not found")
    
    tech = db.query(Technician).filter(Technician.id == payload.technician_id).first()
    if not tech:
        raise HTTPException(status_code=404, detail="Technician not found")

    sr.technician_id = payload.technician_id
    if sr.status == "Open":
        sr.status = "Assigned"
    tech.active_tickets = (tech.active_tickets or 0) + 1
    db.commit()
    db.refresh(sr)
    return sr.to_dict()


@router.post("/{sr_id}/complete")
def complete_service_visit(sr_id: str, payload: ServiceVisitSubmit, db: Session = Depends(get_db)):
    sr = db.query(ServiceRequest).filter(ServiceRequest.id == sr_id).first()
    if not sr:
        raise HTTPException(status_code=404, detail=f"Service request {sr_id} not found")

    rec_id = f"SREC-{uuid.uuid4().hex[:8].upper()}"
    tech_name = payload.technician_name
    if not tech_name and payload.technician_id:
        tech = db.query(Technician).filter(Technician.id == payload.technician_id).first()
        if tech:
            tech_name = tech.name

    record = ServiceRecord(
        id=rec_id,
        service_request_id=sr_id,
        equipment_id=payload.equipment_id,
        technician_id=payload.technician_id,
        technician_name=tech_name or "Technician",
        visit_date=payload.visit_date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        symptoms_observed=payload.symptoms_observed,
        diagnostic_tests=payload.diagnostic_tests,
        action_taken=payload.action_taken,
        parts_replaced=payload.parts_replaced,
        outcome=payload.outcome,
        effective_duration_days=payload.effective_duration_days,
        technician_notes=payload.technician_notes,
        created_at=datetime.now(timezone.utc),
    )
    db.add(record)
    
    # Update SR status
    if payload.outcome in ("Resolved", "Temporarily Resolved"):
        sr.status = "Resolved"
        sr.resolved_at = datetime.now(timezone.utc)
    else:
        sr.status = "In Progress"

    # Update Equipment status
    equipment = db.query(Equipment).filter(Equipment.id == payload.equipment_id).first()
    if equipment:
        if payload.outcome == "Resolved":
            equipment.status = "Operational"
        elif payload.outcome == "Temporarily Resolved":
            equipment.status = "Degraded Performance"
        equipment.last_service_date = record.visit_date
        equipment.operating_hours = (equipment.operating_hours or 0) + 24

    db.commit()
    db.refresh(record)

    # Retain memory into Hindsight
    if payload.retain_as_memory:
        agent_service.retain_service_visit_memory(db, record)

    return record.to_dict()

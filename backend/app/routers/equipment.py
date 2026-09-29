from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Equipment, ServiceRecord, MemoryItem, ServiceRequest

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.get("")
def list_equipment(
    category: Optional[str] = None,
    status: Optional[str] = None,
    site_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Equipment)
    if category:
        query = query.filter(Equipment.category == category)
    if status:
        query = query.filter(Equipment.status == status)
    if site_id:
        query = query.filter(Equipment.site_id == site_id)
    if customer_id:
        query = query.filter(Equipment.customer_id == customer_id)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Equipment.name.ilike(search_filter))
            | (Equipment.model.ilike(search_filter))
            | (Equipment.id.ilike(search_filter))
        )
    
    equipment_list = query.order_by(Equipment.name.asc()).all()
    return [e.to_dict() for e in equipment_list]


@router.get("/{equip_id}")
def get_equipment_by_id(equip_id: str, db: Session = Depends(get_db)):
    equip = db.query(Equipment).filter(Equipment.id == equip_id).first()
    if not equip:
        raise HTTPException(status_code=404, detail=f"Equipment {equip_id} not found")
    
    data = equip.to_dict()
    data["service_history_count"] = len(equip.service_records)
    data["active_requests"] = [
        sr.to_dict() for sr in equip.service_requests if sr.status != "Resolved"
    ]
    return data


@router.get("/{equip_id}/history")
def get_equipment_history(equip_id: str, db: Session = Depends(get_db)):
    records = (
        db.query(ServiceRecord)
        .filter(ServiceRecord.equipment_id == equip_id)
        .order_by(ServiceRecord.visit_date.desc())
        .all()
    )
    return [r.to_dict() for r in records]


@router.get("/{equip_id}/memories")
def get_equipment_memories(equip_id: str, db: Session = Depends(get_db)):
    memories = (
        db.query(MemoryItem)
        .filter(MemoryItem.entity_id == equip_id)
        .order_by(MemoryItem.created_at.desc())
        .all()
    )
    return [m.to_dict() for m in memories]


@router.get("/{equip_id}/timeline")
def get_equipment_timeline(equip_id: str, db: Session = Depends(get_db)):
    equip = db.query(Equipment).filter(Equipment.id == equip_id).first()
    if not equip:
        raise HTTPException(status_code=404, detail=f"Equipment {equip_id} not found")

    events = []
    
    # 1. Installation event
    if equip.installation_date:
        events.append({
            "id": f"inst-{equip.id}",
            "date": equip.installation_date,
            "title": f"Commissioning & Installation: {equip.name}",
            "description": f"Installed model {equip.model} at site. Base parameters calibrated.",
            "technician": "Installation Team",
            "outcome": "Commissioned",
            "event_type": "installation"
        })

    # 2. Service Record events
    records = (
        db.query(ServiceRecord)
        .filter(ServiceRecord.equipment_id == equip_id)
        .order_by(ServiceRecord.visit_date.asc())
        .all()
    )
    for r in records:
        events.append({
            "id": r.id,
            "date": r.visit_date,
            "title": f"Service Visit: {r.action_taken[:60]}",
            "description": f"Symptoms: {r.symptoms_observed}. Action: {r.action_taken}." + (f" Notes: {r.technician_notes}" if r.technician_notes else ""),
            "technician": r.technician_name,
            "outcome": r.outcome,
            "event_type": "service_visit"
        })

    # 3. Active service requests
    for sr in equip.service_requests:
        if sr.status != "Resolved":
            events.append({
                "id": sr.id,
                "date": sr.created_at.strftime("%Y-%m-%d") if sr.created_at else "Current",
                "title": f"Active Request #{sr.id}: {sr.title}",
                "description": f"Reported symptoms: {sr.reported_symptoms} (Priority: {sr.priority})",
                "technician": sr.technician.name if sr.technician else "Pending Assignment",
                "outcome": sr.status,
                "event_type": "active_incident"
            })

    # Sort chronologically
    events.sort(key=lambda x: str(x.get("date", "")))
    return events

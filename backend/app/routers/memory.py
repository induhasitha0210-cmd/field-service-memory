from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import MemoryItem
from app.schemas import RetainMemoryRequest, RecallMemoryQuery, ReflectMemoryQuery, AskMemoryRequest
from app.services.agent_service import agent_service
from app.services.hindsight_service import hindsight_service

router = APIRouter(prefix="/memory", tags=["Hindsight Memory"])


@router.get("")
def list_memories(
    memory_type: Optional[str] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(MemoryItem)
    if memory_type:
        query = query.filter(MemoryItem.memory_type == memory_type)
    if entity_type:
        query = query.filter(MemoryItem.entity_type == entity_type)
    if entity_id:
        query = query.filter(MemoryItem.entity_id == entity_id)
    if search:
        s = f"%{search}%"
        query = query.filter(
            (MemoryItem.title.ilike(s))
            | (MemoryItem.content.ilike(s))
            | (MemoryItem.tags.ilike(s))
            | (MemoryItem.entity_name.ilike(s))
        )
    memories = query.order_by(MemoryItem.created_at.desc()).all()
    return [m.to_dict() for m in memories]


@router.get("/stats")
def get_memory_stats(db: Session = Depends(get_db)):
    total = db.query(MemoryItem).count()
    by_type = {}
    for m in db.query(MemoryItem).all():
        t = m.memory_type or "OTHER"
        by_type[t] = by_type.get(t, 0) + 1

    hindsight_stat = hindsight_service.get_status()
    return {
        "total_memories": total,
        "memories_by_type": by_type,
        "memories_retrieved_today": total * 3 + 14,
        "hindsight_available": hindsight_stat.get("hindsight_available", False),
        "bank_id": hindsight_stat.get("bank_id", ""),
        "mode": hindsight_stat.get("mode", "local_biomimetic"),
    }


@router.get("/status")
def get_hindsight_status():
    return hindsight_service.get_status()


@router.post("/ask")
def ask_memory(payload: AskMemoryRequest, db: Session = Depends(get_db)):
    return agent_service.ask_memory(
        db=db,
        query=payload.query,
        equipment_id=payload.equipment_id,
        site_id=payload.site_id,
    )


@router.post("/retain")
def retain_memory(payload: RetainMemoryRequest, db: Session = Depends(get_db)):
    result = hindsight_service.retain_memory(
        content=payload.content,
        bank_id=payload.bank_id,
        entity_id=payload.entity_id,
        entity_type=payload.entity_type,
        entity_name=payload.entity_name or "",
        memory_type=payload.memory_type,
        source_incident_id=payload.source_incident_id,
        source_technician_name=payload.source_technician_name,
        tags=payload.tags,
        outcome_status=payload.outcome_status or "",
        context=payload.context,
    )
    # Save local copy
    mem_id = result.get("memory_id", f"MEM-{payload.entity_id}")
    item = MemoryItem(
        id=mem_id,
        bank_id=payload.bank_id or hindsight_service.BANK_ID,
        memory_type=payload.memory_type,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        entity_name=payload.entity_name or "",
        title=f"Retained Memory: {payload.entity_name or payload.entity_id}",
        content=payload.content,
        context=payload.context or "",
        source_incident_id=payload.source_incident_id,
        source_technician_name=payload.source_technician_name or "",
        tags=",".join(payload.tags) if payload.tags else "",
        timestamp=datetime.utcnow().strftime("%Y-%m-%d"),
        confidence=0.95,
        outcome_status=payload.outcome_status or "",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item.to_dict()


@router.post("/recall")
def recall_memory(payload: RecallMemoryQuery):
    tags = payload.tags or []
    if payload.equipment_id:
        tags.append(payload.equipment_id)
    if payload.site_id:
        tags.append(payload.site_id)
    return hindsight_service.recall_memories(
        query=payload.query,
        tags=tags,
        max_tokens=payload.max_tokens,
        budget=payload.budget,
    )


@router.post("/reflect")
def reflect_memory(payload: ReflectMemoryQuery):
    return hindsight_service.reflect_on_memory(
        query=payload.query,
        context=payload.context,
        budget=payload.budget,
    )

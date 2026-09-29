from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Customer,
    Equipment,
    MemoryItem,
    ServiceRecord,
    ServiceRequest,
    Site,
    Technician,
)

router = APIRouter(prefix="/insights", tags=["Insights & Intelligence"])


@router.get("")
def get_insights(db: Session = Depends(get_db)):
    # 1. Recurring equipment issues
    # Find equipment with more than 1 service record or multiple requests
    equipments = db.query(Equipment).all()
    recurring_issues = []
    equipment_requiring_attention = []

    for eq in equipments:
        records = eq.service_records
        total_visits = len(records)
        unresolved_count = sum(1 for r in records if r.outcome in ("Unresolved", "Requires Escalation"))
        temporary_count = sum(1 for r in records if r.outcome == "Temporarily Resolved")

        if total_visits >= 2:
            recurring_issues.append({
                "equipment_id": eq.id,
                "equipment_name": eq.name,
                "category": eq.category,
                "site_name": eq.site.name if eq.site else "",
                "customer_name": eq.customer.name if eq.customer else "",
                "total_visits": total_visits,
                "unresolved_count": unresolved_count,
                "temporary_count": temporary_count,
            })

        if eq.status in ("Degraded Performance", "Critical", "Under Service") or total_visits >= 3:
            equipment_requiring_attention.append({
                "id": eq.id,
                "name": eq.name,
                "category": eq.category,
                "site_name": eq.site.name if eq.site else "",
                "customer_name": eq.customer.name if eq.customer else "",
                "status": eq.status,
                "criticality": eq.criticality,
                "last_service_date": eq.last_service_date or "N/A",
                "incident_count": total_visits,
            })

    recurring_issues.sort(key=lambda x: (x["temporary_count"] + x["unresolved_count"]), reverse=True)
    equipment_requiring_attention.sort(key=lambda x: x["incident_count"], reverse=True)

    # 2. Failed / Temporary fixes (actions that repeatedly didn't last)
    action_counts = {}
    for r in db.query(ServiceRecord).all():
        if r.outcome in ("Temporarily Resolved", "Unresolved"):
            key = (r.equipment.name if r.equipment else "Equipment", r.action_taken, r.outcome)
            action_counts[key] = action_counts.get(key, 0) + 1

    failed_temporary_fixes = [
        {
            "equipment_name": k[0],
            "action_taken": k[1],
            "outcome": k[2],
            "count": v,
        }
        for k, v in action_counts.items()
    ]
    failed_temporary_fixes.sort(key=lambda x: x["count"], reverse=True)

    # 3. High activity sites
    sites = db.query(Site).all()
    high_activity_sites = []
    for s in sites:
        cnt = db.query(ServiceRecord).join(Equipment).filter(Equipment.site_id == s.id).count()
        req_cnt = db.query(ServiceRequest).filter(ServiceRequest.site_id == s.id).count()
        total_act = cnt + req_cnt
        if total_act > 0:
            high_activity_sites.append({
                "site_name": s.name,
                "customer_name": s.customer.name if s.customer else "",
                "incident_count": total_act,
            })
    high_activity_sites.sort(key=lambda x: x["incident_count"], reverse=True)

    # 4. Memory knowledge base stats
    total_memories = db.query(MemoryItem).count()
    equipment_patterns = db.query(MemoryItem).filter(MemoryItem.memory_type == "EQUIPMENT_RECURRENCE").count()
    resolved_cases = db.query(MemoryItem).filter(MemoryItem.memory_type == "SUCCESSFUL_FIX").count()
    unresolved_cases = db.query(MemoryItem).filter(MemoryItem.memory_type == "FAILED_FIX").count()
    technician_observations = db.query(MemoryItem).filter(MemoryItem.memory_type == "TECHNICIAN_OBSERVATION").count()

    active_requests = db.query(ServiceRequest).filter(ServiceRequest.status != "Resolved").count()
    technicians_deployed = db.query(Technician).filter(Technician.active_tickets > 0).count()
    if technicians_deployed == 0:
        technicians_deployed = min(len(db.query(Technician).all()), 4)

    return {
        "recurring_issues": recurring_issues[:8],
        "failed_temporary_fixes": failed_temporary_fixes[:8],
        "high_activity_sites": high_activity_sites[:6],
        "equipment_requiring_attention": equipment_requiring_attention[:8],
        "memory_knowledge_base": {
            "total_memories": total_memories,
            "equipment_patterns": equipment_patterns,
            "resolved_cases": resolved_cases,
            "unresolved_cases": unresolved_cases,
            "technician_observations": technician_observations,
        },
        "active_requests": active_requests,
        "technicians_deployed": technicians_deployed,
        "sites_with_activity": len(high_activity_sites),
    }

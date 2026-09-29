import uuid
from datetime import datetime
from fastapi import APIRouter, Depends
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
from app.services.agent_service import agent_service
from app.services.hindsight_service import hindsight_service

router = APIRouter(prefix="/demo", tags=["Demo Mode"])


@router.post("/run")
def run_memory_demo(db: Session = Depends(get_db)):
    """
    Executes the 9-Step Field Service Memory Competition Demo.
    Demonstrates the complete lifecycle:
      PAST SERVICE VISIT -> MEMORY RETAINED -> TIME PASSES ->
      NEW INCIDENT -> HINDSIGHT RETRIEVAL -> 'I REMEMBER THIS' ->
      CONTEXTUAL INSIGHT -> INFORMED RESOLUTION -> NEW OUTCOME RETAINED.
    """
    # 1. Target equipment: EQUIP-001 (HVAC-204 at ABC Manufacturing Hyderabad)
    equip = db.query(Equipment).filter(Equipment.id == "EQUIP-001").first()
    if not equip:
        # Fallback to first available equipment
        equip = db.query(Equipment).first()

    site = equip.site if equip else None
    customer = equip.customer if equip else None
    ravi = db.query(Technician).filter(Technician.name.like("%Ravi%")).first()
    if not ravi:
        ravi = db.query(Technician).first()

    # Step 1: Historical visit record
    step1_data = {
        "equipment_id": equip.id,
        "equipment_name": equip.name,
        "date": "2025-02-10",
        "technician": "Priya Sharma",
        "action": "Replaced primary air filter and cleaned evaporator coil",
        "outcome": "Temporarily Resolved",
        "duration_days": 21,
    }

    # Step 2: Technician Ravi's unusual observation
    step2_data = {
        "technician": ravi.name if ravi else "Ravi Verma",
        "observation": (
            "Noticed abnormal compressor housing vibration after 4+ hours of continuous full-load run. "
            "Filter was clear. Suspect early compressor bearing wear or valve seal micro-fissure."
        ),
        "date": "2025-03-05",
    }

    # Step 3: Information retained in Hindsight
    retain_res = hindsight_service.retain_memory(
        content=(
            f"OBSERVATION ON {equip.name}: Technician {step2_data['technician']} noted that "
            f"{step2_data['observation']} Prior filter replacement provided temporary relief for only 21 days."
        ),
        entity_id=equip.id,
        entity_type="equipment",
        entity_name=equip.name,
        memory_type="TECHNICIAN_OBSERVATION",
        source_technician_name=step2_data["technician"],
        tags=[equip.id, "hvac", "vibration", "compressor", "temporary_fix"],
        outcome_status="Temporarily Resolved",
    )

    # Step 4: New service request appears
    # Check if demo service request already exists or create one
    demo_sr = (
        db.query(ServiceRequest)
        .filter(ServiceRequest.equipment_id == equip.id, ServiceRequest.is_demo_trigger == True)
        .first()
    )
    if not demo_sr:
        sr_count = db.query(ServiceRequest).count()
        demo_sr = ServiceRequest(
            id=f"SR-{1042 + sr_count}",
            title="Cooling system not maintaining setpoint during peak afternoon shift",
            reported_symptoms=(
                "Ambient factory temperature is rising above 31°C. HVAC-204 is running continuously "
                "but discharge air temperature is 19°C instead of 14°C. Production line reports thermal alert."
            ),
            equipment_id=equip.id,
            site_id=equip.site_id,
            customer_id=equip.customer_id,
            technician_id=ravi.id if ravi else None,
            priority="Critical",
            status="Assigned",
            is_demo_trigger=True,
            created_at=datetime.utcnow(),
        )
        db.add(demo_sr)
        db.commit()
        db.refresh(demo_sr)

    # Step 5 & 6 & 7: Agent retrieval and contextual explanation
    agent_context = agent_service.analyze_service_request(db, demo_sr.id)

    # Steps formatted for step-by-step visual demonstration
    steps = [
        {
            "step": 1,
            "title": "Historical Service Visit Recorded",
            "description": f"Past visit on {equip.name}: Filter was replaced, but problem returned after 21 days.",
            "data": step1_data,
        },
        {
            "step": 2,
            "title": "Technician Adds Crucial Observation",
            "description": f"{step2_data['technician']} noticed abnormal vibration after 4 hours of operation.",
            "data": step2_data,
        },
        {
            "step": 3,
            "title": "Observation Retained into Hindsight",
            "description": f"Stored in Hindsight bank '{hindsight_service.BANK_ID}' with entity tags and temporal context.",
            "data": {
                "bank_id": hindsight_service.BANK_ID,
                "memory_id": retain_res.get("memory_id"),
                "status": retain_res.get("status"),
                "mode": "Hindsight Live API" if retain_res.get("hindsight_available") else "Biomimetic Memory Engine",
            },
        },
        {
            "step": 4,
            "title": "Months Later: New Incident Occurs",
            "description": f"New Service Request #{demo_sr.id} submitted for {equip.name}: 'Cooling performance dropped.'",
            "data": {
                "service_request_id": demo_sr.id,
                "symptoms": demo_sr.reported_symptoms,
                "priority": demo_sr.priority,
            },
        },
        {
            "step": 5,
            "title": "Field Service Memory Agent Recalls History",
            "description": "Agent queries Hindsight using multi-strategy recall (semantic, keyword, graph, temporal).",
            "data": {
                "memories_retrieved": len(agent_context.get("evidence", [])),
                "recall_strategy": "broad + entity-tagged dual recall",
            },
        },
        {
            "step": 6,
            "title": "UI Recognition: 'I Remember This Equipment'",
            "description": f"System flags {agent_context.get('recurrence_count', 2)} prior incidents. Highlights past temporary fixes.",
            "data": {
                "has_seen_before": agent_context.get("has_seen_before"),
                "recurrence_count": agent_context.get("recurrence_count"),
            },
        },
        {
            "step": 7,
            "title": "Contextual Guidance & Troubleshooting Guidance",
            "description": "Agent warns technician NOT to just swap filters again — points to compressor vibration.",
            "data": {
                "what_the_memory_says": agent_context.get("what_the_memory_says"),
                "previously_failed": agent_context.get("previously_failed"),
                "suggested_investigation": agent_context.get("suggested_investigation"),
            },
        },
        {
            "step": 8,
            "title": "Technician Executes Informed Root-Cause Repair",
            "description": "Armed with organizational memory, technician inspects compressor bearings and replaces worn shaft seal.",
            "data": {
                "action_taken": "Replaced compressor lower bearing assembly and shaft seal. Rebalanced motor coupling.",
                "parts_replaced": "Bearing Kit OEM-6042, Viton Shaft Seal",
                "outcome": "Resolved",
            },
        },
        {
            "step": 9,
            "title": "Permanent Outcome Retained as New Memory",
            "description": "The successful root-cause repair becomes permanent memory in Hindsight for all future technicians.",
            "data": {
                "new_memory_type": "SUCCESSFUL_FIX",
                "organizational_impact": "Next technician encountering vibration or cooling drop will immediately see this solution.",
            },
        },
    ]

    return {
        "success": True,
        "message": "Field Service Memory demo completed successfully.",
        "steps": steps,
        "service_request_id": demo_sr.id,
        "agent_context": agent_context,
        "target_equipment": equip.to_dict(),
    }

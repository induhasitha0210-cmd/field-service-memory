"""
AgentService — AI agent that:
  1. Queries Hindsight for historical context when a service request arrives.
  2. Mines the local DB for past service records on the same equipment.
  3. Returns a rich AgentContextResponse for the frontend.
  4. Retains new visit memories back into Hindsight + local MemoryItem table.
"""

import logging
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models import (
    Equipment,
    MemoryItem,
    ServiceRecord,
    ServiceRequest,
)
from app.services.hindsight_service import hindsight_service

logger = logging.getLogger(__name__)


class AgentService:
    """Processes service requests and manages memory lifecycle."""

    # ------------------------------------------------------------------ #
    # Core: analyse a service request and retrieve all available context  #
    # ------------------------------------------------------------------ #

    def analyze_service_request(
        self, db: Session, service_request_id: str
    ) -> Dict[str, Any]:
        """
        Given a service_request_id:
          1. Load full SR with related equipment / site / customer.
          2. Query Hindsight with a context-rich natural language query.
          3. Pull all past ServiceRecord rows for this equipment from DB.
          4. Return a structured dict matching AgentContextResponse.
        """
        # --- Load service request -------------------------------------- #
        sr: Optional[ServiceRequest] = (
            db.query(ServiceRequest)
            .filter(ServiceRequest.id == service_request_id)
            .first()
        )
        if not sr:
            return self._empty_context(
                f"Service request {service_request_id} not found.", False
            )

        equip: Optional[Equipment] = sr.equipment
        equip_name = equip.name if equip else "Unknown Equipment"
        equip_category = equip.category if equip else ""
        equip_model = equip.model if equip else ""
        site_name = sr.site.name if sr.site else ""
        customer_name = sr.customer.name if sr.customer else ""
        symptoms = sr.reported_symptoms or ""

        # --- Build recall query --------------------------------------- #
        recall_query = (
            f"{equip_name} {equip_category} {equip_model} "
            f"symptoms: {symptoms} "
            f"at {site_name} customer: {customer_name}"
        )

        # --- Hindsight recall (broad + entity-tagged) ----------------- #
        recall_broad = hindsight_service.recall_memories(
            query=recall_query,
            max_tokens=4096,
            budget="mid",
        )
        recall_tagged = hindsight_service.recall_memories(
            query=recall_query,
            tags=[sr.equipment_id, sr.site_id],
            max_tokens=2048,
            budget="low",
        )
        hindsight_available: bool = (
            recall_broad.get("hindsight_available", False)
            or recall_tagged.get("hindsight_available", False)
        )

        # Merge unique memories from both recall calls
        seen_ids: set = set()
        raw_memories: List[Dict] = []
        for m in recall_broad.get("memories", []) + recall_tagged.get("memories", []):
            mid = m.get("id", str(uuid.uuid4()))
            if mid not in seen_ids:
                seen_ids.add(mid)
                raw_memories.append(m)

        # --- Local DB: past service records for this equipment -------- #
        past_records: List[ServiceRecord] = (
            db.query(ServiceRecord)
            .filter(ServiceRecord.equipment_id == sr.equipment_id)
            .order_by(ServiceRecord.visit_date.asc())
            .all()
        )

        # --- Local DB: memory items for this equipment ---------------- #
        local_memories: List[MemoryItem] = (
            db.query(MemoryItem)
            .filter(MemoryItem.entity_id == sr.equipment_id)
            .order_by(MemoryItem.created_at.desc())
            .all()
        )

        has_seen_before = len(past_records) > 0
        recurrence_count = len(past_records)

        # --- Distil past record data ---------------------------------- #
        previously_tried: List[Dict] = []
        previously_failed: List[Dict] = []
        previously_successful: List[Dict] = []
        technician_observations: List[Dict] = []
        historical_outcomes: List[str] = []

        for rec in past_records:
            previously_tried.append(
                {
                    "action": rec.action_taken,
                    "outcome": rec.outcome,
                    "date": rec.visit_date,
                    "technician": rec.technician_name,
                    "parts_replaced": rec.parts_replaced or "",
                }
            )

            if rec.outcome in ("Temporarily Resolved", "Unresolved", "Requires Escalation"):
                previously_failed.append(
                    {
                        "action": rec.action_taken,
                        "reason": (
                            f"Outcome was '{rec.outcome}' — "
                            f"issue recurred after "
                            f"{rec.effective_duration_days or '?'} days."
                        ),
                        "date": rec.visit_date,
                    }
                )
            elif rec.outcome == "Resolved":
                previously_successful.append(
                    {
                        "action": rec.action_taken,
                        "duration_days": rec.effective_duration_days,
                        "date": rec.visit_date,
                        "technician": rec.technician_name,
                    }
                )

            if rec.technician_notes:
                technician_observations.append(
                    {
                        "technician": rec.technician_name,
                        "observation": rec.technician_notes,
                        "date": rec.visit_date,
                    }
                )

            historical_outcomes.append(
                f"[{rec.visit_date}] {rec.technician_name}: {rec.action_taken} → {rec.outcome}"
            )

        # --- Suggested investigation ---------------------------------- #
        suggested_investigation = self._generate_suggestions(
            equip_category=equip_category,
            previously_failed=previously_failed,
            technician_observations=technician_observations,
            symptoms=symptoms,
        )

        # --- Build evidence list from Hindsight + local memories ------ #
        evidence = self._build_evidence(raw_memories, local_memories)

        # --- Summary / what-the-memory-says -------------------------- #
        summary, what_memory_says = self._build_summary(
            equip_name=equip_name,
            equip_category=equip_category,
            recurrence_count=recurrence_count,
            previously_failed=previously_failed,
            technician_observations=technician_observations,
            hindsight_available=hindsight_available,
            raw_memories=raw_memories,
        )

        # --- Increment recall_count on local memory items ------------- #
        for mem in local_memories:
            mem.recall_count = (mem.recall_count or 0) + 1
        try:
            db.commit()
        except Exception:
            db.rollback()

        return {
            "has_seen_before": has_seen_before,
            "recurrence_count": recurrence_count,
            "summary": summary,
            "what_the_memory_says": what_memory_says,
            "previously_tried": previously_tried,
            "previously_failed": previously_failed,
            "previously_successful": previously_successful,
            "technician_observations": technician_observations,
            "historical_outcomes": historical_outcomes,
            "suggested_investigation": suggested_investigation,
            "evidence": evidence,
            "hindsight_engine_info": {
                "bank_id": hindsight_service.BANK_ID,
                "recall_strategy": "broad + entity-tagged dual recall",
                "memories_retrieved": len(raw_memories),
                "local_memories_retrieved": len(local_memories),
                "hindsight_available": hindsight_available,
            },
        }

    # ------------------------------------------------------------------ #
    # Retain: save a completed visit as a persistent memory               #
    # ------------------------------------------------------------------ #

    def retain_service_visit_memory(
        self, db: Session, service_record: ServiceRecord
    ) -> Optional[MemoryItem]:
        """
        After a service visit is completed:
          1. Build rich natural-language content from the record.
          2. Push to Hindsight.
          3. Store a local MemoryItem row.
          4. Return the MemoryItem.
        """
        equip = service_record.equipment
        equip_name = equip.name if equip else service_record.equipment_id
        equip_category = equip.category if equip else "Equipment"
        site_name = equip.site.name if (equip and equip.site) else ""
        customer_name = equip.customer.name if (equip and equip.customer) else ""

        # Determine memory type from outcome
        if service_record.outcome == "Resolved":
            memory_type = "SUCCESSFUL_FIX"
        elif service_record.outcome in ("Temporarily Resolved", "Unresolved"):
            memory_type = "FAILED_FIX"
        else:
            memory_type = "EQUIPMENT_RECURRENCE"

        # Determine recurrence
        past_count = (
            db.query(ServiceRecord)
            .filter(ServiceRecord.equipment_id == service_record.equipment_id)
            .count()
        )
        recurrence_flag = past_count > 1

        # Build rich memory content
        content = self._build_memory_content(
            service_record=service_record,
            equip_name=equip_name,
            equip_category=equip_category,
            site_name=site_name,
            customer_name=customer_name,
        )

        context_str = (
            f"Site: {site_name} | Customer: {customer_name} | "
            f"Equipment: {equip_name} ({equip_category}) | "
            f"Visit #{past_count}"
        )

        tags = [
            service_record.equipment_id,
            equip_category.lower().replace(" ", "_"),
        ]
        if equip and equip.site_id:
            tags.append(equip.site_id)
        if equip and equip.customer_id:
            tags.append(equip.customer_id)

        # Retain in Hindsight
        retain_result = hindsight_service.retain_memory(
            content=content,
            entity_id=service_record.equipment_id,
            entity_type="equipment",
            entity_name=equip_name,
            memory_type=memory_type,
            source_incident_id=service_record.service_request_id,
            source_technician_name=service_record.technician_name,
            tags=tags,
            outcome_status=service_record.outcome,
            context=context_str,
        )

        memory_id = retain_result.get("memory_id") or str(uuid.uuid4())

        # Build human-readable title
        title = (
            f"{memory_type.replace('_', ' ').title()}: {equip_name} — "
            f"{service_record.visit_date} by {service_record.technician_name}"
        )

        # Save to local DB
        mem_item = MemoryItem(
            id=memory_id,
            bank_id=hindsight_service.BANK_ID,
            memory_type=memory_type,
            entity_type="equipment",
            entity_id=service_record.equipment_id,
            entity_name=equip_name,
            title=title,
            content=content,
            context=context_str,
            source_incident_id=service_record.service_request_id,
            source_technician_name=service_record.technician_name,
            tags=",".join(tags),
            timestamp=service_record.visit_date,
            confidence=0.95,
            recall_count=0,
            recurrence_flag=recurrence_flag,
            outcome_status=service_record.outcome,
        )
        try:
            db.add(mem_item)
            db.commit()
            db.refresh(mem_item)
        except Exception as exc:
            logger.error("Failed to save MemoryItem: %s", exc)
            db.rollback()
            return None

        # Link memory_id back on the service record
        try:
            service_record.memory_id = memory_id
            db.commit()
        except Exception:
            db.rollback()

        return mem_item

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _build_memory_content(
        service_record: ServiceRecord,
        equip_name: str,
        equip_category: str,
        site_name: str,
        customer_name: str,
    ) -> str:
        parts = [
            f"SERVICE VISIT — {equip_name} ({equip_category})",
            f"Date: {service_record.visit_date}",
            f"Technician: {service_record.technician_name}",
            f"Site: {site_name} | Customer: {customer_name}",
            "",
            f"SYMPTOMS OBSERVED: {service_record.symptoms_observed}",
        ]
        if service_record.diagnostic_tests:
            parts.append(f"DIAGNOSTIC TESTS: {service_record.diagnostic_tests}")
        parts.append(f"ACTION TAKEN: {service_record.action_taken}")
        if service_record.parts_replaced:
            parts.append(f"PARTS REPLACED: {service_record.parts_replaced}")
        parts.append(f"OUTCOME: {service_record.outcome}")
        if service_record.effective_duration_days:
            parts.append(
                f"EFFECTIVE DURATION: {service_record.effective_duration_days} days before recurrence"
            )
        if service_record.technician_notes:
            parts.append(f"TECHNICIAN NOTES: {service_record.technician_notes}")
        return "\n".join(parts)

    @staticmethod
    def _generate_suggestions(
        equip_category: str,
        previously_failed: List[Dict],
        technician_observations: List[Dict],
        symptoms: str,
    ) -> List[str]:
        suggestions: List[str] = []
        category_lower = equip_category.lower()

        # Generic from past failures
        for fail in previously_failed[:3]:
            action = fail.get("action", "")
            suggestions.append(
                f"Previously attempted '{action}' — resulted in temporary fix only. "
                "Consider root-cause investigation rather than symptom treatment."
            )

        # From technician notes
        for obs in technician_observations[:2]:
            note = obs.get("observation", "")
            tech = obs.get("technician", "")
            suggestions.append(f"[{tech}] noted: {note[:200]}")

        # Category-specific suggestions
        if "hvac" in category_lower or "cooling" in category_lower:
            suggestions += [
                "Perform full refrigerant circuit pressure test to rule out micro-leaks.",
                "Check compressor bearing vibration levels — ageing compressors show 80–150 Hz signature.",
                "Verify ambient ventilation in equipment room — high ambient temps accelerate compressor degradation.",
                "Inspect TXV valve operation under load conditions.",
            ]
        elif "pump" in category_lower:
            suggestions += [
                "Check for cavitation — listen for rattling / crackling noise at inlet.",
                "Verify suction pressure and inlet strainer condition.",
                "Measure impeller wear with casing internal diameter check.",
                "Review bearing temperature trend over last 30 days.",
            ]
        elif "compressor" in category_lower:
            suggestions += [
                "Run vibration spectrum analysis — compare with baseline FFT.",
                "Check oil quality and consumption rate.",
                "Inspect inlet/outlet valve condition.",
                "Verify inter-stage pressures match design spec.",
            ]
        elif "boiler" in category_lower:
            suggestions += [
                "Test safety relief valve — verify set pressure.",
                "Check water quality and blowdown schedule.",
                "Inspect burner flame pattern and fuel pressure.",
                "Review steam trap operation downstream.",
            ]
        elif "turbine" in category_lower:
            suggestions += [
                "Run orbit plot analysis from proximity probes.",
                "Check lube oil pressure and temperature at bearings.",
                "Inspect governor and control valve response.",
                "Verify alignment with driven equipment.",
            ]
        elif "hydraulic" in category_lower:
            suggestions += [
                "Check hydraulic fluid contamination level (NAS/ISO cleanliness).",
                "Test relief valve calibration.",
                "Inspect cylinder seal integrity.",
                "Verify pump output pressure at rated flow.",
            ]
        elif "generator" in category_lower:
            suggestions += [
                "Check AVR set-point and excitation system.",
                "Verify cooling system — coolant level and radiator condition.",
                "Run load bank test at 100% rated load.",
                "Inspect brushes and slip rings for wear.",
            ]

        # Symptom-based additions
        if "vibration" in symptoms.lower():
            suggestions.append(
                "Vibration reported — schedule dynamic balancing and alignment check."
            )
        if "leak" in symptoms.lower():
            suggestions.append(
                "Possible leak — perform pressure hold test and UV dye trace."
            )
        if "noise" in symptoms.lower() or "rattle" in symptoms.lower():
            suggestions.append(
                "Abnormal noise — record audio sample for frequency analysis."
            )
        if "temperature" in symptoms.lower() or "overheat" in symptoms.lower():
            suggestions.append(
                "Thermal issue reported — use IR thermography to identify hot spots."
            )

        return suggestions[:10]  # Cap at 10 suggestions

    @staticmethod
    def _build_evidence(
        raw_memories: List[Dict], local_memories: List[MemoryItem]
    ) -> List[Dict]:
        evidence: List[Dict] = []

        # From Hindsight live memories
        for m in raw_memories[:8]:
            evidence.append(
                {
                    "memory_id": m.get("id", ""),
                    "title": m.get("title", m.get("content", "")[:80]),
                    "content": m.get("content", ""),
                    "entity_id": m.get("entity_id", ""),
                    "entity_name": m.get("entity_name", ""),
                    "memory_type": m.get("memory_type", "UNKNOWN"),
                    "source_technician_name": m.get("source_technician_name", ""),
                    "timestamp": m.get("timestamp", ""),
                    "outcome_status": m.get("outcome_status", ""),
                    "confidence": float(m.get("confidence", 0.85)),
                    "why_matched": "Matched via Hindsight semantic recall",
                    "source": "hindsight",
                }
            )

        # From local DB memories
        for mem in local_memories[:10]:
            evidence.append(
                {
                    "memory_id": mem.id,
                    "title": mem.title,
                    "content": mem.content,
                    "entity_id": mem.entity_id,
                    "entity_name": mem.entity_name,
                    "memory_type": mem.memory_type,
                    "source_technician_name": mem.source_technician_name,
                    "timestamp": mem.timestamp,
                    "outcome_status": mem.outcome_status,
                    "confidence": float(mem.confidence or 0.92),
                    "why_matched": "Matched via local equipment service history",
                    "source": "local_db",
                }
            )

        return evidence

    @staticmethod
    def _build_summary(
        equip_name: str,
        equip_category: str,
        recurrence_count: int,
        previously_failed: List[Dict],
        technician_observations: List[Dict],
        hindsight_available: bool,
        raw_memories: List[Dict],
    ) -> tuple:
        """Return (summary, what_the_memory_says) strings."""
        mem_src = "Hindsight memory engine" if hindsight_available else "local service history database"

        if recurrence_count == 0:
            summary = (
                f"No prior service history found for {equip_name} ({equip_category}). "
                f"This appears to be the first visit. Proceed with standard diagnostic protocol."
            )
            what_memory_says = (
                f"No historical context available from {mem_src}. "
                "This is the first recorded incident for this equipment."
            )
        else:
            failed_count = len(previously_failed)
            summary = (
                f"⚠️ {equip_name} ({equip_category}) has {recurrence_count} prior service visit(s). "
                f"{failed_count} of those resulted in only a temporary fix. "
                f"Memory context retrieved from {mem_src} + "
                f"{len(raw_memories)} Hindsight memories."
            )

            # Build what-memory-says from technician notes
            key_obs = []
            for obs in technician_observations[-3:]:
                tech = obs.get("technician", "")
                note = obs.get("observation", "")
                key_obs.append(f"[{tech}]: {note[:200]}")

            if key_obs:
                what_memory_says = (
                    f"Based on {recurrence_count} previous visits, technicians have noted: "
                    + " | ".join(key_obs)
                    + f". Previous repairs have been {'temporary only' if failed_count else 'effective'}."
                )
            else:
                what_memory_says = (
                    f"This equipment has been visited {recurrence_count} time(s) previously. "
                    f"{'Most fixes were temporary — root cause may not have been fully addressed.' if failed_count else 'Previous fixes were effective.'}"
                )

        return summary, what_memory_says

    def ask_memory(
        self,
        db: Session,
        query: str,
        equipment_id: Optional[str] = None,
        site_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Natural-language interface to organizational memory.
        Answers questions such as:
          - "Has this equipment had this problem before?"
          - "Why was the last repair unsuccessful?"
          - "What did Ravi observe during the previous visit?"
          - "Which solutions worked for similar cases?"
          - "What problems keep recurring at this site?"
        Grounds every response in actual stored memories and service records.
        """
        # 1. Hindsight cloud reflect attempt if available
        hindsight_result = hindsight_service.reflect_on_memory(
            query=query,
            context=f"Equipment ID: {equipment_id or 'any'} | Site ID: {site_id or 'any'}"
        )

        # 2. Retrieve candidate memories from local DB
        query_terms = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
        
        mem_query = db.query(MemoryItem)
        if equipment_id:
            mem_query = mem_query.filter(MemoryItem.entity_id == equipment_id)
        if site_id:
            mem_query = mem_query.filter(MemoryItem.tags.contains(site_id))
        
        all_memories = mem_query.all()
        
        # Also query service records if equipment_id is present
        rec_query = db.query(ServiceRecord)
        if equipment_id:
            rec_query = rec_query.filter(ServiceRecord.equipment_id == equipment_id)
        records = rec_query.all()

        # Score memories based on keyword overlap
        scored_memories: List[tuple] = []
        for m in all_memories:
            score = 0
            text_corpus = f"{m.title} {m.content} {m.tags} {m.entity_name} {m.source_technician_name}".lower()
            for term in query_terms:
                if term in text_corpus:
                    score += 1
            if equipment_id and m.entity_id == equipment_id:
                score += 3
            if score > 0 or not query_terms:
                scored_memories.append((score, m))

        scored_memories.sort(key=lambda x: x[0], reverse=True)
        top_memories = [m for _, m in scored_memories[:6]]
        if not top_memories and all_memories:
            top_memories = all_memories[:4]

        # Build grounded evidence list
        evidence: List[Dict[str, Any]] = []
        for m in top_memories:
            evidence.append({
                "memory_id": m.id,
                "title": m.title,
                "content": m.content,
                "entity_name": m.entity_name,
                "memory_type": m.memory_type,
                "source_technician_name": m.source_technician_name,
                "timestamp": m.timestamp,
                "outcome_status": m.outcome_status,
                "confidence": float(m.confidence or 0.92),
                "why_matched": f"Matched organizational memory for query '{query}'"
            })

        # Synthesize grounded answer
        if hindsight_result.get("hindsight_available") and hindsight_result.get("reflection"):
            answer = hindsight_result["reflection"]
        elif top_memories:
            # Construct a comprehensive, grounded natural language synthesis
            findings = []
            obs_list = []
            fails = []
            successes = []

            for m in top_memories:
                if "OBSERVATION" in m.memory_type:
                    obs_list.append(f"Technician {m.source_technician_name} recorded on {m.timestamp}: \"{m.content}\"")
                elif "FAILED" in m.memory_type:
                    fails.append(f"Past unsuccessful attempt on {m.timestamp}: \"{m.title}\" — {m.content}")
                elif "SUCCESSFUL" in m.memory_type:
                    successes.append(f"Effective resolution on {m.timestamp}: \"{m.title}\"")
                else:
                    findings.append(f"Recorded historical pattern: {m.title} ({m.timestamp})")

            answer_parts = []
            if equipment_id:
                answer_parts.append(f"Memory analysis for equipment {top_memories[0].entity_name} ({equipment_id}):")
            else:
                answer_parts.append("Organizational memory retrieval across field operations:")

            if obs_list:
                answer_parts.append("\n• TECHNICIAN OBSERVATIONS:\n  " + "\n  ".join(obs_list[:3]))
            if fails:
                answer_parts.append("\n• PREVIOUSLY FAILED / TEMPORARY FIXES:\n  " + "\n  ".join(fails[:2]))
            if successes:
                answer_parts.append("\n• PREVIOUSLY SUCCESSFUL ACTIONS:\n  " + "\n  ".join(successes[:2]))
            if findings and not (obs_list or fails or successes):
                answer_parts.append("\n• HISTORICAL PATTERNS:\n  " + "\n  ".join(findings[:3]))

            answer_parts.append(
                "\nRECOMMENDATION: Review the underlying evidence cards below before deciding on parts or actions. "
                "Do not repeat actions that previously resulted in temporary fixes without verifying the underlying root cause."
            )
            answer = "\n".join(answer_parts)
        else:
            answer = (
                f"No specific previous memories were found matching '{query}'. "
                "This may indicate a novel condition. Once a service visit is completed, "
                "the technician's notes and diagnostic actions will be retained in Hindsight for future reference."
            )

        return {
            "answer": answer,
            "evidence": evidence,
        }

    @staticmethod
    def _empty_context(message: str, hindsight_available: bool) -> Dict[str, Any]:
        return {
            "has_seen_before": False,
            "recurrence_count": 0,
            "summary": message,
            "what_the_memory_says": message,
            "previously_tried": [],
            "previously_failed": [],
            "previously_successful": [],
            "technician_observations": [],
            "historical_outcomes": [],
            "suggested_investigation": [],
            "evidence": [],
            "hindsight_engine_info": {
                "bank_id": hindsight_service.BANK_ID,
                "recall_strategy": "none",
                "memories_retrieved": 0,
                "local_memories_retrieved": 0,
                "hindsight_available": hindsight_available,
            },
        }


# Module-level singleton
agent_service = AgentService()

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# Service Request Schemas
class ServiceRequestCreate(BaseModel):
    title: str
    reported_symptoms: str
    equipment_id: str
    site_id: str
    customer_id: str
    technician_id: Optional[str] = None
    priority: str = "Medium"

class ServiceRequestAssign(BaseModel):
    technician_id: str

class ServiceVisitSubmit(BaseModel):
    service_request_id: str
    equipment_id: str
    technician_id: str
    technician_name: str
    visit_date: str
    symptoms_observed: str
    diagnostic_tests: str = ""
    action_taken: str
    parts_replaced: str = ""
    outcome: str  # Resolved, Temporarily Resolved, Unresolved, Requires Escalation
    effective_duration_days: Optional[int] = None
    technician_notes: str = ""
    retain_as_memory: bool = True

# Hindsight Memory Schemas
class RetainMemoryRequest(BaseModel):
    bank_id: Optional[str] = None
    content: str
    context: Optional[str] = None
    entity_id: str
    entity_type: str  # equipment, site, customer, technician
    entity_name: Optional[str] = ""
    memory_type: str  # EQUIPMENT_RECURRENCE, FAILED_FIX, SUCCESSFUL_FIX, TECHNICIAN_OBSERVATION, SITE_ENVIRONMENTAL
    source_incident_id: Optional[str] = None
    source_technician_name: Optional[str] = None
    tags: List[str] = []
    outcome_status: Optional[str] = ""

class RecallMemoryQuery(BaseModel):
    query: str
    equipment_id: Optional[str] = None
    site_id: Optional[str] = None
    customer_id: Optional[str] = None
    tags: Optional[List[str]] = None
    max_tokens: int = 4096
    budget: str = "mid"
    min_confidence: float = 0.5

class ReflectMemoryQuery(BaseModel):
    query: str
    equipment_id: Optional[str] = None
    site_id: Optional[str] = None
    budget: str = "low"
    context: Optional[str] = None

class AskMemoryRequest(BaseModel):
    query: str
    equipment_id: Optional[str] = None
    site_id: Optional[str] = None

# Response structures
class MemoryEvidenceItem(BaseModel):
    memory_id: str
    title: str
    content: str
    entity_id: str
    entity_name: str
    memory_type: str
    source_technician_name: str
    timestamp: str
    outcome_status: str
    confidence: float
    why_matched: str

class AgentContextResponse(BaseModel):
    has_seen_before: bool
    recurrence_count: int
    summary: str
    what_the_memory_says: str
    previously_tried: List[Dict[str, Any]]
    previously_failed: List[Dict[str, Any]]
    previously_successful: List[Dict[str, Any]]
    technician_observations: List[Dict[str, Any]]
    historical_outcomes: List[str]
    suggested_investigation: List[str]
    evidence: List[MemoryEvidenceItem]
    hindsight_engine_info: Dict[str, Any]

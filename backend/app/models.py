from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    industry = Column(String(100), nullable=False)
    contact_name = Column(String(100), default="")
    contact_email = Column(String(150), default="")
    phone = Column(String(50), default="")
    sla_level = Column(String(50), default="Standard")  # Platinum, Gold, Silver
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    sites = relationship("Site", back_populates="customer", cascade="all, delete-orphan")
    equipment = relationship("Equipment", back_populates="customer")
    service_requests = relationship("ServiceRequest", back_populates="customer")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "industry": self.industry,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
            "phone": self.phone,
            "sla_level": self.sla_level,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "sites_count": len(self.sites) if self.sites else 0
        }

class Site(Base):
    __tablename__ = "sites"
    
    id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey("customers.id"), nullable=False)
    name = Column(String(200), nullable=False)
    address = Column(String(250), default="")
    city = Column(String(100), default="")
    state = Column(String(100), default="")
    operating_environment = Column(String(200), default="Standard Industrial")
    access_constraints = Column(Text, default="")
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    customer = relationship("Customer", back_populates="sites")
    equipment = relationship("Equipment", back_populates="site", cascade="all, delete-orphan")
    service_requests = relationship("ServiceRequest", back_populates="site")

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer_name": self.customer.name if self.customer else "",
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "operating_environment": self.operating_environment,
            "access_constraints": self.access_constraints,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "equipment_count": len(self.equipment) if self.equipment else 0
        }

class Equipment(Base):
    __tablename__ = "equipment"
    
    id = Column(String(50), primary_key=True, index=True)
    site_id = Column(String(50), ForeignKey("sites.id"), nullable=False)
    customer_id = Column(String(50), ForeignKey("customers.id"), nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)  # HVAC, Compressor, Industrial Pump, Boiler, Turbine, Hydraulic
    model = Column(String(150), default="")
    serial_number = Column(String(100), default="")
    installation_date = Column(String(50), default="")
    status = Column(String(50), default="Operational")  # Operational, Degraded Performance, Under Service, Critical
    criticality = Column(String(50), default="Medium")  # Critical, High, Medium, Low
    operating_hours = Column(Integer, default=0)
    last_service_date = Column(String(50), default="")
    notes = Column(Text, default="")
    
    customer = relationship("Customer", back_populates="equipment")
    site = relationship("Site", back_populates="equipment")
    service_requests = relationship("ServiceRequest", back_populates="equipment")
    service_records = relationship("ServiceRecord", back_populates="equipment")

    def to_dict(self):
        return {
            "id": self.id,
            "site_id": self.site_id,
            "site_name": self.site.name if self.site else "",
            "customer_id": self.customer_id,
            "customer_name": self.customer.name if self.customer else "",
            "name": self.name,
            "category": self.category,
            "model": self.model,
            "serial_number": self.serial_number,
            "installation_date": self.installation_date,
            "status": self.status,
            "criticality": self.criticality,
            "operating_hours": self.operating_hours,
            "last_service_date": self.last_service_date,
            "notes": self.notes,
            "incident_count": len(self.service_requests) if self.service_requests else 0
        }

class Technician(Base):
    __tablename__ = "technicians"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    role = Column(String(100), default="Field Service Engineer")
    email = Column(String(150), default="")
    phone = Column(String(50), default="")
    skills = Column(Text, default="")
    years_experience = Column(Integer, default=5)
    active_tickets = Column(Integer, default=0)
    avatar = Column(String(255), default="")
    
    service_requests = relationship("ServiceRequest", back_populates="technician")
    service_records = relationship("ServiceRecord", back_populates="technician")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "email": self.email,
            "phone": self.phone,
            "skills": [s.strip() for s in self.skills.split(",") if s.strip()] if self.skills else [],
            "years_experience": self.years_experience,
            "active_tickets": self.active_tickets,
            "avatar": self.avatar
        }

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    
    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    reported_symptoms = Column(Text, nullable=False)
    equipment_id = Column(String(50), ForeignKey("equipment.id"), nullable=False)
    site_id = Column(String(50), ForeignKey("sites.id"), nullable=False)
    customer_id = Column(String(50), ForeignKey("customers.id"), nullable=False)
    technician_id = Column(String(50), ForeignKey("technicians.id"), nullable=True)
    priority = Column(String(50), default="Medium")  # Critical, High, Medium, Low
    status = Column(String(50), default="Open")  # Open, Assigned, In Progress, Resolved
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime, nullable=True)
    is_demo_trigger = Column(Boolean, default=False)
    
    equipment = relationship("Equipment", back_populates="service_requests")
    site = relationship("Site", back_populates="service_requests")
    customer = relationship("Customer", back_populates="service_requests")
    technician = relationship("Technician", back_populates="service_requests")
    service_records = relationship("ServiceRecord", back_populates="service_request")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "reported_symptoms": self.reported_symptoms,
            "equipment_id": self.equipment_id,
            "equipment_name": self.equipment.name if self.equipment else "",
            "equipment_category": self.equipment.category if self.equipment else "",
            "equipment_model": self.equipment.model if self.equipment else "",
            "site_id": self.site_id,
            "site_name": self.site.name if self.site else "",
            "customer_id": self.customer_id,
            "customer_name": self.customer.name if self.customer else "",
            "technician_id": self.technician_id,
            "technician_name": self.technician.name if self.technician else "Unassigned",
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "is_demo_trigger": bool(self.is_demo_trigger),
            "records_count": len(self.service_records) if self.service_records else 0
        }

class ServiceRecord(Base):
    __tablename__ = "service_records"
    
    id = Column(String(50), primary_key=True, index=True)
    service_request_id = Column(String(50), ForeignKey("service_requests.id"), nullable=True)
    equipment_id = Column(String(50), ForeignKey("equipment.id"), nullable=False)
    technician_id = Column(String(50), ForeignKey("technicians.id"), nullable=False)
    technician_name = Column(String(150), nullable=False)
    visit_date = Column(String(50), nullable=False)  # ISO Date String
    symptoms_observed = Column(Text, nullable=False)
    diagnostic_tests = Column(Text, default="")
    action_taken = Column(Text, nullable=False)
    parts_replaced = Column(String(255), default="")
    outcome = Column(String(50), nullable=False)  # Resolved, Temporarily Resolved, Unresolved, Requires Escalation
    effective_duration_days = Column(Integer, nullable=True)  # Days before issue re-occurred (null if permanent)
    technician_notes = Column(Text, default="")
    memory_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    service_request = relationship("ServiceRequest", back_populates="service_records")
    equipment = relationship("Equipment", back_populates="service_records")
    technician = relationship("Technician", back_populates="service_records")

    def to_dict(self):
        return {
            "id": self.id,
            "service_request_id": self.service_request_id,
            "equipment_id": self.equipment_id,
            "equipment_name": self.equipment.name if self.equipment else "",
            "technician_id": self.technician_id,
            "technician_name": self.technician_name,
            "visit_date": self.visit_date,
            "symptoms_observed": self.symptoms_observed,
            "diagnostic_tests": self.diagnostic_tests,
            "action_taken": self.action_taken,
            "parts_replaced": self.parts_replaced,
            "outcome": self.outcome,
            "effective_duration_days": self.effective_duration_days,
            "technician_notes": self.technician_notes,
            "memory_id": self.memory_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class MemoryItem(Base):
    __tablename__ = "memory_items"
    
    id = Column(String(100), primary_key=True, index=True)
    bank_id = Column(String(100), default="field-service-org-memory", index=True)
    memory_type = Column(String(100), nullable=False)  # EQUIPMENT_RECURRENCE, FAILED_FIX, SUCCESSFUL_FIX, TECHNICIAN_OBSERVATION, SITE_ENVIRONMENTAL, CUSTOMER_PREFERENCE
    entity_type = Column(String(50), nullable=False)  # equipment, site, customer, technician, incident
    entity_id = Column(String(100), nullable=False, index=True)
    entity_name = Column(String(200), default="")
    title = Column(String(250), nullable=False)
    content = Column(Text, nullable=False)
    context = Column(Text, default="")
    source_incident_id = Column(String(50), nullable=True)
    source_technician_name = Column(String(150), default="")
    tags = Column(Text, default="")  # comma separated
    timestamp = Column(String(50), default="")
    confidence = Column(Float, default=0.92)
    recall_count = Column(Integer, default=0)
    recurrence_flag = Column(Boolean, default=False)
    outcome_status = Column(String(50), default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "bank_id": self.bank_id,
            "memory_type": self.memory_type,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "title": self.title,
            "content": self.content,
            "context": self.context,
            "source_incident_id": self.source_incident_id,
            "source_technician_name": self.source_technician_name,
            "tags": [t.strip() for t in self.tags.split(",") if t.strip()] if self.tags else [],
            "timestamp": self.timestamp,
            "confidence": self.confidence,
            "recall_count": self.recall_count,
            "recurrence_flag": bool(self.recurrence_flag),
            "outcome_status": self.outcome_status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

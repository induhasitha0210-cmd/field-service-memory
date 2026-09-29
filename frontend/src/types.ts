export interface Customer {
  id: string;
  name: string;
  industry: string;
  contact_name: string;
  contact_email?: string;
  phone?: string;
  sla_level: string;
  notes?: string;
  sites_count: number;
}

export interface Site {
  id: string;
  customer_id: string;
  customer_name: string;
  name: string;
  city: string;
  state?: string;
  address?: string;
  operating_environment: string;
  access_constraints?: string;
  equipment_count: number;
}

export interface Equipment {
  id: string;
  name: string;
  category: string;
  model: string;
  serial_number?: string;
  site_id?: string;
  site_name: string;
  customer_id?: string;
  customer_name: string;
  status: string;
  criticality: string;
  installation_date: string;
  last_service_date: string;
  incident_count: number;
  operating_hours: number;
  notes?: string;
  service_history_count?: number;
  active_requests?: ServiceRequest[];
}

export interface Technician {
  id: string;
  name: string;
  role: string;
  email?: string;
  phone?: string;
  skills: string[];
  years_experience: number;
  active_tickets: number;
  avatar?: string;
  assigned_requests?: ServiceRequest[];
  recent_records?: ServiceRecord[];
}

export interface ServiceRequest {
  id: string;
  title: string;
  reported_symptoms: string;
  equipment_id: string;
  equipment_name: string;
  equipment_category: string;
  equipment_model: string;
  site_id?: string;
  site_name: string;
  customer_id?: string;
  customer_name: string;
  technician_id?: string | null;
  technician_name: string | null;
  priority: string;
  status: string;
  created_at: string;
  resolved_at?: string | null;
  is_demo_trigger?: boolean;
  records_count?: number;
  records?: ServiceRecord[];
}

export interface ServiceRecord {
  id: string;
  service_request_id?: string | null;
  equipment_id?: string;
  equipment_name?: string;
  technician_id?: string;
  technician_name: string;
  visit_date: string;
  symptoms_observed: string;
  diagnostic_tests?: string;
  action_taken: string;
  parts_replaced?: string;
  outcome: string;
  effective_duration_days: number | null;
  technician_notes: string;
  memory_id?: string | null;
}

export interface MemoryItem {
  id: string;
  bank_id?: string;
  memory_type: string;
  entity_type: string;
  entity_id: string;
  entity_name: string;
  title: string;
  content: string;
  context?: string;
  source_incident_id?: string | null;
  source_technician_name?: string | null;
  tags?: string[];
  timestamp: string;
  confidence: number;
  recall_count?: number;
  recurrence_flag?: boolean;
  outcome_status?: string | null;
}

export interface MemoryEvidence {
  memory_id: string;
  title: string;
  content: string;
  entity_name: string;
  memory_type: string;
  source_technician_name?: string | null;
  timestamp: string;
  outcome_status?: string | null;
  confidence: number;
  why_matched: string;
  source?: string;
}

export interface AgentContext {
  has_seen_before: boolean;
  recurrence_count: number;
  summary: string;
  what_the_memory_says: string;
  previously_tried: Array<{ action: string; outcome?: string; date?: string; technician?: string; parts_replaced?: string }>;
  previously_failed: Array<{ action: string; reason: string; date?: string }>;
  previously_successful: Array<{ action: string; duration_days?: number | null; date?: string; technician?: string }>;
  technician_observations: Array<{ technician: string; observation: string; date?: string }>;
  historical_outcomes: string[];
  suggested_investigation: string[];
  evidence: MemoryEvidence[];
  hindsight_engine_info: {
    bank_id: string;
    hindsight_available: boolean;
    memories_retrieved: number;
    recall_strategy: string;
    local_memories_retrieved?: number;
  };
}

export interface TimelineEvent {
  id: string;
  date: string;
  title: string;
  description: string;
  technician: string | null;
  outcome: string | null;
  event_type: string;
}

export interface Insight {
  recurring_issues: Array<{
    equipment_id: string;
    equipment_name: string;
    category?: string;
    site_name: string;
    customer_name: string;
    total_visits: number;
    unresolved_count: number;
    temporary_count: number;
  }>;
  failed_temporary_fixes: Array<{
    equipment_name: string;
    action_taken: string;
    outcome: string;
    count: number;
  }>;
  high_activity_sites: Array<{
    site_name: string;
    customer_name: string;
    incident_count: number;
  }>;
  equipment_requiring_attention: Array<{
    id: string;
    name: string;
    category?: string;
    site_name: string;
    customer_name: string;
    status: string;
    criticality: string;
    last_service_date: string;
    incident_count: number;
  }>;
  memory_knowledge_base: {
    total_memories: number;
    equipment_patterns: number;
    resolved_cases: number;
    unresolved_cases: number;
    technician_observations: number;
  };
  active_requests: number;
  technicians_deployed: number;
  sites_with_activity: number;
}

export interface MemoryStats {
  total_memories: number;
  memories_by_type: Record<string, number>;
  memories_retrieved_today: number;
  hindsight_available: boolean;
  bank_id?: string;
  mode?: string;
}

export interface DemoStep {
  step: number;
  title: string;
  description: string;
  data?: Record<string, any>;
}

export interface DemoResult {
  success: boolean;
  steps: DemoStep[];
  service_request_id?: string;
  agent_context?: AgentContext;
  target_equipment?: Equipment;
  message?: string;
}

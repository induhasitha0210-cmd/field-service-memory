import type { AgentContext, DemoResult, MemoryItem, Equipment, ServiceRequest, ServiceRecord, Customer, Site, Technician, Insight, MemoryStats, TimelineEvent } from './types';

const BASE = '/api';

async function req<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(BASE + url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  // Dashboard / Insights
  getInsights: () => req<Insight>('/insights'),
  getMemoryStats: () => req<MemoryStats>('/memory/stats'),
  getHindsightStatus: () => req<{ hindsight_available: boolean; bank_id: string; mode: string }>('/memory/status'),

  // Service Requests
  getServiceRequests: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : '';
    return req<ServiceRequest[]>(`/service-requests${qs}`);
  },
  getServiceRequest: (id: number | string) => req<ServiceRequest>(`/service-requests/${id}`),
  getServiceRequestContext: (id: number | string) => req<AgentContext>(`/service-requests/${id}/context`),
  assignTechnician: (id: number | string, techId: number) =>
    req<ServiceRequest>(`/service-requests/${id}/assign`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ technician_id: techId }),
    }),
  completeServiceVisit: (id: number | string, data: Record<string, unknown>) =>
    req<ServiceRecord>(`/service-requests/${id}/complete`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }),
  createServiceRequest: (data: Record<string, unknown>) =>
    req<ServiceRequest>('/service-requests', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }),

  // Equipment
  getEquipment: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : '';
    return req<Equipment[]>(`/equipment${qs}`);
  },
  getEquipmentById: (id: number | string) => req<Equipment>(`/equipment/${id}`),
  getEquipmentHistory: (id: number | string) => req<ServiceRecord[]>(`/equipment/${id}/history`),
  getEquipmentMemories: (id: number | string) => req<MemoryItem[]>(`/equipment/${id}/memories`),
  getEquipmentTimeline: (id: number | string) => req<TimelineEvent[]>(`/equipment/${id}/timeline`),

  // Customers
  getCustomers: () => req<Customer[]>('/customers'),
  getCustomerById: (id: number | string) => req<Customer>(`/customers/${id}`),

  // Sites
  getSites: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : '';
    return req<Site[]>(`/sites${qs}`);
  },

  // Technicians
  getTechnicians: () => req<Technician[]>('/technicians'),

  // Memory
  getMemories: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : '';
    return req<MemoryItem[]>(`/memory${qs}`);
  },
  askMemory: (query: string, equipment_id?: number, site_id?: number) =>
    req<{ answer: string; evidence: import('./types').MemoryEvidence[] }>('/memory/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, equipment_id, site_id }),
    }),

  // Demo
  runDemo: () => req<DemoResult>('/demo/run', { method: 'POST' }),
};

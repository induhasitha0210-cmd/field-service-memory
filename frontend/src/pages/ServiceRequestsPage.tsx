import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Ticket,
  Plus,
  Search,
  Filter,
  Wrench,
  Clock,
  CheckCircle,
  AlertTriangle,
  UserCheck,
  Building2,
  MapPin,
  X,
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';
import type { ServiceRequest, Equipment, Customer, Site, Technician } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';

export default function ServiceRequestsPage() {
  const navigate = useNavigate();
  const [requests, setRequests] = useState<ServiceRequest[]>([]);
  const [equipments, setEquipments] = useState<Equipment[]>([]);
  const [technicians, setTechnicians] = useState<Technician[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [statusFilter, setStatusFilter] = useState('All');
  const [priorityFilter, setPriorityFilter] = useState('All');
  const [search, setSearch] = useState('');

  // New Request Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newSymptoms, setNewSymptoms] = useState('');
  const [newEquipId, setNewEquipId] = useState('');
  const [newPriority, setNewPriority] = useState('High');
  const [newTechId, setNewTechId] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadRequests();
    // Load equipment and technicians for create modal
    Promise.all([api.getEquipment(), api.getTechnicians()])
      .then(([eqs, techs]) => {
        setEquipments(eqs);
        setTechnicians(techs);
        if (eqs.length > 0) setNewEquipId(eqs[0].id);
      })
      .catch(() => {});
  }, []);

  async function loadRequests() {
    try {
      setLoading(true);
      const data = await api.getServiceRequests();
      setRequests(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load service requests');
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateRequest(e: React.FormEvent) {
    e.preventDefault();
    if (!newTitle.trim() || !newSymptoms.trim() || !newEquipId) return;

    try {
      setSubmitting(true);
      const targetEq = equipments.find((eq) => eq.id === newEquipId);
      const newSr = await api.createServiceRequest({
        title: newTitle,
        reported_symptoms: newSymptoms,
        equipment_id: newEquipId,
        site_id: targetEq?.site_id || '',
        customer_id: targetEq?.customer_id || '',
        technician_id: newTechId || null,
        priority: newPriority,
      });
      setIsModalOpen(false);
      setNewTitle('');
      setNewSymptoms('');
      // Navigate straight to the technician workspace for this newly created request!
      navigate(`/service-requests/${newSr.id}`);
    } catch (err: any) {
      alert(`Error creating service request: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  }

  const filteredRequests = requests.filter((r) => {
    if (statusFilter !== 'All' && r.status !== statusFilter) return false;
    if (priorityFilter !== 'All' && r.priority !== priorityFilter) return false;
    if (search.trim()) {
      const q = search.toLowerCase();
      const match =
        r.id.toLowerCase().includes(q) ||
        r.title.toLowerCase().includes(q) ||
        r.equipment_name.toLowerCase().includes(q) ||
        r.customer_name.toLowerCase().includes(q) ||
        r.site_name.toLowerCase().includes(q) ||
        (r.technician_name && r.technician_name.toLowerCase().includes(q));
      if (!match) return false;
    }
    return true;
  });

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorState message={error} onRetry={loadRequests} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Ticket className="w-6 h-6 text-sky-400" />
            <span>Service Requests</span>
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Dispatch, assign, and open the Hindsight-backed Technician Workspace for any incident.
          </p>
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2 px-4 py-2 bg-sky-500 hover:bg-sky-400 text-white rounded-xl text-sm font-semibold shadow-md shadow-sky-500/20 transition-all self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>New Service Request</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex flex-col md:flex-row gap-4 justify-between items-stretch md:items-center">
        {/* Search */}
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by ticket #, equipment, site, customer, symptoms..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <Filter className="w-3.5 h-3.5" />
            <span>Status:</span>
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
          >
            <option value="All">All Statuses</option>
            <option value="Open">Open</option>
            <option value="Assigned">Assigned</option>
            <option value="In Progress">In Progress</option>
            <option value="Resolved">Resolved</option>
          </select>

          <span className="text-slate-700">|</span>

          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <span>Priority:</span>
          </div>
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
          >
            <option value="All">All Priorities</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>
      </div>

      {/* Requests List */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div className="divide-y divide-slate-800">
          {filteredRequests.length === 0 ? (
            <div className="p-12 text-center text-slate-500 text-sm">
              No service requests match the selected filters.
            </div>
          ) : (
            filteredRequests.map((sr) => (
              <div
                key={sr.id}
                className="p-5 hover:bg-slate-800/40 transition-colors flex flex-col lg:flex-row lg:items-center justify-between gap-4"
              >
                {/* Left block */}
                <div className="space-y-2 flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-mono text-xs font-bold text-sky-400">
                      #{sr.id}
                    </span>
                    <span
                      className={clsx(
                        'px-2 py-0.5 rounded text-[10px] font-semibold uppercase',
                        sr.priority === 'Critical'
                          ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                          : sr.priority === 'High'
                          ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          : 'bg-slate-800 text-slate-300'
                      )}
                    >
                      {sr.priority}
                    </span>
                    <span
                      className={clsx(
                        'px-2 py-0.5 rounded text-[10px] font-semibold',
                        sr.status === 'Resolved'
                          ? 'bg-emerald-500/20 text-emerald-400'
                          : sr.status === 'Assigned'
                          ? 'bg-sky-500/20 text-sky-400'
                          : 'bg-amber-500/20 text-amber-400'
                      )}
                    >
                      {sr.status}
                    </span>
                    {sr.is_demo_trigger && (
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        Demo Trigger
                      </span>
                    )}
                  </div>

                  <h3 className="text-base font-semibold text-slate-100">
                    {sr.title}
                  </h3>

                  <p className="text-xs text-slate-400 leading-relaxed line-clamp-2">
                    {sr.reported_symptoms}
                  </p>

                  <div className="flex items-center gap-4 text-xs text-slate-400 flex-wrap pt-1">
                    <div className="flex items-center gap-1.5">
                      <Wrench className="w-3.5 h-3.5 text-slate-500" />
                      <span className="text-slate-200 font-medium">{sr.equipment_name}</span>
                      <span className="text-slate-500">({sr.equipment_category})</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <Building2 className="w-3.5 h-3.5 text-slate-500" />
                      <span>{sr.customer_name}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <MapPin className="w-3.5 h-3.5 text-slate-500" />
                      <span>{sr.site_name}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <UserCheck className="w-3.5 h-3.5 text-slate-500" />
                      <span>
                        Tech: {sr.technician_name ? (
                          <span className="text-slate-200">{sr.technician_name}</span>
                        ) : (
                          <span className="text-amber-500/80 italic">Unassigned</span>
                        )}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Right button */}
                <div className="flex items-center gap-3 self-end lg:self-center flex-shrink-0">
                  <button
                    onClick={() => navigate(`/service-requests/${sr.id}`)}
                    className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white rounded-xl text-xs font-semibold shadow-md transition-all"
                  >
                    <Wrench className="w-3.5 h-3.5" />
                    <span>Open Technician Workspace</span>
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Modal: Create New Service Request */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full overflow-hidden shadow-2xl">
            <div className="p-5 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Ticket className="w-5 h-5 text-sky-400" />
                <h2 className="text-base font-bold text-white">Create Service Request</h2>
              </div>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateRequest} className="p-5 space-y-4 text-xs">
              <div>
                <label className="block text-slate-300 font-medium mb-1">Issue Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Unit overheating after continuous run..."
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-sky-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Reported Symptoms</label>
                <textarea
                  required
                  rows={3}
                  placeholder="Describe symptoms, alarms, unusual noises, temperature spikes..."
                  value={newSymptoms}
                  onChange={(e) => setNewSymptoms(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-sky-500"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-slate-300 font-medium mb-1">Target Equipment</label>
                  <select
                    value={newEquipId}
                    onChange={(e) => setNewEquipId(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-sky-500"
                  >
                    {equipments.map((eq) => (
                      <option key={eq.id} value={eq.id}>
                        {eq.name} ({eq.category})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">Priority</label>
                  <select
                    value={newPriority}
                    onChange={(e) => setNewPriority(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-sky-500"
                  >
                    <option value="Critical">Critical</option>
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Assign Technician (Optional)</label>
                <select
                  value={newTechId}
                  onChange={(e) => setNewTechId(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-sky-500"
                >
                  <option value="">Leave Unassigned</option>
                  {technicians.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.name} ({t.role})
                    </option>
                  ))}
                </select>
              </div>

              <div className="pt-3 border-t border-slate-800 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-5 py-2 bg-sky-500 hover:bg-sky-400 text-white font-semibold rounded-xl disabled:opacity-50"
                >
                  {submitting ? 'Creating...' : 'Submit & Analyze Memory'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

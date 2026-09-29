import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  Ticket,
  Wrench,
  Building2,
  MapPin,
  Clock,
  UserCheck,
  CheckCircle,
  AlertTriangle,
  ArrowLeft,
  Brain,
  Database,
  History,
  Send,
  Zap,
  Check,
  ShieldCheck,
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';
import type { ServiceRequest, AgentContext, ServiceRecord, Technician } from '../types';
import AgentInsightCard from '../components/AgentInsightCard';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';

export default function ServiceRequestDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [request, setRequest] = useState<ServiceRequest | null>(null);
  const [context, setContext] = useState<AgentContext | null>(null);
  const [history, setHistory] = useState<ServiceRecord[]>([]);
  const [technicians, setTechnicians] = useState<Technician[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Assignment state
  const [assigneeId, setAssigneeId] = useState('');
  const [assigning, setAssigning] = useState(false);

  // Technician Visit Action Form state
  const [symptomsObserved, setSymptomsObserved] = useState('');
  const [diagnosticTests, setDiagnosticTests] = useState('');
  const [actionTaken, setActionTaken] = useState('');
  const [partsReplaced, setPartsReplaced] = useState('');
  const [outcome, setOutcome] = useState('Resolved');
  const [effectiveDuration, setEffectiveDuration] = useState<string>('');
  const [technicianNotes, setTechnicianNotes] = useState('');
  const [retainMemory, setRetainMemory] = useState(true);
  const [submittingVisit, setSubmittingVisit] = useState(false);
  const [completionNotice, setCompletionNotice] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadData(id);
    }
  }, [id]);

  async function loadData(srId: string) {
    try {
      setLoading(true);
      setError(null);
      const [sr, ctx, techs] = await Promise.all([
        api.getServiceRequest(srId),
        api.getServiceRequestContext(srId),
        api.getTechnicians(),
      ]);
      setRequest(sr);
      setContext(ctx);
      setTechnicians(techs);
      setAssigneeId(sr.technician_id || '');

      // Load past records for this equipment
      if (sr.equipment_id) {
        const past = await api.getEquipmentHistory(sr.equipment_id);
        setHistory(past);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load technician workspace');
    } finally {
      setLoading(false);
    }
  }

  async function handleAssignTechnician() {
    if (!id || !assigneeId) return;
    try {
      setAssigning(true);
      await api.assignTechnician(id, assigneeId as any);
      const updated = await api.getServiceRequest(id);
      setRequest(updated);
    } catch (err: any) {
      alert(`Assignment failed: ${err.message}`);
    } finally {
      setAssigning(false);
    }
  }

  async function handleSubmitVisit(e: React.FormEvent) {
    e.preventDefault();
    if (!id || !request) return;
    if (!actionTaken.trim() || !symptomsObserved.trim()) {
      alert('Please enter observed symptoms and action taken.');
      return;
    }

    try {
      setSubmittingVisit(true);
      const selectedTech = technicians.find((t) => t.id === assigneeId) || technicians[0];
      const payload = {
        service_request_id: id,
        equipment_id: request.equipment_id,
        technician_id: selectedTech?.id || 'TECH-001',
        technician_name: selectedTech?.name || 'Technician',
        visit_date: new Date().toISOString().split('T')[0],
        symptoms_observed: symptomsObserved,
        diagnostic_tests: diagnosticTests,
        action_taken: actionTaken,
        parts_replaced: partsReplaced,
        outcome: outcome,
        effective_duration_days: effectiveDuration ? parseInt(effectiveDuration, 10) : null,
        technician_notes: technicianNotes,
        retain_as_memory: retainMemory,
      };

      await api.completeServiceVisit(id, payload);

      setCompletionNotice(
        `Service visit recorded successfully! ${
          retainMemory
            ? 'New organizational memory retained in Hindsight for future technicians.'
            : ''
        }`
      );

      // Reload data to reflect new state
      await loadData(id);

      // Reset form
      setSymptomsObserved('');
      setDiagnosticTests('');
      setActionTaken('');
      partsReplaced && setPartsReplaced('');
      technicianNotes && setTechnicianNotes('');
    } catch (err: any) {
      alert(`Failed to complete visit: ${err.message}`);
    } finally {
      setSubmittingVisit(false);
    }
  }

  if (loading) return <LoadingSpinner />;
  if (error || !request) return <ErrorState message={error || 'Service request not found'} onRetry={() => id && loadData(id)} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Back button & Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/service-requests')}
            className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-sky-400">#{request.id}</span>
              <span
                className={clsx(
                  'px-2 py-0.5 rounded text-[10px] font-semibold uppercase',
                  request.priority === 'Critical'
                    ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                    : request.priority === 'High'
                    ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                    : 'bg-slate-800 text-slate-300'
                )}
              >
                {request.priority}
              </span>
              <span
                className={clsx(
                  'px-2 py-0.5 rounded text-[10px] font-semibold',
                  request.status === 'Resolved'
                    ? 'bg-emerald-500/20 text-emerald-400'
                    : 'bg-sky-500/20 text-sky-400'
                )}
              >
                {request.status}
              </span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight mt-1">
              Technician Workspace: {request.title}
            </h1>
          </div>
        </div>

        {/* Link to equipment timeline */}
        <Link
          to={`/equipment/${request.equipment_id}`}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium transition-colors self-start sm:self-auto"
        >
          <History className="w-3.5 h-3.5 text-sky-400" />
          <span>View Equipment History</span>
        </Link>
      </div>

      {/* Completion notice alert banner */}
      {completionNotice && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-between gap-3 text-emerald-400 text-xs">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 flex-shrink-0" />
            <span className="font-medium">{completionNotice}</span>
          </div>
          <button
            onClick={() => setCompletionNotice(null)}
            className="text-emerald-400/80 hover:text-emerald-300"
          >
            ✕
          </button>
        </div>
      )}

      {/* Header Info Card */}
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
        <div className="space-y-1">
          <span className="text-slate-500 font-medium">Customer</span>
          <p className="text-slate-200 font-semibold text-sm">{request.customer_name}</p>
        </div>

        <div className="space-y-1">
          <span className="text-slate-500 font-medium">Site</span>
          <p className="text-slate-200 font-semibold text-sm">{request.site_name}</p>
        </div>

        <div className="space-y-1">
          <span className="text-slate-500 font-medium">Target Equipment</span>
          <p className="text-slate-200 font-semibold text-sm flex items-center gap-1.5">
            <Wrench className="w-3.5 h-3.5 text-sky-400" />
            <span>{request.equipment_name}</span>
            <span className="text-slate-500 text-xs">({request.equipment_category})</span>
          </p>
        </div>

        <div className="space-y-1">
          <span className="text-slate-500 font-medium">Assigned Field Tech</span>
          <div className="flex items-center gap-2">
            <select
              value={assigneeId}
              onChange={(e) => setAssigneeId(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-lg px-2 py-1 text-slate-200 focus:outline-none focus:border-sky-500 text-xs flex-1"
            >
              <option value="">Unassigned</option>
              {technicians.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </select>
            {assigneeId !== request.technician_id && (
              <button
                onClick={handleAssignTechnician}
                disabled={assigning}
                className="px-2 py-1 bg-sky-500 hover:bg-sky-400 text-white rounded text-[11px] font-semibold"
              >
                {assigning ? '...' : 'Save'}
              </button>
            )}
          </div>
        </div>

        {/* Symptoms block */}
        <div className="md:col-span-4 pt-3 border-t border-slate-800/80 space-y-1">
          <span className="text-slate-500 font-medium uppercase tracking-wider text-[10px]">
            Reported Symptoms
          </span>
          <p className="text-slate-200 leading-relaxed bg-slate-950/60 p-3 rounded-xl border border-slate-800 font-sans">
            {request.reported_symptoms}
          </p>
        </div>
      </div>

      {/* Main Workspace Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Hindsight Memory Context & Previous Visits (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Agent Memory Insight Card */}
          {context ? (
            <AgentInsightCard ctx={context} />
          ) : (
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-center text-slate-500 text-xs">
              Memory analysis in progress...
            </div>
          )}

          {/* Previous Visits Section */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <History className="w-4 h-4 text-sky-400" />
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">
                  Previous Visits on {request.equipment_name} ({history.length})
                </h3>
              </div>
              <span className="text-[11px] text-slate-500">Chronological service log</span>
            </div>

            <div className="divide-y divide-slate-800 max-h-[460px] overflow-y-auto">
              {history.length === 0 ? (
                <p className="p-6 text-slate-500 text-xs text-center">
                  No prior service visits recorded for this equipment.
                </p>
              ) : (
                history.map((rec, idx) => (
                  <div key={rec.id} className="p-4 space-y-2 text-xs">
                    <div className="flex items-center justify-between gap-2 flex-wrap">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-slate-300">
                          Visit #{history.length - idx}
                        </span>
                        <span className="text-slate-500">· {rec.visit_date}</span>
                        <span className="text-slate-400">by {rec.technician_name}</span>
                      </div>
                      <span
                        className={clsx(
                          'px-2 py-0.5 rounded text-[10px] font-semibold',
                          rec.outcome === 'Resolved'
                            ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                            : rec.outcome === 'Temporarily Resolved'
                            ? 'bg-amber-500/15 text-amber-400 border border-amber-500/30'
                            : 'bg-rose-500/15 text-rose-400 border border-rose-500/30'
                        )}
                      >
                        {rec.outcome}
                        {rec.effective_duration_days && (
                          <span className="ml-1 text-[9px]">({rec.effective_duration_days}d)</span>
                        )}
                      </span>
                    </div>

                    <div className="space-y-1 text-slate-300">
                      <p>
                        <span className="text-slate-500 font-medium">Symptoms: </span>
                        {rec.symptoms_observed}
                      </p>
                      <p>
                        <span className="text-slate-500 font-medium">Action Taken: </span>
                        {rec.action_taken}
                      </p>
                      {rec.parts_replaced && (
                        <p>
                          <span className="text-slate-500 font-medium">Parts: </span>
                          <span className="text-sky-400">{rec.parts_replaced}</span>
                        </p>
                      )}
                      {rec.technician_notes && (
                        <p className="italic text-slate-400 bg-slate-950/40 p-2 rounded border border-slate-800/80">
                          "{rec.technician_notes}"
                        </p>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Technician Action Form (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden sticky top-6 shadow-xl">
            <div className="p-4 border-b border-slate-800 bg-slate-950/60 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Wrench className="w-4 h-4 text-emerald-400" />
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">
                  Record Service Visit & Learn
                </h3>
              </div>
              <span className="text-[10px] text-emerald-400 font-medium bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                Live Memory Retention
              </span>
            </div>

            <form onSubmit={handleSubmitVisit} className="p-5 space-y-4 text-xs">
              <div>
                <label className="block text-slate-300 font-semibold mb-1">
                  What did you observe? *
                </label>
                <textarea
                  required
                  rows={2}
                  placeholder="Record symptoms, baseline gauge readings, sounds, vibration..."
                  value={symptomsObserved}
                  onChange={(e) => setSymptomsObserved(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">
                  What did you test? (Diagnostic Actions)
                </label>
                <input
                  type="text"
                  placeholder="e.g. Megger motor test, FFT vibration spectrum, pressure drop check..."
                  value={diagnosticTests}
                  onChange={(e) => setDiagnosticTests(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">
                  What did you do? (Action Taken) *
                </label>
                <textarea
                  required
                  rows={2}
                  placeholder="Specific mechanical, electrical, or software actions taken..."
                  value={actionTaken}
                  onChange={(e) => setActionTaken(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">
                  Parts Replaced (Optional)
                </label>
                <input
                  type="text"
                  placeholder="e.g. Bearing Assembly B-6042, Shaft Seal..."
                  value={partsReplaced}
                  onChange={(e) => setPartsReplaced(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">
                    Visit Outcome *
                  </label>
                  <select
                    value={outcome}
                    onChange={(e) => setOutcome(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-sky-500"
                  >
                    <option value="Resolved">Resolved (Permanent)</option>
                    <option value="Temporarily Resolved">Temporarily Resolved</option>
                    <option value="Unresolved">Unresolved</option>
                    <option value="Requires Escalation">Requires Escalation</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">
                    Est. Duration (Days)
                  </label>
                  <input
                    type="number"
                    placeholder="If temporary (e.g. 14)"
                    value={effectiveDuration}
                    onChange={(e) => setEffectiveDuration(e.target.value)}
                    disabled={outcome === 'Resolved'}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500 disabled:opacity-40"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">
                  Technician Notes & Observations
                </label>
                <textarea
                  rows={2}
                  placeholder="Record subtleties for the next technician (e.g. 'vibration spiked at 120Hz', 'access panel screws stripped')..."
                  value={technicianNotes}
                  onChange={(e) => setTechnicianNotes(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500"
                />
              </div>

              {/* Memory Retention Toggle */}
              <div className="p-3 bg-sky-950/20 border border-sky-500/30 rounded-xl space-y-1">
                <label className="flex items-center gap-2 text-slate-200 font-semibold cursor-pointer">
                  <input
                    type="checkbox"
                    checked={retainMemory}
                    onChange={(e) => setRetainMemory(e.target.checked)}
                    className="w-4 h-4 rounded text-sky-500 bg-slate-950 border-slate-700"
                  />
                  <span>Preserve in Hindsight Memory Bank</span>
                </label>
                <p className="text-[11px] text-slate-400 pl-6">
                  Transforms your observation and resolution into persistent organizational knowledge, so future technicians are alerted if symptoms return.
                </p>
              </div>

              <button
                type="submit"
                disabled={submittingVisit}
                className="w-full py-3 bg-gradient-to-r from-emerald-500 to-sky-600 hover:from-emerald-400 hover:to-sky-500 text-white font-bold rounded-xl shadow-lg shadow-emerald-500/10 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
              >
                <Check className="w-4 h-4" />
                <span>{submittingVisit ? 'Saving to Memory...' : 'Complete Visit & Retain Memory'}</span>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

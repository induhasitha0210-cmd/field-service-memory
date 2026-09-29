import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Brain,
  Play,
  Ticket,
  AlertTriangle,
  CheckCircle2,
  Wrench,
  Building2,
  Users,
  Database,
  ArrowRight,
  Sparkles,
  Zap,
  Clock,
  History,
  TrendingDown,
  Eye,
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';
import type { Insight, ServiceRequest, MemoryItem, MemoryStats } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [insight, setInsight] = useState<Insight | null>(null);
  const [activeRequests, setActiveRequests] = useState<ServiceRequest[]>([]);
  const [recentMemories, setRecentMemories] = useState<MemoryItem[]>([]);
  const [memoryStats, setMemoryStats] = useState<MemoryStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [ins, reqs, mems, stats] = await Promise.all([
          api.getInsights(),
          api.getServiceRequests({ status: 'Open' }),
          api.getMemories(),
          api.getMemoryStats(),
        ]);
        setInsight(ins);
        // Also include Assigned requests
        const assigned = await api.getServiceRequests({ status: 'Assigned' });
        setActiveRequests([...reqs, ...assigned].slice(0, 6));
        setRecentMemories(mems.slice(0, 5));
        setMemoryStats(stats);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* 1. Hero Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900 via-slate-900 to-sky-950/40 border border-slate-800 p-8 shadow-xl">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-96 h-96 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-3 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/20 text-sky-400 text-xs font-semibold tracking-wide">
              <Brain className="w-3.5 h-3.5" />
              <span>POWERED BY HINDSIGHT AGENT MEMORY</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              FIELD SERVICE MEMORY
            </h1>
            <p className="text-lg text-sky-300 font-medium italic">
              "The Technician Who Never Forgets."
            </p>
            <p className="text-slate-400 text-sm leading-relaxed">
              When a service visit ends, critical knowledge is preserved in Hindsight. When a new incident appears, the agent recalls past symptoms, previous failed fixes, and technician observations—guiding the next technician to the right root-cause resolution.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <button
              onClick={() => navigate('/demo')}
              className="flex items-center justify-center gap-2 px-5 py-3 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white rounded-xl text-sm font-semibold shadow-lg shadow-sky-500/20 transition-all"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>Run Memory Demo</span>
            </button>
            <button
              onClick={() => navigate('/memory')}
              className="flex items-center justify-center gap-2 px-5 py-3 bg-slate-800/80 hover:bg-slate-700/80 text-slate-200 border border-slate-700 rounded-xl text-sm font-semibold transition-all"
            >
              <Brain className="w-4 h-4 text-sky-400" />
              <span>Explore Memory</span>
            </button>
          </div>
        </div>

        {/* Memory Lifecycle visual strip */}
        <div className="mt-8 pt-6 border-t border-slate-800/80">
          <p className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-3">
            Persistent Memory Lifecycle
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2 text-center text-xs">
            <div className="bg-slate-950/60 border border-slate-800 p-2.5 rounded-lg">
              <span className="text-sky-400 font-bold block mb-1">1. Visit</span>
              <span className="text-slate-400 text-[11px]">Structured Action</span>
            </div>
            <div className="bg-slate-950/60 border border-slate-800 p-2.5 rounded-lg">
              <span className="text-sky-400 font-bold block mb-1">2. Note</span>
              <span className="text-slate-400 text-[11px]">Tech Observation</span>
            </div>
            <div className="bg-slate-950/60 border border-sky-500/30 p-2.5 rounded-lg bg-sky-950/20">
              <span className="text-sky-300 font-bold block mb-1">3. Retain</span>
              <span className="text-sky-400 text-[11px]">Hindsight Bank</span>
            </div>
            <div className="bg-slate-950/60 border border-slate-800 p-2.5 rounded-lg">
              <span className="text-amber-400 font-bold block mb-1">4. New Request</span>
              <span className="text-slate-400 text-[11px]">Future Incident</span>
            </div>
            <div className="bg-slate-950/60 border border-sky-500/30 p-2.5 rounded-lg bg-sky-950/20">
              <span className="text-sky-300 font-bold block mb-1">5. Recall</span>
              <span className="text-sky-400 text-[11px]">Multi-strategy</span>
            </div>
            <div className="bg-slate-950/60 border border-slate-800 p-2.5 rounded-lg">
              <span className="text-emerald-400 font-bold block mb-1">6. Insight</span>
              <span className="text-slate-400 text-[11px]">"Seen Before"</span>
            </div>
            <div className="bg-slate-950/60 border border-slate-800 p-2.5 rounded-lg">
              <span className="text-emerald-400 font-bold block mb-1">7. Learn</span>
              <span className="text-slate-400 text-[11px]">New Outcome</span>
            </div>
          </div>
        </div>
      </div>

      {/* 2. Key Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Active Requests</span>
            <Ticket className="w-4 h-4 text-sky-400" />
          </div>
          <p className="text-2xl font-bold text-white">{insight?.active_requests ?? 0}</p>
          <span className="text-[11px] text-sky-400 font-medium">Requiring dispatch</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Recurring Issues</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">
            {insight?.recurring_issues?.length ?? 0}
          </p>
          <span className="text-[11px] text-amber-500/80 font-medium">Repeated failures</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Sites with Issues</span>
            <Building2 className="w-4 h-4 text-indigo-400" />
          </div>
          <p className="text-2xl font-bold text-white">
            {insight?.high_activity_sites?.length ?? 0}
          </p>
          <span className="text-[11px] text-slate-400">Active industrial sites</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Units Needing Care</span>
            <Wrench className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400">
            {insight?.equipment_requiring_attention?.length ?? 0}
          </p>
          <span className="text-[11px] text-rose-400/80 font-medium">Critical / degraded</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Field Techs</span>
            <Users className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-white">
            {insight?.technicians_deployed ?? 0}
          </p>
          <span className="text-[11px] text-emerald-400 font-medium">Active in field</span>
        </div>

        <div className="bg-slate-900 border border-sky-500/30 p-4 rounded-xl bg-sky-950/10">
          <div className="flex items-center justify-between text-sky-400 text-xs mb-2">
            <span>Hindsight Memories</span>
            <Database className="w-4 h-4 text-sky-400" />
          </div>
          <p className="text-2xl font-bold text-sky-400">
            {memoryStats?.total_memories ?? 0}
          </p>
          <span className="text-[11px] text-sky-500 font-medium">Organizational bank</span>
        </div>
      </div>

      {/* 3. Memory Insights Highlight Bar */}
      <div className="bg-sky-500/10 border border-sky-500/30 rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-sky-500/20 rounded-lg text-sky-400 flex-shrink-0">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">
              Memory Intelligence Active: {insight?.recurring_issues?.length ?? 0} Recurring Equipment Issues Detected
            </h3>
            <p className="text-xs text-slate-300">
              {memoryStats?.memories_retrieved_today ?? 24} historical memories retrieved today to guide technicians away from repeating known temporary fixes.
            </p>
          </div>
        </div>
        <Link
          to="/insights"
          className="flex items-center gap-1.5 text-xs font-semibold text-sky-400 hover:text-sky-300 transition-colors whitespace-nowrap self-end md:self-center"
        >
          <span>View Insights Report</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* 4. Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Active Service Requests (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Ticket className="w-4 h-4 text-sky-400" />
                <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                  Active Service Requests
                </h2>
              </div>
              <Link
                to="/service-requests"
                className="text-xs text-sky-400 hover:text-sky-300 flex items-center gap-1"
              >
                <span>View all</span>
                <ArrowRight className="w-3 h-3" />
              </Link>
            </div>

            <div className="divide-y divide-slate-800">
              {activeRequests.length === 0 ? (
                <p className="p-6 text-slate-500 text-sm text-center">No active service requests.</p>
              ) : (
                activeRequests.map((sr) => (
                  <div
                    key={sr.id}
                    className="p-4 hover:bg-slate-800/40 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                  >
                    <div className="space-y-1.5 flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="font-mono text-xs text-slate-400 font-bold">
                          #{sr.id}
                        </span>
                        <span
                          className={clsx(
                            'px-2 py-0.5 rounded text-[10px] font-semibold uppercase',
                            sr.priority === 'Critical'
                              ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                              : sr.priority === 'High'
                              ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                              : 'bg-slate-700/50 text-slate-300'
                          )}
                        >
                          {sr.priority}
                        </span>
                        <span className="text-xs text-slate-400">
                          {sr.customer_name} · {sr.site_name}
                        </span>
                      </div>

                      <h3 className="text-sm font-semibold text-slate-100 truncate">
                        {sr.title}
                      </h3>

                      <p className="text-xs text-slate-400 line-clamp-1">
                        Equipment: <span className="text-slate-200 font-medium">{sr.equipment_name}</span> ({sr.equipment_category})
                      </p>
                    </div>

                    <div className="flex items-center gap-2 flex-shrink-0">
                      <button
                        onClick={() => navigate(`/service-requests/${sr.id}`)}
                        className="flex items-center gap-1.5 px-3 py-1.5 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded-lg text-xs font-semibold transition-colors"
                      >
                        <Wrench className="w-3.5 h-3.5" />
                        <span>Technician Workspace</span>
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Recently Retained Organizational Memories */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Brain className="w-4 h-4 text-purple-400" />
                <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                  Recently Created Organizational Memories
                </h2>
              </div>
              <Link
                to="/memory"
                className="text-xs text-sky-400 hover:text-sky-300 flex items-center gap-1"
              >
                <span>Memory Explorer</span>
                <ArrowRight className="w-3 h-3" />
              </Link>
            </div>

            <div className="divide-y divide-slate-800">
              {recentMemories.map((mem) => (
                <div key={mem.id} className="p-4 hover:bg-slate-800/40 transition-colors space-y-2">
                  <div className="flex items-center justify-between gap-2 flex-wrap">
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-purple-500/15 text-purple-300 border border-purple-500/30">
                        {mem.memory_type.replace(/_/g, ' ')}
                      </span>
                      <span className="text-xs font-medium text-slate-300">{mem.entity_name}</span>
                    </div>
                    <span className="text-[11px] text-slate-500">{mem.timestamp}</span>
                  </div>
                  <h4 className="text-xs font-semibold text-slate-100">{mem.title}</h4>
                  <p className="text-xs text-slate-400 leading-relaxed line-clamp-2">
                    {mem.content}
                  </p>
                  {mem.source_technician_name && (
                    <div className="text-[11px] text-slate-500">
                      Observation by: <span className="text-slate-300">{mem.source_technician_name}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Recurring Issues & Known Failed Fixes (1 col) */}
        <div className="space-y-6">
          {/* Known Failed / Temporary Fixes */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 border-b border-slate-800 flex items-center gap-2">
              <TrendingDown className="w-4 h-4 text-amber-400" />
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                Frequently Ineffective Fixes
              </h2>
            </div>
            <div className="p-4 space-y-3">
              <p className="text-xs text-slate-400">
                Actions that previously resulted in temporary fixes rather than permanent resolutions:
              </p>
              <div className="space-y-2.5">
                {insight?.failed_temporary_fixes?.slice(0, 4).map((f, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-lg bg-amber-500/5 border border-amber-500/20 text-xs space-y-1"
                  >
                    <div className="flex items-center justify-between text-amber-400 font-semibold">
                      <span>{f.equipment_name}</span>
                      <span className="text-[10px] bg-amber-500/20 px-1.5 py-0.5 rounded">
                        Failed {f.count}x
                      </span>
                    </div>
                    <p className="text-slate-300">Attempted: {f.action_taken}</p>
                    <p className="text-amber-500/80 text-[11px] italic">
                      Outcome: {f.outcome} — recurring problem
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Equipment Requiring Attention */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-rose-400" />
                <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                  High-Risk Equipment
                </h2>
              </div>
              <Link
                to="/equipment"
                className="text-xs text-sky-400 hover:text-sky-300"
              >
                All Equipment
              </Link>
            </div>
            <div className="divide-y divide-slate-800">
              {insight?.equipment_requiring_attention?.slice(0, 4).map((eq) => (
                <div
                  key={eq.id}
                  onClick={() => navigate(`/equipment/${eq.id}`)}
                  className="p-3.5 hover:bg-slate-800/40 cursor-pointer transition-colors space-y-1"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-white">{eq.name}</span>
                    <span
                      className={clsx(
                        'px-1.5 py-0.5 rounded text-[10px] font-medium',
                        eq.status === 'Critical'
                          ? 'bg-rose-500/20 text-rose-400'
                          : 'bg-amber-500/20 text-amber-400'
                      )}
                    >
                      {eq.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 truncate">
                    {eq.customer_name} · {eq.site_name}
                  </p>
                  <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1">
                    <span>Criticality: {eq.criticality}</span>
                    <span>{eq.incident_count} past incidents</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Memory Engine Architecture Card */}
          <div className="bg-gradient-to-br from-slate-900 to-sky-950/30 border border-sky-500/30 rounded-xl p-4 space-y-3">
            <div className="flex items-center gap-2 text-sky-400">
              <Brain className="w-4 h-4" />
              <h3 className="text-xs font-bold uppercase tracking-wider">Hindsight Architecture</h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Unlike generic chat bots or standard vector search, Hindsight constructs an evolving organizational memory graph. It captures temporal progression, recurring patterns, and technician observations across visits.
            </p>
            <div className="pt-2 border-t border-sky-500/20 flex items-center justify-between text-xs">
              <span className="text-slate-400 font-mono text-[11px]">
                Bank: {memoryStats?.bank_id || 'field-service-org-memory'}
              </span>
              <Link to="/settings" className="text-sky-400 hover:text-sky-300 font-medium">
                Engine Diagnostics →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

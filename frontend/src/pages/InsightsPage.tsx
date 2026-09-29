import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  BarChart3,
  AlertTriangle,
  TrendingDown,
  Building2,
  Wrench,
  Brain,
  CheckCircle2,
  ArrowRight,
  ShieldAlert,
} from 'lucide-react';
import { api } from '../api';
import type { Insight } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';

export default function InsightsPage() {
  const navigate = useNavigate();
  const [insight, setInsight] = useState<Insight | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadInsights();
  }, []);

  async function loadInsights() {
    try {
      setLoading(true);
      const data = await api.getInsights();
      setInsight(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load intelligence insights');
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <LoadingSpinner />;
  if (error || !insight) return <ErrorState message={error || 'Insights unavailable'} onRetry={loadInsights} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-sky-400 font-bold uppercase tracking-wider text-xs mb-1">
          <Brain className="w-4 h-4" />
          <span>Hindsight Operational Intelligence</span>
        </div>
        <h1 className="text-2xl font-bold text-white tracking-tight">
          Field Service Memory Insights
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Patterns, recurring failure modes, and ineffective fixes synthesized across {insight.memory_knowledge_base.total_memories} organizational memories.
        </p>
      </div>

      {/* Top 4 KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
          <span className="text-slate-400 text-xs font-medium">Recurring Problems Detected</span>
          <p className="text-3xl font-extrabold text-amber-400 mt-2">
            {insight.recurring_issues.length}
          </p>
          <span className="text-xs text-amber-500/80 mt-1 block">Repeated service visits</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
          <span className="text-slate-400 text-xs font-medium">Ineffective Fix Patterns</span>
          <p className="text-3xl font-extrabold text-rose-400 mt-2">
            {insight.failed_temporary_fixes.length}
          </p>
          <span className="text-xs text-rose-400/80 mt-1 block">Actions that didn't hold</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
          <span className="text-slate-400 text-xs font-medium">High Attention Units</span>
          <p className="text-3xl font-extrabold text-white mt-2">
            {insight.equipment_requiring_attention.length}
          </p>
          <span className="text-xs text-slate-400 mt-1 block">Degraded or repeated faults</span>
        </div>

        <div className="bg-slate-900 border border-sky-500/30 p-5 rounded-2xl bg-sky-950/10">
          <span className="text-sky-400 text-xs font-medium">Retained Technician Lessons</span>
          <p className="text-3xl font-extrabold text-sky-400 mt-2">
            {insight.memory_knowledge_base.technician_observations}
          </p>
          <span className="text-xs text-sky-500 mt-1 block">Preserved observations</span>
        </div>
      </div>

      {/* Two Column Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recurring Equipment Issues */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                Recurring Equipment Issues
              </h2>
            </div>
            <span className="text-xs text-slate-500">2+ visits on record</span>
          </div>

          <div className="divide-y divide-slate-800">
            {insight.recurring_issues.map((rec) => (
              <div
                key={rec.equipment_id}
                onClick={() => navigate(`/equipment/${rec.equipment_id}`)}
                className="p-4 hover:bg-slate-800/40 cursor-pointer transition-colors space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-white text-sm hover:text-sky-300">
                      {rec.equipment_name}
                    </span>
                    <span className="text-slate-500">({rec.category})</span>
                  </div>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                    {rec.total_visits} Visits
                  </span>
                </div>

                <p className="text-slate-400">
                  {rec.customer_name} · {rec.site_name}
                </p>

                <div className="flex items-center gap-4 text-slate-500 text-[11px] pt-1">
                  <span>Temporary Fixes: <strong className="text-amber-400">{rec.temporary_count}</strong></span>
                  <span>Unresolved: <strong className="text-rose-400">{rec.unresolved_count}</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Ineffective Temporary Fixes */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <TrendingDown className="w-4 h-4 text-rose-400" />
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                Frequently Ineffective Actions
              </h2>
            </div>
            <span className="text-xs text-slate-500">Known pitfall actions</span>
          </div>

          <div className="divide-y divide-slate-800">
            {insight.failed_temporary_fixes.map((f, i) => (
              <div key={i} className="p-4 space-y-1.5 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white">{f.equipment_name}</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
                    Recurred {f.count}x
                  </span>
                </div>
                <p className="text-slate-300">
                  Action Attempted: <strong className="text-slate-100">{f.action_taken}</strong>
                </p>
                <p className="text-rose-400/80 text-[11px] italic">
                  Outcome: {f.outcome} — problem returned after temporary relief.
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* High Activity Sites & Knowledge Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* High Activity Sites */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 flex items-center gap-2">
            <Building2 className="w-4 h-4 text-indigo-400" />
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Sites with Concentrated Service Activity
            </h2>
          </div>
          <div className="divide-y divide-slate-800">
            {insight.high_activity_sites.map((site, i) => (
              <div key={i} className="p-4 flex items-center justify-between text-xs">
                <div>
                  <h4 className="font-semibold text-white">{site.site_name}</h4>
                  <p className="text-slate-400 text-[11px]">{site.customer_name}</p>
                </div>
                <span className="px-2.5 py-1 bg-indigo-500/10 text-indigo-400 font-bold rounded-lg border border-indigo-500/20 text-xs">
                  {site.incident_count} Incidents / Visits
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Memory Knowledge Base Breakdown */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
          <div className="flex items-center gap-2 text-sky-400">
            <Brain className="w-4 h-4" />
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Hindsight Knowledge Base Breakdown
            </h2>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Technician Observations & Notes</span>
                <span className="font-mono text-purple-400">{insight.memory_knowledge_base.technician_observations}</span>
              </div>
              <div className="h-2 bg-slate-950 rounded-full overflow-hidden">
                <div className="h-full bg-purple-500 rounded-full" style={{ width: '45%' }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Equipment Recurrence Signatures</span>
                <span className="font-mono text-amber-400">{insight.memory_knowledge_base.equipment_patterns}</span>
              </div>
              <div className="h-2 bg-slate-950 rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 rounded-full" style={{ width: '30%' }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Verified Permanent Solutions</span>
                <span className="font-mono text-emerald-400">{insight.memory_knowledge_base.resolved_cases}</span>
              </div>
              <div className="h-2 bg-slate-950 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 rounded-full" style={{ width: '60%' }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Unresolved / Failed Fix Records</span>
                <span className="font-mono text-rose-400">{insight.memory_knowledge_base.unresolved_cases}</span>
              </div>
              <div className="h-2 bg-slate-950 rounded-full overflow-hidden">
                <div className="h-full bg-rose-500 rounded-full" style={{ width: '25%' }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

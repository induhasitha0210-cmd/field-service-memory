import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  Wrench,
  Building2,
  MapPin,
  Clock,
  History,
  Brain,
  MessageSquare,
  ArrowLeft,
  Calendar,
  Shield,
  Plus,
  Send,
  Sparkles,
  Database,
  X,
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';
import type { Equipment, ServiceRecord, MemoryItem, TimelineEvent, MemoryEvidence } from '../types';
import Timeline from '../components/Timeline';
import MemoryCard from '../components/MemoryCard';
import MemoryEvidenceView from '../components/MemoryEvidence';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';

export default function EquipmentDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [equipment, setEquipment] = useState<Equipment | null>(null);
  const [history, setHistory] = useState<ServiceRecord[]>([]);
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>([]);
  const [activeTab, setActiveTab] = useState<'timeline' | 'history' | 'memories'>('timeline');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // "Ask Equipment Memory" natural language query state
  const [askModalOpen, setAskModalOpen] = useState(false);
  const [askQuery, setAskQuery] = useState('');
  const [askLoading, setAskLoading] = useState(false);
  const [askAnswer, setAskAnswer] = useState<string | null>(null);
  const [askEvidence, setAskEvidence] = useState<MemoryEvidence[]>([]);

  useEffect(() => {
    if (id) {
      loadData(id);
    }
  }, [id]);

  async function loadData(equipId: string) {
    try {
      setLoading(true);
      setError(null);
      const [eq, hist, mems, tl] = await Promise.all([
        api.getEquipmentById(equipId),
        api.getEquipmentHistory(equipId),
        api.getEquipmentMemories(equipId),
        api.getEquipmentTimeline(equipId),
      ]);
      setEquipment(eq);
      setHistory(hist);
      setMemories(mems);
      setTimelineEvents(tl);
    } catch (err: any) {
      setError(err.message || 'Failed to load equipment details');
    } finally {
      setLoading(false);
    }
  }

  async function handleAskMemory(e: React.FormEvent) {
    e.preventDefault();
    if (!id || !askQuery.trim()) return;

    try {
      setAskLoading(true);
      setAskAnswer(null);
      setAskEvidence([]);
      const res = await api.askMemory(askQuery, id as any);
      setAskAnswer(res.answer);
      setAskEvidence(res.evidence || []);
    } catch (err: any) {
      setAskAnswer(`Query error: ${err.message}`);
    } finally {
      setAskLoading(false);
    }
  }

  if (loading) return <LoadingSpinner />;
  if (error || !equipment) return <ErrorState message={error || 'Equipment not found'} onRetry={() => id && loadData(id)} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Back button & Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/equipment')}
            className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-sky-400">#{equipment.id}</span>
              <span
                className={clsx(
                  'px-2 py-0.5 rounded text-[10px] font-semibold',
                  equipment.status === 'Operational'
                    ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                    : equipment.status === 'Degraded Performance'
                    ? 'bg-amber-500/15 text-amber-400 border border-amber-500/30'
                    : 'bg-rose-500/15 text-rose-400 border border-rose-500/30'
                )}
              >
                {equipment.status}
              </span>
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight mt-1">
              {equipment.name}
            </h1>
          </div>
        </div>

        {/* Action Buttons: Ask Memory & Create Service Request */}
        <div className="flex items-center gap-3 self-start sm:self-auto">
          <button
            onClick={() => {
              setAskQuery(`Has ${equipment.name} experienced similar failures before?`);
              setAskModalOpen(true);
            }}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white rounded-xl text-xs font-bold shadow-md shadow-sky-500/20 transition-all"
          >
            <Brain className="w-4 h-4" />
            <span>Ask Equipment Memory</span>
          </button>
        </div>
      </div>

      {/* Equipment Specification Card */}
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 text-xs">
        <div>
          <span className="text-slate-500 block mb-1">Category</span>
          <p className="text-white font-semibold">{equipment.category}</p>
        </div>
        <div>
          <span className="text-slate-500 block mb-1">Model</span>
          <p className="text-white font-semibold">{equipment.model || 'Standard'}</p>
        </div>
        <div>
          <span className="text-slate-500 block mb-1">Customer</span>
          <p className="text-white font-semibold truncate">{equipment.customer_name}</p>
        </div>
        <div>
          <span className="text-slate-500 block mb-1">Site</span>
          <p className="text-white font-semibold truncate">{equipment.site_name}</p>
        </div>
        <div>
          <span className="text-slate-500 block mb-1">Operating Hours</span>
          <p className="text-white font-semibold">{equipment.operating_hours.toLocaleString()} hrs</p>
        </div>
        <div>
          <span className="text-slate-500 block mb-1">Installation Date</span>
          <p className="text-white font-semibold">{equipment.installation_date || 'N/A'}</p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6 text-sm">
        <button
          onClick={() => setActiveTab('timeline')}
          className={clsx(
            'pb-3 font-semibold transition-all border-b-2 flex items-center gap-2',
            activeTab === 'timeline'
              ? 'border-sky-400 text-sky-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          )}
        >
          <Calendar className="w-4 h-4" />
          <span>Memory Timeline ({timelineEvents.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('history')}
          className={clsx(
            'pb-3 font-semibold transition-all border-b-2 flex items-center gap-2',
            activeTab === 'history'
              ? 'border-sky-400 text-sky-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          )}
        >
          <History className="w-4 h-4" />
          <span>Service Visits ({history.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('memories')}
          className={clsx(
            'pb-3 font-semibold transition-all border-b-2 flex items-center gap-2',
            activeTab === 'memories'
              ? 'border-sky-400 text-sky-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          )}
        >
          <Brain className="w-4 h-4" />
          <span>Hindsight Memories ({memories.length})</span>
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'timeline' && (
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Chronological Memory Stream for {equipment.name}
            </h3>
            <span className="text-[11px] text-sky-400">
              Preserving equipment evolution over time
            </span>
          </div>
          <Timeline events={timelineEvents} />
        </div>
      )}

      {activeTab === 'history' && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden divide-y divide-slate-800">
          {history.length === 0 ? (
            <p className="p-8 text-center text-slate-500 text-sm">No service visits recorded.</p>
          ) : (
            history.map((rec) => (
              <div key={rec.id} className="p-5 space-y-3 text-xs">
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <div className="flex items-center gap-3">
                    <span className="font-mono font-bold text-sky-400">#{rec.id}</span>
                    <span className="text-slate-400">Visit Date: {rec.visit_date}</span>
                    <span className="text-slate-300">Technician: {rec.technician_name}</span>
                  </div>
                  <span
                    className={clsx(
                      'px-2 py-0.5 rounded text-[10px] font-semibold',
                      rec.outcome === 'Resolved'
                        ? 'bg-emerald-500/15 text-emerald-400'
                        : rec.outcome === 'Temporarily Resolved'
                        ? 'bg-amber-500/15 text-amber-400'
                        : 'bg-rose-500/15 text-rose-400'
                    )}
                  >
                    {rec.outcome}
                  </span>
                </div>

                <div className="space-y-1.5 text-slate-300">
                  <p><span className="text-slate-500 font-medium">Symptoms:</span> {rec.symptoms_observed}</p>
                  <p><span className="text-slate-500 font-medium">Action:</span> {rec.action_taken}</p>
                  {rec.parts_replaced && (
                    <p><span className="text-slate-500 font-medium">Parts:</span> {rec.parts_replaced}</p>
                  )}
                  {rec.technician_notes && (
                    <p className="italic text-slate-400 bg-slate-950/40 p-2.5 rounded-lg border border-slate-800">
                      "{rec.technician_notes}"
                    </p>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'memories' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {memories.length === 0 ? (
            <p className="col-span-2 p-8 text-center text-slate-500 text-sm">
              No memories retained for this equipment unit yet.
            </p>
          ) : (
            memories.map((m) => <MemoryCard key={m.id} item={m} />)
          )}
        </div>
      )}

      {/* Ask Equipment Memory Modal */}
      {askModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden shadow-2xl">
            {/* Modal Header */}
            <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
              <div className="flex items-center gap-2">
                <Brain className="w-5 h-5 text-sky-400" />
                <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                  Ask Equipment Memory: {equipment.name}
                </h3>
              </div>
              <button
                onClick={() => setAskModalOpen(false)}
                className="text-slate-400 hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-5 overflow-y-auto space-y-4 flex-1 text-xs">
              <form onSubmit={handleAskMemory} className="space-y-3">
                <div className="relative">
                  <input
                    type="text"
                    required
                    placeholder={`e.g. Has ${equipment.name} had overheating problems before?`}
                    value={askQuery}
                    onChange={(e) => setAskQuery(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 text-xs focus:outline-none focus:border-sky-500 pr-24"
                  />
                  <button
                    type="submit"
                    disabled={askLoading}
                    className="absolute right-1.5 top-1.5 bottom-1.5 px-3 bg-sky-500 hover:bg-sky-400 text-white font-semibold rounded-lg flex items-center gap-1 text-xs disabled:opacity-50"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>{askLoading ? 'Thinking...' : 'Ask'}</span>
                  </button>
                </div>

                {/* Preset prompt pills */}
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-[11px] text-slate-500">Suggested:</span>
                  {[
                    `Why did previous repairs fail on this unit?`,
                    `What did technicians observe during past visits?`,
                    `What parts were replaced on ${equipment.name}?`,
                  ].map((preset, i) => (
                    <button
                      key={i}
                      type="button"
                      onClick={() => setAskQuery(preset)}
                      className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-full text-[11px] transition-colors"
                    >
                      {preset}
                    </button>
                  ))}
                </div>
              </form>

              {/* Answer display */}
              {askAnswer && (
                <div className="space-y-3 pt-4 border-t border-slate-800">
                  <div className="p-4 bg-sky-950/20 border border-sky-500/30 rounded-xl space-y-2">
                    <div className="flex items-center gap-1.5 text-sky-400 font-bold uppercase tracking-wider text-[10px]">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Hindsight Grounded Answer</span>
                    </div>
                    <p className="text-slate-200 text-xs leading-relaxed whitespace-pre-line font-sans">
                      {askAnswer}
                    </p>
                  </div>

                  {/* Supporting Evidence */}
                  {askEvidence.length > 0 && (
                    <div className="space-y-2">
                      <h4 className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                        Supporting Memory Evidence ({askEvidence.length})
                      </h4>
                      <MemoryEvidenceView evidence={askEvidence} />
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

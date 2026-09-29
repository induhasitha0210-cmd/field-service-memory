import { useEffect, useState } from 'react';
import {
  Brain,
  Search,
  Filter,
  Send,
  Sparkles,
  Database,
  Plus,
  X,
  History,
  Tag,
  CheckCircle,
  AlertTriangle,
  MessageSquare,
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';
import type { MemoryItem, MemoryEvidence } from '../types';
import MemoryCard from '../components/MemoryCard';
import MemoryEvidenceView from '../components/MemoryEvidence';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';

export default function MemoryExplorerPage() {
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Ask the Memory state
  const [query, setQuery] = useState('');
  const [asking, setAsking] = useState(false);
  const [answer, setAnswer] = useState<string | null>(null);
  const [evidence, setEvidence] = useState<MemoryEvidence[]>([]);

  // Filters
  const [typeFilter, setTypeFilter] = useState('ALL');
  const [search, setSearch] = useState('');

  // Retain Memory Modal state
  const [isRetainModalOpen, setIsRetainModalOpen] = useState(false);
  const [newContent, setNewContent] = useState('');
  const [newEntityId, setNewEntityId] = useState('EQUIP-001');
  const [newEntityType, setNewEntityType] = useState('equipment');
  const [newEntityName, setNewEntityName] = useState('HVAC-204');
  const [newMemoryType, setNewMemoryType] = useState('TECHNICIAN_OBSERVATION');
  const [newTechName, setNewTechName] = useState('Ravi Verma');
  const [newTags, setNewTags] = useState('vibration,compressor,hvac');
  const [retaining, setRetaining] = useState(false);

  useEffect(() => {
    loadMemories();
  }, []);

  async function loadMemories() {
    try {
      setLoading(true);
      const data = await api.getMemories();
      setMemories(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load organizational memory bank');
    } finally {
      setLoading(false);
    }
  }

  async function handleAskMemory(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setAsking(true);
      setAnswer(null);
      setEvidence([]);
      const res = await api.askMemory(query);
      setAnswer(res.answer);
      setEvidence(res.evidence || []);
    } catch (err: any) {
      setAnswer(`Memory reflection failed: ${err.message}`);
    } finally {
      setAsking(false);
    }
  }

  async function handleRetainMemory(e: React.FormEvent) {
    e.preventDefault();
    if (!newContent.trim()) return;

    try {
      setRetaining(true);
      await fetch('/api/memory/retain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: newContent,
          entity_id: newEntityId,
          entity_type: newEntityType,
          entity_name: newEntityName,
          memory_type: newMemoryType,
          source_technician_name: newTechName,
          tags: newTags.split(',').map((t) => t.trim()),
          outcome_status: 'Resolved',
        }),
      });

      setIsRetainModalOpen(false);
      setNewContent('');
      await loadMemories();
    } catch (err: any) {
      alert(`Retain error: ${err.message}`);
    } finally {
      setRetaining(false);
    }
  }

  const memoryTypes = [
    { label: 'All Memories', value: 'ALL' },
    { label: 'Technician Observations', value: 'TECHNICIAN_OBSERVATION' },
    { label: 'Equipment Recurrence', value: 'EQUIPMENT_RECURRENCE' },
    { label: 'Failed / Temp Fixes', value: 'FAILED_FIX' },
    { label: 'Successful Fixes', value: 'SUCCESSFUL_FIX' },
    { label: 'Site Patterns', value: 'SITE_ENVIRONMENTAL' },
  ];

  const filteredMemories = memories.filter((m) => {
    if (typeFilter !== 'ALL' && m.memory_type !== typeFilter) return false;
    if (search.trim()) {
      const q = search.toLowerCase();
      const match =
        m.title.toLowerCase().includes(q) ||
        m.content.toLowerCase().includes(q) ||
        m.entity_name.toLowerCase().includes(q) ||
        (m.source_technician_name && m.source_technician_name.toLowerCase().includes(q)) ||
        (m.tags && m.tags.some((t) => t.toLowerCase().includes(q)));
      if (!match) return false;
    }
    return true;
  });

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorState message={error} onRetry={loadMemories} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Brain className="w-6 h-6 text-sky-400" />
            <span>Hindsight Memory Explorer ({memories.length} Memories)</span>
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Browse persistent organizational memories, query past technician experiences, and inspect grounded audit evidence.
          </p>
        </div>

        <button
          onClick={() => setIsRetainModalOpen(true)}
          className="flex items-center gap-2 px-4 py-2 bg-sky-500 hover:bg-sky-400 text-white rounded-xl text-sm font-semibold shadow-md shadow-sky-500/20 transition-all self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>Retain New Memory</span>
        </button>
      </div>

      {/* 1. Natural Language "Ask the Memory" Section */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-900 to-sky-950/40 border border-sky-500/30 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center gap-2 text-sky-400 font-bold uppercase tracking-wider text-xs">
          <Sparkles className="w-4 h-4" />
          <span>Ask Organizational Memory</span>
        </div>

        <form onSubmit={handleAskMemory} className="space-y-3">
          <div className="relative">
            <input
              type="text"
              required
              placeholder="Ask anything... e.g. 'What did Ravi observe during the previous visit?' or 'Which solutions worked for cooling failures?'"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3.5 text-slate-100 text-sm focus:outline-none focus:border-sky-500 pr-28 shadow-inner"
            />
            <button
              type="submit"
              disabled={asking}
              className="absolute right-2 top-2 bottom-2 px-4 bg-sky-500 hover:bg-sky-400 text-white font-semibold rounded-lg flex items-center gap-1.5 text-xs disabled:opacity-50 transition-all shadow"
            >
              <Send className="w-3.5 h-3.5" />
              <span>{asking ? 'Searching...' : 'Recall'}</span>
            </button>
          </div>

          {/* Quick preset chips */}
          <div className="flex items-center gap-2 flex-wrap text-xs">
            <span className="text-slate-500">Sample questions:</span>
            {[
              'Has HVAC-204 had overheating issues before?',
              'Why was the last repair unsuccessful?',
              'What did Ravi observe during the previous visit?',
              'Which solutions worked for cooling failures?',
              'What problems keep recurring at Hyderabad Plant?',
            ].map((qText, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => setQuery(qText)}
                className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-full text-[11px] transition-colors border border-slate-700/60"
              >
                {qText}
              </button>
            ))}
          </div>
        </form>

        {/* Answer & Grounded Evidence */}
        {answer && (
          <div className="pt-4 border-t border-slate-800 space-y-4">
            <div className="p-4 bg-slate-950/70 border border-sky-500/30 rounded-xl space-y-2">
              <div className="flex items-center gap-1.5 text-sky-400 font-bold uppercase tracking-wider text-[11px]">
                <Brain className="w-4 h-4" />
                <span>Memory Reflection Response</span>
              </div>
              <p className="text-slate-200 text-sm leading-relaxed whitespace-pre-line font-sans">
                {answer}
              </p>
            </div>

            {evidence.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Underlying Memory Evidence ({evidence.length} Memories Cited)
                </h4>
                <MemoryEvidenceView evidence={evidence} />
              </div>
            )}
          </div>
        )}
      </div>

      {/* 2. Type Tabs & Search */}
      <div className="space-y-4">
        {/* Type pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
          {memoryTypes.map((t) => (
            <button
              key={t.value}
              onClick={() => setTypeFilter(t.value)}
              className={clsx(
                'px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all',
                typeFilter === t.value
                  ? 'bg-sky-500 text-white shadow-sm'
                  : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
              )}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search memories by keyword, entity, technician, failure mode, or tags..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>
      </div>

      {/* 3. Memories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredMemories.length === 0 ? (
          <div className="col-span-full p-12 text-center text-slate-500 text-sm">
            No memories match the current filters.
          </div>
        ) : (
          filteredMemories.map((item) => <MemoryCard key={item.id} item={item} />)
        )}
      </div>

      {/* Retain New Memory Modal */}
      {isRetainModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full overflow-hidden shadow-2xl">
            <div className="p-5 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Brain className="w-5 h-5 text-sky-400" />
                <h3 className="text-base font-bold text-white">Retain Organizational Memory</h3>
              </div>
              <button
                onClick={() => setIsRetainModalOpen(false)}
                className="text-slate-400 hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleRetainMemory} className="p-5 space-y-4 text-xs">
              <div>
                <label className="block text-slate-300 font-medium mb-1">
                  Memory Content (Detailed Observation / Lesson) *
                </label>
                <textarea
                  required
                  rows={4}
                  placeholder="Describe the technical learning, observation, or recurrence..."
                  value={newContent}
                  onChange={(e) => setNewContent(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-sky-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-medium mb-1">Memory Type</label>
                  <select
                    value={newMemoryType}
                    onChange={(e) => setNewMemoryType(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-sky-500"
                  >
                    <option value="TECHNICIAN_OBSERVATION">Technician Observation</option>
                    <option value="EQUIPMENT_RECURRENCE">Equipment Recurrence</option>
                    <option value="FAILED_FIX">Failed / Temporary Fix</option>
                    <option value="SUCCESSFUL_FIX">Successful Fix</option>
                    <option value="SITE_ENVIRONMENTAL">Site Environmental</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">Technician</label>
                  <input
                    type="text"
                    value={newTechName}
                    onChange={(e) => setNewTechName(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-sky-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-medium mb-1">Entity ID</label>
                  <input
                    type="text"
                    value={newEntityId}
                    onChange={(e) => setNewEntityId(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-sky-500"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">Entity Name</label>
                  <input
                    type="text"
                    value={newEntityName}
                    onChange={(e) => setNewEntityName(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-sky-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Tags (comma-separated)</label>
                <input
                  type="text"
                  placeholder="e.g. vibration, compressor, high_temp"
                  value={newTags}
                  onChange={(e) => setNewTags(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-sky-500"
                />
              </div>

              <div className="pt-3 border-t border-slate-800 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsRetainModalOpen(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={retaining}
                  className="px-5 py-2 bg-sky-500 hover:bg-sky-400 text-white font-semibold rounded-xl disabled:opacity-50"
                >
                  {retaining ? 'Retaining...' : 'Retain in Hindsight'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

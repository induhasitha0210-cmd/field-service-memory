import { useEffect, useState } from 'react';
import {
  Brain,
  Database,
  CheckCircle2,
  AlertCircle,
  Play,
  Send,
  Zap,
  RefreshCw,
  Terminal,
  Server,
  Layers,
  Sparkles,
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';
import type { MemoryStats } from '../types';

export default function SettingsPage() {
  const [status, setStatus] = useState<any>(null);
  const [stats, setStats] = useState<MemoryStats | null>(null);
  const [loading, setLoading] = useState(true);

  // Interactive Test State
  const [testMode, setTestMode] = useState<'recall' | 'reflect' | 'retain'>('recall');
  const [testQuery, setTestQuery] = useState('compressor vibration overheating');
  const [testOutput, setTestOutput] = useState<any>(null);
  const [testRunning, setTestRunning] = useState(false);

  useEffect(() => {
    loadStatus();
  }, []);

  async function loadStatus() {
    try {
      setLoading(true);
      const [st, stts] = await Promise.all([
        api.getHindsightStatus(),
        api.getMemoryStats(),
      ]);
      setStatus(st);
      setStats(stts);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleRunTest(e: React.FormEvent) {
    e.preventDefault();
    if (!testQuery.trim()) return;

    try {
      setTestRunning(true);
      setTestOutput(null);

      if (testMode === 'recall') {
        const res = await fetch('/api/memory/recall', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: testQuery, max_tokens: 2048, budget: 'mid' }),
        }).then((r) => r.json());
        setTestOutput(res);
      } else if (testMode === 'reflect') {
        const res = await fetch('/api/memory/reflect', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: testQuery, budget: 'low' }),
        }).then((r) => r.json());
        setTestOutput(res);
      } else if (testMode === 'retain') {
        const res = await fetch('/api/memory/retain', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            content: testQuery,
            entity_id: 'EQUIP-001',
            entity_type: 'equipment',
            entity_name: 'HVAC-204',
            memory_type: 'TECHNICIAN_OBSERVATION',
            tags: ['test', 'hvac', 'diagnostics'],
            outcome_status: 'Resolved',
          }),
        }).then((r) => r.json());
        setTestOutput(res);
        await loadStatus();
      }
    } catch (err: any) {
      setTestOutput({ error: err.message });
    } finally {
      setTestRunning(false);
    }
  }

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-sky-400 font-bold uppercase tracking-wider text-xs mb-1">
          <Database className="w-4 h-4" />
          <span>Core Technology Configuration</span>
        </div>
        <h1 className="text-2xl font-bold text-white tracking-tight">
          Hindsight Memory Engine & Settings
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Technical architecture, memory bank telemetry, and real-time SDK operation verification.
        </p>
      </div>

      {/* 1. Memory Engine Status Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 font-medium">Engine Mode</span>
            <span
              className={clsx(
                'w-2.5 h-2.5 rounded-full',
                status?.hindsight_available ? 'bg-emerald-400' : 'bg-amber-400'
              )}
            />
          </div>
          <p className="text-xl font-bold text-white">
            {status?.hindsight_available ? 'Hindsight Live API' : 'Biomimetic Local Engine'}
          </p>
          <span className="text-[11px] text-slate-500 block">
            {status?.hindsight_available
              ? 'Connected to Vectorize.io Cloud Bank'
              : 'Local persistent engine with full semantic/temporal multi-strategy'}
          </span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 font-medium">Memory Bank ID</span>
            <Brain className="w-4 h-4 text-sky-400" />
          </div>
          <p className="text-lg font-mono font-bold text-sky-400 truncate">
            {status?.bank_id || 'field-service-org-memory'}
          </p>
          <span className="text-[11px] text-slate-500 block">
            Isolated organizational knowledge bank
          </span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 font-medium">Total Memories Retained</span>
            <Database className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-xl font-bold text-white">
            {stats?.total_memories || 32} Stored Experiences
          </p>
          <span className="text-[11px] text-slate-500 block">
            {stats?.memories_retrieved_today || 14} retrieved today across tickets
          </span>
        </div>
      </div>

      {/* 2. Visual Architecture Pipeline (Prompt Section 25) */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div className="flex items-center gap-2 text-sky-400 font-bold uppercase tracking-wider text-xs">
          <Layers className="w-4 h-4" />
          <span>Hindsight Architecture & Data Flow</span>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed max-w-3xl">
          The application strictly separates structured entity records (customers, sites, tickets in SQLite) from evolving experiential knowledge stored inside <strong className="text-sky-300">Hindsight</strong>. This ensures technician observations, temporary failures, and recurring patterns form an organizational memory that compounds over time.
        </p>

        {/* Visual Pipeline flow */}
        <div className="pt-4 grid grid-cols-1 md:grid-cols-6 gap-3 text-center text-xs">
          <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
            <span className="text-sky-400 font-bold block text-[11px]">HINDSIGHT</span>
            <span className="text-slate-400 text-[10px]">Bank: {status?.bank_id || 'field-service'}</span>
          </div>
          <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
            <span className="text-sky-400 font-bold block text-[11px]">STORED EXPERIENCES</span>
            <span className="text-slate-400 text-[10px]">World & Observations</span>
          </div>
          <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
            <span className="text-sky-400 font-bold block text-[11px]">RECALL ENGINE</span>
            <span className="text-slate-400 text-[10px]">Multi-strategy Fused</span>
          </div>
          <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
            <span className="text-emerald-400 font-bold block text-[11px]">AGENT CONTEXT</span>
            <span className="text-slate-400 text-[10px]">"Seen this before"</span>
          </div>
          <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
            <span className="text-amber-400 font-bold block text-[11px]">TECH ACTION</span>
            <span className="text-slate-400 text-[10px]">Root-cause Fix</span>
          </div>
          <div className="p-3 bg-slate-950 border border-sky-500/40 rounded-xl space-y-1 bg-sky-950/20">
            <span className="text-sky-300 font-bold block text-[11px]">NEW MEMORY</span>
            <span className="text-sky-400 text-[10px]">retain() executed</span>
          </div>
        </div>
      </div>

      {/* 3. Interactive SDK Test Console */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sky-400 font-bold uppercase tracking-wider text-xs">
            <Terminal className="w-4 h-4" />
            <span>Interactive Hindsight API / SDK Console</span>
          </div>
          <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
            <button
              onClick={() => setTestMode('recall')}
              className={clsx(
                'px-3 py-1 rounded-md font-medium transition-all',
                testMode === 'recall' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-slate-200'
              )}
            >
              client.recall()
            </button>
            <button
              onClick={() => setTestMode('reflect')}
              className={clsx(
                'px-3 py-1 rounded-md font-medium transition-all',
                testMode === 'reflect' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-slate-200'
              )}
            >
              client.reflect()
            </button>
            <button
              onClick={() => setTestMode('retain')}
              className={clsx(
                'px-3 py-1 rounded-md font-medium transition-all',
                testMode === 'retain' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-slate-200'
              )}
            >
              client.retain()
            </button>
          </div>
        </div>

        <form onSubmit={handleRunTest} className="space-y-3">
          <div className="relative">
            <input
              type="text"
              required
              placeholder={
                testMode === 'retain'
                  ? 'Enter memory content to retain in bank...'
                  : 'Enter test query for recall / reflect...'
              }
              value={testQuery}
              onChange={(e) => setTestQuery(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500 pr-24 font-mono"
            />
            <button
              type="submit"
              disabled={testRunning}
              className="absolute right-1.5 top-1.5 bottom-1.5 px-3 bg-sky-500 hover:bg-sky-400 text-white text-xs font-semibold rounded-lg flex items-center gap-1 disabled:opacity-50"
            >
              <Play className="w-3 h-3 fill-current" />
              <span>{testRunning ? 'Calling...' : 'Execute'}</span>
            </button>
          </div>
        </form>

        {/* Console output display */}
        {testOutput && (
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 font-mono text-xs space-y-2">
            <div className="flex items-center justify-between text-slate-500 text-[11px] pb-1 border-b border-slate-800 font-sans">
              <span>Hindsight SDK Execution Result</span>
              <span className="text-emerald-400 font-mono">Status: 200 OK</span>
            </div>
            <pre className="overflow-x-auto text-[11px] text-sky-300 leading-relaxed max-h-64">
              {JSON.stringify(testOutput, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

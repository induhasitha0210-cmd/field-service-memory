import { useEffect, useState } from 'react';
import {
  Users,
  Search,
  Briefcase,
  Ticket,
  Star,
  Brain,
  MessageSquare,
  Wrench,
  CheckCircle,
  X,
} from 'lucide-react';
import { api } from '../api';
import type { Technician, MemoryItem } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';

export default function TechniciansPage() {
  const [technicians, setTechnicians] = useState<Technician[]>([]);
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');

  // Selected tech modal
  const [selectedTech, setSelectedTech] = useState<Technician | null>(null);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const [tList, mList] = await Promise.all([
          api.getTechnicians(),
          api.getMemories(),
        ]);
        setTechnicians(tList);
        setMemories(mList);
      } catch (err: any) {
        setError(err.message || 'Failed to load technicians');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const filtered = technicians.filter((t) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      t.name.toLowerCase().includes(q) ||
      t.role.toLowerCase().includes(q) ||
      t.skills.some((s) => s.toLowerCase().includes(q))
    );
  });

  const techMemories = selectedTech
    ? memories.filter((m) => m.source_technician_name === selectedTech.name)
    : [];

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Users className="w-6 h-6 text-sky-400" />
          <span>Field Technicians ({technicians.length})</span>
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Every technician's observation becomes permanent organizational memory, accessible by future technicians.
        </p>
      </div>

      {/* Search */}
      <div className="relative max-w-md">
        <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="Search technicians by name, role, or skill..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500"
        />
      </div>

      {/* Technicians Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((t) => {
          const count = memories.filter((m) => m.source_technician_name === t.name).length;

          return (
            <div
              key={t.id}
              onClick={() => setSelectedTech(t)}
              className="bg-slate-900 border border-slate-800 hover:border-sky-500/40 p-5 rounded-2xl cursor-pointer transition-all hover:shadow-xl space-y-4 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white font-bold text-sm shadow">
                      {t.name.split(' ').map((n) => n[0]).join('')}
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-white">{t.name}</h3>
                      <p className="text-[11px] text-slate-400">{t.role}</p>
                    </div>
                  </div>
                  <span className="text-[10px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                    {t.years_experience} yrs exp
                  </span>
                </div>

                {/* Skills tags */}
                <div className="flex items-center gap-1.5 flex-wrap">
                  {t.skills.slice(0, 4).map((s, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 rounded text-[10px] bg-slate-800/80 text-slate-300 border border-slate-700/60"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              {/* Memory contribution stat */}
              <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5 text-purple-400">
                  <Brain className="w-3.5 h-3.5" />
                  <span className="font-semibold">{count} Observations Retained</span>
                </div>
                <span className="text-sky-400 text-xs font-semibold">Inspect →</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Tech Details Modal */}
      {selectedTech && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-xl w-full max-h-[85vh] flex flex-col overflow-hidden shadow-2xl">
            <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-full bg-sky-500 flex items-center justify-center text-white font-bold text-xs">
                  {selectedTech.name.split(' ').map((n) => n[0]).join('')}
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white">{selectedTech.name}</h3>
                  <p className="text-[11px] text-slate-400">{selectedTech.role} · {selectedTech.years_experience} Years</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedTech(null)}
                className="text-slate-400 hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-5 overflow-y-auto space-y-4 flex-1 text-xs">
              <div>
                <h4 className="text-slate-400 font-semibold mb-2 uppercase text-[11px] tracking-wider">
                  Technical Expertise
                </h4>
                <div className="flex items-center gap-1.5 flex-wrap">
                  {selectedTech.skills.map((s, i) => (
                    <span key={i} className="px-2.5 py-1 rounded bg-slate-800 text-slate-200">
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-2 border-t border-slate-800 space-y-3">
                <h4 className="text-purple-400 font-bold uppercase text-[11px] tracking-wider flex items-center gap-2">
                  <Brain className="w-4 h-4" />
                  <span>Observations Retained in Hindsight by {selectedTech.name} ({techMemories.length})</span>
                </h4>

                <div className="space-y-2">
                  {techMemories.length === 0 ? (
                    <p className="text-slate-500 italic">No specific observations logged yet.</p>
                  ) : (
                    techMemories.map((m) => (
                      <div
                        key={m.id}
                        className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5"
                      >
                        <div className="flex items-center justify-between text-slate-400 text-[10px]">
                          <span className="font-semibold text-slate-300">{m.entity_name}</span>
                          <span>{m.timestamp}</span>
                        </div>
                        <p className="text-slate-200 text-xs italic">"{m.content}"</p>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

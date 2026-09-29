import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Wrench,
  Search,
  Filter,
  ArrowRight,
  Building2,
  MapPin,
  Clock,
  History,
  AlertTriangle,
  Brain,
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';
import type { Equipment } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';

export default function EquipmentListPage() {
  const navigate = useNavigate();
  const [equipmentList, setEquipmentList] = useState<Equipment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [categoryFilter, setCategoryFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadEquipment();
  }, []);

  async function loadEquipment() {
    try {
      setLoading(true);
      const data = await api.getEquipment();
      setEquipmentList(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load equipment list');
    } finally {
      setLoading(false);
    }
  }

  const categories = ['All', ...new Set(equipmentList.map((e) => e.category))];

  const filtered = equipmentList.filter((e) => {
    if (categoryFilter !== 'All' && e.category !== categoryFilter) return false;
    if (statusFilter !== 'All' && e.status !== statusFilter) return false;
    if (search.trim()) {
      const q = search.toLowerCase();
      const match =
        e.id.toLowerCase().includes(q) ||
        e.name.toLowerCase().includes(q) ||
        e.model.toLowerCase().includes(q) ||
        e.customer_name.toLowerCase().includes(q) ||
        e.site_name.toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorState message={error} onRetry={loadEquipment} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Wrench className="w-6 h-6 text-sky-400" />
            <span>Industrial Equipment Units ({equipmentList.length})</span>
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Browse installed equipment, inspect persistent memory timelines, and query historical knowledge.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex flex-col md:flex-row gap-4 justify-between items-stretch md:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by equipment name, model, customer, site..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <Filter className="w-3.5 h-3.5" />
            <span>Category:</span>
          </div>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
          >
            {categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>

          <span className="text-slate-700">|</span>

          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <span>Status:</span>
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
          >
            <option value="All">All Statuses</option>
            <option value="Operational">Operational</option>
            <option value="Degraded Performance">Degraded Performance</option>
            <option value="Under Service">Under Service</option>
            <option value="Critical">Critical</option>
          </select>
        </div>
      </div>

      {/* Equipment Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((eq) => (
          <div
            key={eq.id}
            onClick={() => navigate(`/equipment/${eq.id}`)}
            className="bg-slate-900 border border-slate-800 hover:border-sky-500/50 p-5 rounded-2xl cursor-pointer transition-all hover:shadow-xl hover:shadow-sky-500/5 flex flex-col justify-between space-y-4"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between gap-2">
                <span className="font-mono text-xs font-bold text-sky-400">#{eq.id}</span>
                <span
                  className={clsx(
                    'px-2 py-0.5 rounded text-[10px] font-semibold',
                    eq.status === 'Operational'
                      ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                      : eq.status === 'Degraded Performance'
                      ? 'bg-amber-500/15 text-amber-400 border border-amber-500/30'
                      : 'bg-rose-500/15 text-rose-400 border border-rose-500/30'
                  )}
                >
                  {eq.status}
                </span>
              </div>

              <h3 className="text-base font-bold text-white group-hover:text-sky-300">
                {eq.name}
              </h3>

              <p className="text-xs text-slate-400">
                Model: <span className="text-slate-200">{eq.model || 'Standard'}</span> · Category: <span className="text-slate-200">{eq.category}</span>
              </p>

              <div className="pt-2 border-t border-slate-800/80 space-y-1.5 text-xs text-slate-400">
                <div className="flex items-center gap-1.5">
                  <Building2 className="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                  <span className="truncate">{eq.customer_name}</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                  <span className="truncate">{eq.site_name}</span>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
              <div className="flex items-center gap-2 text-slate-500">
                <Clock className="w-3.5 h-3.5" />
                <span>{eq.operating_hours.toLocaleString()} hrs</span>
              </div>

              <div className="flex items-center gap-1.5 text-sky-400 font-semibold group-hover:translate-x-1 transition-transform">
                <span>Memory & History</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { MapPin, Search, Building2, Wrench, ArrowRight, ShieldAlert } from 'lucide-react';
import { api } from '../api';
import type { Site } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';

export default function SitesPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const customerIdParam = searchParams.get('customer_id');

  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadSites();
  }, [customerIdParam]);

  async function loadSites() {
    try {
      setLoading(true);
      const params = customerIdParam ? { customer_id: customerIdParam } : undefined;
      const data = await api.getSites(params);
      setSites(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load sites');
    } finally {
      setLoading(false);
    }
  }

  const filtered = sites.filter((s) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      s.name.toLowerCase().includes(q) ||
      s.city.toLowerCase().includes(q) ||
      s.customer_name.toLowerCase().includes(q)
    );
  });

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorState message={error} onRetry={loadSites} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <MapPin className="w-6 h-6 text-sky-400" />
            <span>Industrial Facilities & Plants ({sites.length})</span>
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Site-specific environmental factors, access constraints, and equipment configurations remembered by Hindsight.
          </p>
        </div>

        {customerIdParam && (
          <button
            onClick={() => navigate('/sites')}
            className="text-xs text-sky-400 hover:text-sky-300 self-start sm:self-auto"
          >
            Show All Sites
          </button>
        )}
      </div>

      <div className="relative max-w-md">
        <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="Search by facility name, city, customer..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((s) => (
          <div
            key={s.id}
            className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-4 flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-sky-400">#{s.id}</span>
                <span className="text-xs text-slate-400">{s.city}</span>
              </div>

              <h3 className="text-base font-bold text-white">{s.name}</h3>
              <p className="text-xs text-slate-400">
                Customer: <span className="text-slate-200 font-medium">{s.customer_name}</span>
              </p>

              <div className="space-y-1 text-xs text-slate-300 pt-1">
                <p>
                  <span className="text-slate-500 font-medium">Environment: </span>
                  {s.operating_environment}
                </p>
                {s.access_constraints && (
                  <p className="text-amber-400/90 bg-amber-500/10 p-2 rounded border border-amber-500/20 text-[11px]">
                    ⚠ {s.access_constraints}
                  </p>
                )}
              </div>
            </div>

            <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>{s.equipment_count} Equipment Units</span>
              <button
                onClick={() => navigate(`/equipment?site_id=${s.id}`)}
                className="text-sky-400 hover:text-sky-300 font-semibold flex items-center gap-1"
              >
                <span>View Equipment</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

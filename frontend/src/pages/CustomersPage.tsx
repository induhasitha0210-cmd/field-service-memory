import { useEffect, useState } from 'react';
import { Building2, Search, MapPin, Wrench, Shield, Phone, Mail, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';
import type { Customer } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';

export default function CustomersPage() {
  const navigate = useNavigate();
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadCustomers();
  }, []);

  async function loadCustomers() {
    try {
      setLoading(true);
      const data = await api.getCustomers();
      setCustomers(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load customers');
    } finally {
      setLoading(false);
    }
  }

  const filtered = customers.filter((c) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      c.name.toLowerCase().includes(q) ||
      c.industry.toLowerCase().includes(q) ||
      c.contact_name.toLowerCase().includes(q)
    );
  });

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorState message={error} onRetry={loadCustomers} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Building2 className="w-6 h-6 text-sky-400" />
          <span>Industrial Customers ({customers.length})</span>
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Organizations with active field service contracts and persistent facility knowledge.
        </p>
      </div>

      <div className="relative max-w-md">
        <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="Search by customer name, industry, contact..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((c) => (
          <div
            key={c.id}
            className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-4 flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-sky-400">#{c.id}</span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-500/10 text-sky-400 border border-sky-500/20">
                  {c.sla_level} SLA
                </span>
              </div>

              <h3 className="text-base font-bold text-white">{c.name}</h3>
              <p className="text-xs text-slate-400">Industry: <span className="text-slate-200">{c.industry}</span></p>

              {c.notes && (
                <p className="text-xs text-slate-400 bg-slate-950 p-2.5 rounded-lg border border-slate-800 leading-relaxed">
                  {c.notes}
                </p>
              )}
            </div>

            <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>{c.sites_count} Operational Sites</span>
              <button
                onClick={() => navigate(`/sites?customer_id=${c.id}`)}
                className="text-sky-400 hover:text-sky-300 font-semibold flex items-center gap-1"
              >
                <span>View Sites</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

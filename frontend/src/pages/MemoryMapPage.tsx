import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Brain,
  Building2,
  MapPin,
  Wrench,
  Ticket,
  Users,
  CheckCircle,
  AlertTriangle,
  ArrowRight,
  Database,
  Search,
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';
import type { Customer, Site, Equipment, ServiceRecord, Technician, MemoryItem } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';
import MemoryCard from '../components/MemoryCard';

export default function MemoryMapPage() {
  const navigate = useNavigate();
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [sites, setSites] = useState<Site[]>([]);
  const [equipments, setEquipments] = useState<Equipment[]>([]);
  const [technicians, setTechnicians] = useState<Technician[]>([]);
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Selected entities in the relationship hierarchy
  const [selectedCustomerId, setSelectedCustomerId] = useState<string>('');
  const [selectedSiteId, setSelectedSiteId] = useState<string>('');
  const [selectedEquipmentId, setSelectedEquipmentId] = useState<string>('');
  const [selectedTechnicianId, setSelectedTechnicianId] = useState<string>('');
  const [selectedEntityTitle, setSelectedEntityTitle] = useState<string>('All Organizational Memories');

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [cList, sList, eList, tList, mList] = await Promise.all([
          api.getCustomers(),
          api.getSites(),
          api.getEquipment(),
          api.getTechnicians(),
          api.getMemories(),
        ]);
        setCustomers(cList);
        setSites(sList);
        setEquipments(eList);
        setTechnicians(tList);
        setMemories(mList);

        if (cList.length > 0) {
          setSelectedCustomerId(cList[0].id);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load memory map data');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  // Filtered sites for chosen customer
  const filteredSites = sites.filter((s) => !selectedCustomerId || s.customer_id === selectedCustomerId);

  // Filtered equipment for chosen site
  const filteredEquipment = equipments.filter((e) => {
    if (selectedSiteId && e.site_id !== selectedSiteId) return false;
    if (selectedCustomerId && e.customer_id !== selectedCustomerId) return false;
    return true;
  });

  // Memories linked to currently focused entity
  const displayedMemories = memories.filter((m) => {
    if (selectedEquipmentId) {
      return m.entity_id === selectedEquipmentId;
    }
    if (selectedTechnicianId) {
      const tech = technicians.find((t) => t.id === selectedTechnicianId);
      return m.source_technician_name === tech?.name;
    }
    if (selectedSiteId) {
      return m.tags?.some((t) => t.includes(selectedSiteId));
    }
    if (selectedCustomerId) {
      return m.tags?.some((t) => t.includes(selectedCustomerId));
    }
    return true;
  });

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-sky-400 font-bold uppercase tracking-wider text-xs mb-1">
          <Brain className="w-4 h-4" />
          <span>Interactive Relationship Graph</span>
        </div>
        <h1 className="text-2xl font-bold text-white tracking-tight">
          Field Service Memory Map
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Explore the organizational knowledge hierarchy: Customer → Site → Equipment → Technicians → Retained Memories. Click any node to inspect grounded knowledge.
        </p>
      </div>

      {/* Visual Navigation Hierarchy Columns */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Column 1: Customers */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3">
          <div className="flex items-center gap-2 text-sky-400 text-xs font-bold uppercase tracking-wider">
            <Building2 className="w-4 h-4" />
            <span>1. Customers</span>
          </div>
          <div className="space-y-1.5 max-h-[380px] overflow-y-auto">
            {customers.map((c) => (
              <button
                key={c.id}
                onClick={() => {
                  setSelectedCustomerId(c.id);
                  setSelectedSiteId('');
                  setSelectedEquipmentId('');
                  setSelectedTechnicianId('');
                  setSelectedEntityTitle(`Customer: ${c.name}`);
                }}
                className={clsx(
                  'w-full text-left p-2.5 rounded-xl text-xs transition-all flex items-center justify-between',
                  selectedCustomerId === c.id
                    ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 font-semibold'
                    : 'text-slate-300 hover:bg-slate-800/60 border border-transparent'
                )}
              >
                <span className="truncate">{c.name}</span>
                <span className="text-[10px] text-slate-500">{c.sla_level}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Column 2: Sites */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3">
          <div className="flex items-center gap-2 text-indigo-400 text-xs font-bold uppercase tracking-wider">
            <MapPin className="w-4 h-4" />
            <span>2. Sites</span>
          </div>
          <div className="space-y-1.5 max-h-[380px] overflow-y-auto">
            {filteredSites.map((s) => (
              <button
                key={s.id}
                onClick={() => {
                  setSelectedSiteId(s.id);
                  setSelectedEquipmentId('');
                  setSelectedTechnicianId('');
                  setSelectedEntityTitle(`Site: ${s.name}`);
                }}
                className={clsx(
                  'w-full text-left p-2.5 rounded-xl text-xs transition-all flex items-center justify-between',
                  selectedSiteId === s.id
                    ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 font-semibold'
                    : 'text-slate-300 hover:bg-slate-800/60 border border-transparent'
                )}
              >
                <span className="truncate">{s.name}</span>
                <span className="text-[10px] text-slate-500">{s.city}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Column 3: Equipment */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3">
          <div className="flex items-center gap-2 text-emerald-400 text-xs font-bold uppercase tracking-wider">
            <Wrench className="w-4 h-4" />
            <span>3. Equipment Units</span>
          </div>
          <div className="space-y-1.5 max-h-[380px] overflow-y-auto">
            {filteredEquipment.map((eq) => (
              <button
                key={eq.id}
                onClick={() => {
                  setSelectedEquipmentId(eq.id);
                  setSelectedTechnicianId('');
                  setSelectedEntityTitle(`Equipment: ${eq.name} (${eq.category})`);
                }}
                className={clsx(
                  'w-full text-left p-2.5 rounded-xl text-xs transition-all flex items-center justify-between',
                  selectedEquipmentId === eq.id
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold'
                    : 'text-slate-300 hover:bg-slate-800/60 border border-transparent'
                )}
              >
                <div className="truncate">
                  <span className="block truncate">{eq.name}</span>
                  <span className="text-[10px] text-slate-500">{eq.category}</span>
                </div>
                <span className="text-[10px] text-slate-400">{eq.status}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Column 4: Contributing Technicians */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3">
          <div className="flex items-center gap-2 text-purple-400 text-xs font-bold uppercase tracking-wider">
            <Users className="w-4 h-4" />
            <span>4. Technicians</span>
          </div>
          <div className="space-y-1.5 max-h-[380px] overflow-y-auto">
            {technicians.map((t) => (
              <button
                key={t.id}
                onClick={() => {
                  setSelectedTechnicianId(t.id);
                  setSelectedEquipmentId('');
                  setSelectedEntityTitle(`Observations contributed by ${t.name}`);
                }}
                className={clsx(
                  'w-full text-left p-2.5 rounded-xl text-xs transition-all flex items-center justify-between',
                  selectedTechnicianId === t.id
                    ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40 font-semibold'
                    : 'text-slate-300 hover:bg-slate-800/60 border border-transparent'
                )}
              >
                <span className="truncate">{t.name}</span>
                <span className="text-[10px] text-slate-500">{t.role}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Linked Memories View */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <span className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold">
              Retrieved Memory Focus
            </span>
            <h3 className="text-base font-bold text-white mt-0.5">
              {selectedEntityTitle} ({displayedMemories.length} Memories)
            </h3>
          </div>

          <button
            onClick={() => {
              setSelectedCustomerId('');
              setSelectedSiteId('');
              setSelectedEquipmentId('');
              setSelectedTechnicianId('');
              setSelectedEntityTitle('All Organizational Memories');
            }}
            className="text-xs text-sky-400 hover:text-sky-300"
          >
            Clear Filters / Show All
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {displayedMemories.length === 0 ? (
            <p className="col-span-full p-8 text-center text-slate-500 text-xs">
              No specific memories associated with this selected entity. Select another node above.
            </p>
          ) : (
            displayedMemories.map((m) => <MemoryCard key={m.id} item={m} />)
          )}
        </div>
      </div>
    </div>
  );
}

import { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, Ticket, Users, Building2, MapPin, Wrench,
  Brain, BarChart3, Play, Settings, Database, Network
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, exact: true },
  { to: '/service-requests', label: 'Service Requests', icon: Ticket },
  { to: '/technicians', label: 'Technicians', icon: Users },
  { to: '/customers', label: 'Customers', icon: Building2 },
  { to: '/sites', label: 'Sites', icon: MapPin },
  { to: '/equipment', label: 'Equipment', icon: Wrench },
  { to: '/memory', label: 'Memory Explorer', icon: Brain },
  { to: '/memory-map', label: 'Memory Map', icon: Network },
  { to: '/insights', label: 'Insights', icon: BarChart3 },
  { to: '/demo', label: 'Demo Mode', icon: Play },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
  const [hindsight, setHindsight] = useState<{ hindsight_available?: boolean; bank_id?: string; mode?: string } | null>(null);

  useEffect(() => {
    api.getHindsightStatus().then(setHindsight).catch(() => setHindsight(null));
  }, []);

  return (
    <aside className="w-60 flex-shrink-0 bg-slate-900 border-r border-slate-800 flex flex-col h-full">
      {/* Logo */}
      <div className="px-4 py-5 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-sky-400 flex-shrink-0" />
          <span className="text-sky-400 font-bold text-sm tracking-wide leading-tight">
            FIELD SERVICE MEMORY
          </span>
        </div>
        <p className="text-slate-500 text-xs mt-1 leading-tight pl-7">The Technician Who Never Forgets</p>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-2 py-4 space-y-0.5 overflow-y-auto">
        {navItems.map(({ to, label, icon: Icon, exact }) => (
          <NavLink
            key={to}
            to={to}
            end={exact}
            className={({ isActive }) =>
              clsx(
                'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all',
                isActive
                  ? 'bg-sky-500/10 text-sky-400 border-l-2 border-sky-400 pl-[10px]'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border-l-2 border-transparent'
              )
            }
          >
            <Icon className="w-4 h-4 flex-shrink-0" />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Memory Engine footer */}
      <div className="border-t border-slate-800 px-4 py-3">
        <div className="flex items-center gap-2">
          <Database className="w-3.5 h-3.5 text-slate-500" />
          <span className="text-slate-500 text-xs font-semibold uppercase tracking-wide">Memory Engine</span>
        </div>
        <div className="flex items-center gap-2 mt-2">
          <span
            className={clsx(
              'inline-block w-2 h-2 rounded-full flex-shrink-0',
              hindsight?.hindsight_available ? 'bg-emerald-400' : 'bg-amber-400'
            )}
          />
          <span className="text-slate-400 text-xs">
            {hindsight?.hindsight_available ? 'Hindsight Live' : hindsight?.mode === 'demo' ? 'Demo Mode' : 'Local Fallback'}
          </span>
        </div>
        {hindsight?.bank_id && (
          <p className="text-slate-600 text-[10px] mt-1 font-mono truncate">{hindsight.bank_id}</p>
        )}
      </div>
    </aside>
  );
}

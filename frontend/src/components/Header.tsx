import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Brain,
  Shield,
  UserCheck,
  Radio,
  Play,
  Search,
  Database,
  ExternalLink,
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';

export type UserRole = 'manager' | 'technician' | 'dispatcher';

interface HeaderProps {
  currentRole: UserRole;
  onRoleChange: (role: UserRole) => void;
}

export default function Header({ currentRole, onRoleChange }: HeaderProps) {
  const navigate = useNavigate();
  const [hindsightStatus, setHindsightStatus] = useState<{
    hindsight_available?: boolean;
    bank_id?: string;
    mode?: string;
  } | null>(null);

  useEffect(() => {
    api.getHindsightStatus()
      .then(setHindsightStatus)
      .catch(() => setHindsightStatus(null));
  }, []);

  return (
    <header className="h-14 bg-slate-900/90 backdrop-blur border-b border-slate-800 px-6 flex items-center justify-between z-20">
      {/* Left: Role Switcher */}
      <div className="flex items-center gap-3">
        <span className="text-xs text-slate-400 font-medium uppercase tracking-wider hidden sm:inline">
          Active Role:
        </span>
        <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => onRoleChange('manager')}
            className={clsx(
              'flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all',
              currentRole === 'manager'
                ? 'bg-sky-500 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            )}
            title="Service Manager / Admin"
          >
            <Shield className="w-3.5 h-3.5" />
            <span>Service Manager</span>
          </button>
          <button
            onClick={() => onRoleChange('technician')}
            className={clsx(
              'flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all',
              currentRole === 'technician'
                ? 'bg-sky-500 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            )}
            title="Field Technician"
          >
            <UserCheck className="w-3.5 h-3.5" />
            <span>Technician</span>
          </button>
          <button
            onClick={() => onRoleChange('dispatcher')}
            className={clsx(
              'flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all',
              currentRole === 'dispatcher'
                ? 'bg-sky-500 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            )}
            title="Dispatcher"
          >
            <Radio className="w-3.5 h-3.5" />
            <span>Dispatcher</span>
          </button>
        </div>
      </div>

      {/* Right: Quick actions & Hindsight status */}
      <div className="flex items-center gap-3">
        {/* Quick Demo CTA */}
        <button
          onClick={() => navigate('/demo')}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white rounded-lg text-xs font-semibold shadow-sm transition-all"
        >
          <Play className="w-3.5 h-3.5 fill-current" />
          <span>Run Memory Demo</span>
        </button>

        {/* Hindsight Engine Status Badge */}
        <div
          onClick={() => navigate('/settings')}
          className="cursor-pointer flex items-center gap-2 px-2.5 py-1 bg-slate-950 border border-slate-800 rounded-lg hover:border-slate-700 transition-colors"
          title="Click to view Hindsight Memory Engine settings & diagnostics"
        >
          <span
            className={clsx(
              'w-2 h-2 rounded-full',
              hindsightStatus?.hindsight_available ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'
            )}
          />
          <div className="flex flex-col text-left">
            <span className="text-[11px] font-medium text-slate-300">
              {hindsightStatus?.hindsight_available ? 'Hindsight Live' : 'Hindsight Local'}
            </span>
          </div>
          <Database className="w-3 h-3 text-slate-500 ml-0.5" />
        </div>
      </div>
    </header>
  );
}

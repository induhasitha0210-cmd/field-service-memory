import { RefreshCw } from 'lucide-react';
import type { MemoryItem } from '../types';
import clsx from 'clsx';

const typeColors: Record<string, string> = {
  equipment_pattern: 'bg-sky-500/15 text-sky-400 border-sky-500/30',
  resolution: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  technician_observation: 'bg-purple-500/15 text-purple-400 border-purple-500/30',
  recurring_issue: 'bg-red-500/15 text-red-400 border-red-500/30',
  site_pattern: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
};

const typeLabels: Record<string, string> = {
  equipment_pattern: 'Equipment Pattern',
  resolution: 'Resolution',
  technician_observation: 'Observation',
  recurring_issue: 'Recurring Issue',
  site_pattern: 'Site Pattern',
};

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

export default function MemoryCard({ memory, item }: { memory?: MemoryItem; item?: MemoryItem }) {
  const mem = memory || item;
  if (!mem) return null;

  const typeClass = typeColors[mem.memory_type] ?? 'bg-slate-500/15 text-slate-400 border-slate-500/30';
  const typeLabel = typeLabels[mem.memory_type] ?? mem.memory_type.replace(/_/g, ' ');

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col gap-3 hover:border-slate-700 transition-colors">
      <div className="flex items-start justify-between gap-2">
        <span className={clsx('inline-flex items-center px-2 py-0.5 rounded border text-xs font-medium flex-shrink-0', typeClass)}>
          {typeLabel}
        </span>
        {mem.recurrence_flag && (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded border text-xs font-medium bg-amber-500/15 text-amber-400 border-amber-500/30">
            <RefreshCw className="w-3 h-3" />
            Recurring
          </span>
        )}
      </div>
      <h3 className="text-slate-100 text-sm font-semibold leading-snug">{mem.title}</h3>
      <p className="text-slate-400 text-xs leading-relaxed line-clamp-3">{mem.content}</p>
      <div className="flex items-center justify-between text-xs text-slate-500 border-t border-slate-800 pt-2 mt-auto gap-2 flex-wrap">
        <span className="text-sky-400/80 truncate max-w-[120px]">{mem.entity_name}</span>
        {mem.source_technician_name && (
          <span className="truncate max-w-[100px]">{mem.source_technician_name}</span>
        )}
        <span>{formatDate(mem.timestamp)}</span>
        <span className="text-slate-400">{Math.round(mem.confidence * 100)}% conf</span>
      </div>
    </div>
  );
}

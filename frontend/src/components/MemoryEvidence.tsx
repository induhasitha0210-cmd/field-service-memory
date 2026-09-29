import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import type { MemoryEvidence as MemoryEvidenceType } from '../types';
import clsx from 'clsx';

const typeColors: Record<string, string> = {
  equipment_pattern: 'bg-sky-500/15 text-sky-400 border-sky-500/30',
  resolution: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  technician_observation: 'bg-purple-500/15 text-purple-400 border-purple-500/30',
  recurring_issue: 'bg-red-500/15 text-red-400 border-red-500/30',
  site_pattern: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
};

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

function EvidenceItem({ item }: { item: MemoryEvidenceType }) {
  const [open, setOpen] = useState(false);
  const typeClass = typeColors[item.memory_type] ?? 'bg-slate-500/15 text-slate-400 border-slate-500/30';
  const confidencePct = Math.round(item.confidence * 100);

  return (
    <div className="border border-slate-700 rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between gap-3 p-3 text-left hover:bg-slate-800/50 transition-colors"
      >
        <div className="flex items-center gap-2 min-w-0">
          <span className={clsx('inline-flex items-center px-1.5 py-0.5 rounded border text-[10px] font-medium flex-shrink-0', typeClass)}>
            {item.memory_type.replace(/_/g, ' ')}
          </span>
          <span className="text-slate-200 text-xs font-medium truncate">{item.title}</span>
        </div>
        <span className="text-slate-500 flex-shrink-0">
          {open ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </span>
      </button>

      {open && (
        <div className="border-t border-slate-700 p-3 space-y-3 bg-slate-800/30">
          <p className="text-slate-300 text-xs leading-relaxed">{item.content}</p>

          {item.why_matched && (
            <p className="text-sky-400/80 text-xs italic">💡 {item.why_matched}</p>
          )}

          <div className="flex items-center gap-4 text-xs text-slate-500 flex-wrap">
            {item.source_technician_name && (
              <span>By: <span className="text-slate-300">{item.source_technician_name}</span></span>
            )}
            <span>{formatDate(item.timestamp)}</span>
            {item.outcome_status && (
              <span className={clsx('px-1.5 py-0.5 rounded text-[10px]',
                item.outcome_status === 'Resolved' ? 'bg-emerald-500/15 text-emerald-400' :
                item.outcome_status === 'Temporarily Resolved' ? 'bg-amber-500/15 text-amber-400' :
                'bg-red-500/15 text-red-400'
              )}>
                {item.outcome_status}
              </span>
            )}
          </div>

          <div>
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="text-slate-500">Confidence</span>
              <span className="text-slate-300">{confidencePct}%</span>
            </div>
            <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
              <div
                className={clsx('h-full rounded-full transition-all', confidencePct >= 80 ? 'bg-emerald-500' : confidencePct >= 60 ? 'bg-sky-500' : 'bg-amber-500')}
                style={{ width: `${confidencePct}%` }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

interface Props {
  evidence: MemoryEvidenceType[];
}

export default function MemoryEvidence({ evidence }: Props) {
  if (!evidence || evidence.length === 0) return null;
  return (
    <div className="space-y-2">
      <h4 className="text-slate-400 text-xs font-semibold uppercase tracking-wide">
        Memory Evidence ({evidence.length} items)
      </h4>
      <div className="space-y-1.5">
        {evidence.map((item) => (
          <EvidenceItem key={item.memory_id} item={item} />
        ))}
      </div>
    </div>
  );
}

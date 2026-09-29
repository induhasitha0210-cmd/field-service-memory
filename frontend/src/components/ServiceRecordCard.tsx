import clsx from 'clsx';
import type { ServiceRecord } from '../types';

const outcomeColors: Record<string, string> = {
  Resolved: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  'Temporarily Resolved': 'bg-amber-500/15 text-amber-400 border-amber-500/30',
  Unresolved: 'bg-red-500/15 text-red-400 border-red-500/30',
  'Requires Escalation': 'bg-purple-500/15 text-purple-400 border-purple-500/30',
};

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

export default function ServiceRecordCard({ record }: { record: ServiceRecord }) {
  const outcomeClass = outcomeColors[record.outcome] ?? 'bg-slate-500/15 text-slate-400 border-slate-500/30';
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <span className="text-slate-100 text-sm font-semibold">{record.technician_name}</span>
          <span className="text-slate-500 text-xs ml-2">{formatDate(record.visit_date)}</span>
        </div>
        <span className={clsx('inline-flex items-center px-2 py-0.5 rounded border text-xs font-medium', outcomeClass)}>
          {record.outcome}
        </span>
      </div>

      <div className="grid grid-cols-1 gap-2 text-xs">
        {record.symptoms_observed && (
          <div>
            <span className="text-slate-500 uppercase tracking-wide text-[10px]">Symptoms</span>
            <p className="text-slate-300 mt-0.5">{record.symptoms_observed}</p>
          </div>
        )}
        {record.action_taken && (
          <div>
            <span className="text-slate-500 uppercase tracking-wide text-[10px]">Action Taken</span>
            <p className="text-slate-300 mt-0.5">{record.action_taken}</p>
          </div>
        )}
        {record.parts_replaced && (
          <div>
            <span className="text-slate-500 uppercase tracking-wide text-[10px]">Parts Replaced</span>
            <p className="text-slate-300 mt-0.5">{record.parts_replaced}</p>
          </div>
        )}
        {record.effective_duration_days !== null && record.effective_duration_days !== undefined && (
          <div>
            <span className="text-slate-500 uppercase tracking-wide text-[10px]">Effective Duration</span>
            <p className="text-amber-400 mt-0.5">{record.effective_duration_days} days before recurrence</p>
          </div>
        )}
        {record.technician_notes && (
          <div>
            <span className="text-slate-500 uppercase tracking-wide text-[10px]">Notes</span>
            <p className="text-slate-400 mt-0.5 italic">{record.technician_notes}</p>
          </div>
        )}
      </div>
    </div>
  );
}

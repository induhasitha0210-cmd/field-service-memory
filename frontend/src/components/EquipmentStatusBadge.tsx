import clsx from 'clsx';

type StatusType = 'Operational' | 'Degraded Performance' | 'Under Service' | 'Critical' | string;

const statusConfig: Record<string, { label: string; classes: string }> = {
  Operational: { label: 'Operational', classes: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30' },
  'Degraded Performance': { label: 'Degraded', classes: 'bg-amber-500/15 text-amber-400 border-amber-500/30' },
  'Under Service': { label: 'Under Service', classes: 'bg-sky-500/15 text-sky-400 border-sky-500/30' },
  Critical: { label: 'Critical', classes: 'bg-red-500/15 text-red-400 border-red-500/30' },
};

export default function EquipmentStatusBadge({ status }: { status: StatusType }) {
  const cfg = statusConfig[status] ?? { label: status, classes: 'bg-slate-500/15 text-slate-400 border-slate-500/30' };
  return (
    <span className={clsx('inline-flex items-center px-2 py-0.5 rounded border text-xs font-medium', cfg.classes)}>
      {cfg.label}
    </span>
  );
}

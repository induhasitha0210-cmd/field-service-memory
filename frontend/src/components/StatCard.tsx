import type { ReactNode } from 'react';
import clsx from 'clsx';

interface Props {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: ReactNode;
  color?: 'sky' | 'emerald' | 'amber' | 'red' | 'slate';
}

const colorMap = {
  sky: 'text-sky-400 bg-sky-500/10',
  emerald: 'text-emerald-400 bg-emerald-500/10',
  amber: 'text-amber-400 bg-amber-500/10',
  red: 'text-red-400 bg-red-500/10',
  slate: 'text-slate-400 bg-slate-500/10',
};

const valueColorMap = {
  sky: 'text-sky-300',
  emerald: 'text-emerald-300',
  amber: 'text-amber-300',
  red: 'text-red-300',
  slate: 'text-slate-200',
};

export default function StatCard({ title, value, subtitle, icon, color = 'slate' }: Props) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex items-start gap-4">
      <div className={clsx('p-2.5 rounded-lg flex-shrink-0', colorMap[color])}>
        <span className={clsx('w-5 h-5 block', colorMap[color].split(' ')[0])}>{icon}</span>
      </div>
      <div className="min-w-0">
        <p className="text-slate-400 text-xs font-medium uppercase tracking-wide">{title}</p>
        <p className={clsx('text-2xl font-bold mt-1', valueColorMap[color])}>{value}</p>
        {subtitle && <p className="text-slate-500 text-xs mt-1 truncate">{subtitle}</p>}
      </div>
    </div>
  );
}

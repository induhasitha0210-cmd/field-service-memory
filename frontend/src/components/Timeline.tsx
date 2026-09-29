import clsx from 'clsx';
import type { TimelineEvent } from '../types';

const dotColors: Record<string, string> = {
  install: 'bg-emerald-500 border-emerald-400',
  service: 'bg-sky-500 border-sky-400',
  temporary: 'bg-amber-500 border-amber-400',
  unresolved: 'bg-red-500 border-red-400',
  default: 'bg-slate-500 border-slate-400',
};

const labelColors: Record<string, string> = {
  install: 'text-emerald-400',
  service: 'text-sky-400',
  temporary: 'text-amber-400',
  unresolved: 'text-red-400',
  default: 'text-slate-400',
};

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

export default function Timeline({ events }: { events: TimelineEvent[] }) {
  if (!events || events.length === 0) {
    return <p className="text-slate-500 text-sm py-4">No timeline events available.</p>;
  }

  let lastYear = '';

  return (
    <div className="relative pl-6">
      {/* Vertical connector line */}
      <div className="absolute left-2 top-2 bottom-2 w-px bg-slate-800" />

      <div className="space-y-0">
        {events.map((event) => {
          const year = new Date(event.date).getFullYear().toString();
          const showYearSep = year !== lastYear;
          lastYear = year;
          const dotClass = dotColors[event.event_type] ?? dotColors.default;
          const labelClass = labelColors[event.event_type] ?? labelColors.default;

          return (
            <div key={event.id}>
              {showYearSep && (
                <div className="flex items-center gap-3 py-2 -ml-6 pl-6">
                  <span className="text-slate-600 text-xs font-bold uppercase tracking-widest">{year}</span>
                  <div className="flex-1 h-px bg-slate-800" />
                </div>
              )}
              <div className="relative flex gap-4 pb-6">
                {/* Dot */}
                <div className={clsx('absolute -left-4 top-1 w-3 h-3 rounded-full border-2 flex-shrink-0 z-10', dotClass)} />
                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2 flex-wrap">
                    <span className={clsx('text-xs font-semibold', labelClass)}>{event.title}</span>
                    <span className="text-slate-600 text-xs flex-shrink-0">{formatDate(event.date)}</span>
                  </div>
                  {event.description && (
                    <p className="text-slate-400 text-xs mt-1 leading-relaxed">{event.description}</p>
                  )}
                  <div className="flex items-center gap-3 mt-1 flex-wrap">
                    {event.technician && (
                      <span className="text-slate-500 text-xs">By {event.technician}</span>
                    )}
                    {event.outcome && (
                      <span className={clsx('text-xs px-1.5 py-0.5 rounded',
                        event.outcome === 'Resolved' ? 'bg-emerald-500/15 text-emerald-400' :
                        event.outcome === 'Temporarily Resolved' ? 'bg-amber-500/15 text-amber-400' :
                        event.outcome === 'Unresolved' ? 'bg-red-500/15 text-red-400' :
                        'bg-slate-500/15 text-slate-400'
                      )}>
                        {event.outcome}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

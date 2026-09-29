import { Brain, Zap, CheckCircle, AlertTriangle, MessageSquare, ArrowRight, Database } from 'lucide-react';
import type { AgentContext } from '../types';
import MemoryEvidence from './MemoryEvidence';
import clsx from 'clsx';

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

export default function AgentInsightCard({ ctx }: { ctx: AgentContext }) {
  const { hindsight_engine_info: hei } = ctx;
  return (
    <div className="bg-slate-900 border border-sky-500/30 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="bg-sky-500/10 border-b border-sky-500/20 px-4 py-3 flex items-center gap-2">
        <Brain className="w-4 h-4 text-sky-400" />
        <span className="text-sky-400 text-xs font-bold uppercase tracking-widest">Field Service Memory</span>
      </div>

      {/* Has seen before banner */}
      {ctx.has_seen_before && (
        <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-3 flex items-center gap-2">
          <Zap className="w-4 h-4 text-amber-400" />
          <div>
            <span className="text-amber-300 text-sm font-bold">⚡ Equipment Recognized</span>
            <span className="text-amber-500 text-xs ml-2">
              {ctx.recurrence_count > 0 ? `${ctx.recurrence_count} similar incidents on record` : 'Seen before'}
            </span>
          </div>
        </div>
      )}

      <div className="p-4 space-y-4">
        {/* What memory says */}
        {ctx.what_the_memory_says && (
          <blockquote className="border-l-2 border-sky-500 pl-3">
            <p className="text-slate-300 text-sm italic leading-relaxed">"{ctx.what_the_memory_says}"</p>
          </blockquote>
        )}

        {/* Previously successful */}
        {ctx.previously_successful && ctx.previously_successful.length > 0 && (
          <div>
            <h4 className="text-emerald-400 text-xs font-semibold uppercase tracking-wide mb-2">✓ What Worked</h4>
            <ul className="space-y-1">
              {ctx.previously_successful.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0" />
                  <span className="text-slate-300">
                    {item.action}
                    {(item.duration_days ?? 0) > 0 && (
                      <span className="text-emerald-500 ml-1">(lasted {item.duration_days} days)</span>
                    )}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Previously tried */}
        {ctx.previously_tried && ctx.previously_tried.length > 0 && (
          <div>
            <h4 className="text-slate-400 text-xs font-semibold uppercase tracking-wide mb-2">Previously Tried</h4>
            <ul className="space-y-1">
              {ctx.previously_tried.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs">
                  <span className="text-slate-500 mt-0.5 flex-shrink-0">→</span>
                  <span className="text-slate-300">
                    {item.action}
                    {item.date && <span className="text-slate-500 ml-1">({formatDate(item.date)})</span>}
                    {item.outcome && <span className="text-slate-500 ml-1">— {item.outcome}</span>}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Previously failed */}
        {ctx.previously_failed && ctx.previously_failed.length > 0 && (
          <div>
            <h4 className="text-amber-400 text-xs font-semibold uppercase tracking-wide mb-2">⚠ Known Failures</h4>
            <ul className="space-y-1">
              {ctx.previously_failed.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-400 mt-0.5 flex-shrink-0" />
                  <span className="text-slate-300">
                    {item.action}
                    {item.reason && <span className="text-amber-500/80 ml-1">— {item.reason}</span>}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Technician observations */}
        {ctx.technician_observations && ctx.technician_observations.length > 0 && (
          <div>
            <h4 className="text-purple-400 text-xs font-semibold uppercase tracking-wide mb-2">💬 Technician Observations</h4>
            <ul className="space-y-2">
              {ctx.technician_observations.map((obs, i) => (
                <li key={i} className="flex items-start gap-2 text-xs">
                  <MessageSquare className="w-3.5 h-3.5 text-purple-400 mt-0.5 flex-shrink-0" />
                  <div>
                    <span className="text-slate-300 italic">"{obs.observation}"</span>
                    <span className="text-slate-500 ml-1">— {obs.technician}</span>
                    {obs.date && <span className="text-slate-600 ml-1">({formatDate(obs.date)})</span>}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Historical outcomes */}
        {ctx.historical_outcomes && ctx.historical_outcomes.length > 0 && (
          <div>
            <h4 className="text-slate-400 text-xs font-semibold uppercase tracking-wide mb-2">Historical Outcomes</h4>
            <ol className="space-y-1">
              {ctx.historical_outcomes.map((outcome, i) => (
                <li key={i} className="flex items-start gap-2 text-xs">
                  <span className="text-slate-500 font-mono">{i + 1}.</span>
                  <span className="text-slate-300">{outcome}</span>
                </li>
              ))}
            </ol>
          </div>
        )}

        {/* Suggested investigation */}
        {ctx.suggested_investigation && ctx.suggested_investigation.length > 0 && (
          <div>
            <h4 className="text-sky-400 text-xs font-semibold uppercase tracking-wide mb-2">→ Suggested Investigation</h4>
            <ul className="space-y-1">
              {ctx.suggested_investigation.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs">
                  <ArrowRight className="w-3.5 h-3.5 text-sky-400 mt-0.5 flex-shrink-0" />
                  <span className="text-slate-300">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Evidence */}
        {ctx.evidence && ctx.evidence.length > 0 && (
          <div className="border-t border-slate-800 pt-4">
            <MemoryEvidence evidence={ctx.evidence} />
          </div>
        )}
      </div>

      {/* Footer */}
      <div className={clsx(
        'px-4 py-2 border-t border-slate-800 flex items-center justify-between flex-wrap gap-2',
        hei.hindsight_available ? 'bg-slate-950' : 'bg-amber-900/10'
      )}>
        <div className="flex items-center gap-1.5 text-xs text-slate-500">
          <Database className="w-3 h-3" />
          <span>Powered by Hindsight Memory Engine</span>
          {hei.bank_id && <span className="text-slate-600">· {hei.bank_id}</span>}
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className={clsx('font-medium', hei.hindsight_available ? 'text-emerald-400' : 'text-amber-400')}>
            {hei.hindsight_available ? '● Live' : '● Local'}
          </span>
          <span className="text-slate-600">{hei.memories_retrieved} memories retrieved</span>
        </div>
      </div>
    </div>
  );
}

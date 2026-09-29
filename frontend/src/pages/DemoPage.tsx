import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Play,
  RotateCcw,
  CheckCircle2,
  Brain,
  Wrench,
  Clock,
  Database,
  ArrowRight,
  Sparkles,
  Zap,
  ShieldCheck,
  ChevronRight,
  ChevronLeft,
} from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';
import type { DemoResult, DemoStep } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';

export default function DemoPage() {
  const navigate = useNavigate();
  const [demoResult, setDemoResult] = useState<DemoResult | null>(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [isRunning, setIsRunning] = useState(false);
  const [autoPlay, setAutoPlay] = useState(false);

  useEffect(() => {
    // Auto-run once upon page load so judge immediately sees the demo ready
    handleRunDemo();
  }, []);

  useEffect(() => {
    let timer: any;
    if (autoPlay && demoResult && currentStep < demoResult.steps.length) {
      timer = setTimeout(() => {
        setCurrentStep((s) => s + 1);
      }, 3500);
    } else if (currentStep >= (demoResult?.steps.length ?? 9)) {
      setAutoPlay(false);
    }
    return () => clearTimeout(timer);
  }, [autoPlay, currentStep, demoResult]);

  async function handleRunDemo() {
    try {
      setIsRunning(true);
      const res = await api.runDemo();
      setDemoResult(res);
      setCurrentStep(1);
    } catch (err: any) {
      alert(`Demo run error: ${err.message}`);
    } finally {
      setIsRunning(false);
    }
  }

  const activeStepData: DemoStep | undefined = demoResult?.steps.find(
    (s) => s.step === currentStep
  );

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/20 text-sky-400 text-xs font-semibold tracking-wide mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI COMPETITION EVALUATION SHOWCASE</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Field Service Memory Demo: The 9-Step Lifecycle
          </h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Experience how persistent organizational memory preserves field knowledge, connects past visits, and prevents repeated repair mistakes.
          </p>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setAutoPlay((a) => !a)}
            className={clsx(
              'px-4 py-2 rounded-xl text-xs font-semibold border transition-all flex items-center gap-1.5',
              autoPlay
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
            )}
          >
            <Play className="w-3.5 h-3.5" />
            <span>{autoPlay ? 'Pause Auto-Play' : 'Auto-Play Story'}</span>
          </button>

          <button
            onClick={handleRunDemo}
            disabled={isRunning}
            className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-sky-500/20 transition-all disabled:opacity-50"
          >
            <RotateCcw className={clsx('w-3.5 h-3.5', isRunning && 'animate-spin')} />
            <span>{isRunning ? 'Running Demo...' : 'Restart Demo'}</span>
          </button>
        </div>
      </div>

      {/* Progress Stepper Bar */}
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl overflow-x-auto">
        <div className="flex items-center justify-between min-w-[700px] gap-2">
          {demoResult?.steps.map((st) => {
            const isDone = st.step < currentStep;
            const isCurrent = st.step === currentStep;

            return (
              <button
                key={st.step}
                onClick={() => setCurrentStep(st.step)}
                className="flex-1 flex flex-col items-center text-center group transition-all"
              >
                <div
                  className={clsx(
                    'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all mb-2',
                    isCurrent
                      ? 'bg-sky-500 text-white ring-4 ring-sky-500/20 scale-110 shadow-lg shadow-sky-500/30'
                      : isDone
                      ? 'bg-emerald-500 text-white'
                      : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700'
                  )}
                >
                  {isDone ? <CheckCircle2 className="w-4 h-4" /> : st.step}
                </div>
                <span
                  className={clsx(
                    'text-[11px] font-medium leading-tight line-clamp-1',
                    isCurrent ? 'text-sky-400 font-bold' : isDone ? 'text-slate-300' : 'text-slate-500'
                  )}
                >
                  Step {st.step}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Active Step Feature Showcase */}
      {activeStepData && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Main Visual Display (8 cols) */}
          <div className="lg:col-span-8 bg-slate-900 border border-sky-500/30 rounded-2xl p-6 shadow-2xl relative overflow-hidden space-y-6">
            <div className="flex items-center justify-between">
              <span className="px-3 py-1 bg-sky-500/10 border border-sky-500/20 text-sky-400 rounded-full text-xs font-bold uppercase tracking-wider">
                Step {activeStepData.step} of 9
              </span>
              <span className="text-xs text-slate-400">
                Target: <span className="text-white font-medium">HVAC-204 at ABC Manufacturing</span>
              </span>
            </div>

            <div>
              <h2 className="text-xl sm:text-2xl font-extrabold text-white">
                {activeStepData.title}
              </h2>
              <p className="text-slate-300 text-sm mt-2 leading-relaxed">
                {activeStepData.description}
              </p>
            </div>

            {/* Step Data Inspection Box */}
            {activeStepData.data && (
              <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 font-mono text-xs text-slate-300 space-y-2">
                <div className="flex items-center justify-between text-slate-500 text-[11px] pb-1 border-b border-slate-800 font-sans font-semibold uppercase">
                  <span>Hindsight Event Payload / Diagnostic Log</span>
                  <Database className="w-3.5 h-3.5 text-sky-400" />
                </div>
                <pre className="overflow-x-auto text-[11px] text-sky-300 leading-relaxed font-mono">
                  {JSON.stringify(activeStepData.data, null, 2)}
                </pre>
              </div>
            )}

            {/* Special Highlight for Step 6: 'I Remember This Equipment' */}
            {activeStepData.step === 6 && (
              <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-xl flex items-center gap-3">
                <Zap className="w-6 h-6 text-amber-400 flex-shrink-0 animate-pulse" />
                <div>
                  <h4 className="text-amber-300 text-sm font-bold">
                    "I've seen this before."
                  </h4>
                  <p className="text-slate-300 text-xs">
                    The agent instantly recognizes that HVAC-204 had 2 prior visits. It flags that the previous filter swap provided only temporary relief for 21 days!
                  </p>
                </div>
              </div>
            )}

            {/* Step Navigation Controls */}
            <div className="flex items-center justify-between pt-4 border-t border-slate-800">
              <button
                onClick={() => setCurrentStep((s) => Math.max(1, s - 1))}
                disabled={currentStep === 1}
                className="flex items-center gap-1.5 px-4 py-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-30 text-slate-300 rounded-xl text-xs font-semibold transition-all"
              >
                <ChevronLeft className="w-4 h-4" />
                <span>Previous Step</span>
              </button>

              <div className="flex items-center gap-2">
                {demoResult?.service_request_id && (
                  <button
                    onClick={() => navigate(`/service-requests/${demoResult.service_request_id}`)}
                    className="flex items-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold shadow transition-all"
                  >
                    <Wrench className="w-3.5 h-3.5" />
                    <span>Open in Technician Workspace</span>
                  </button>
                )}

                <button
                  onClick={() => setCurrentStep((s) => Math.min(demoResult?.steps.length ?? 9, s + 1))}
                  disabled={currentStep === (demoResult?.steps.length ?? 9)}
                  className="flex items-center gap-1.5 px-4 py-2 bg-sky-500 hover:bg-sky-400 disabled:opacity-30 text-white rounded-xl text-xs font-semibold shadow transition-all"
                >
                  <span>Next Step</span>
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          {/* Right Summary Sidebar (4 cols) */}
          <div className="lg:col-span-4 space-y-6">
            {/* Why This Matters for Competition */}
            <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-3">
              <div className="flex items-center gap-2 text-sky-400">
                <Brain className="w-4 h-4" />
                <h3 className="text-xs font-bold uppercase tracking-wider">
                  The Competition Differentiator
                </h3>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                Traditional field service tickets are dead archives. A new technician arrives 6 months later and repeats the same failed steps.
              </p>
              <p className="text-xs text-slate-300 leading-relaxed">
                With <span className="text-sky-300 font-semibold">Hindsight</span>, the organization learns: technician observations (like Ravi's note on vibration) become active organizational guidance, steering the next technician to the real root cause.
              </p>
            </div>

            {/* Quick Flow Checklist */}
            <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-3">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider">
                Full 9-Step Sequence
              </h3>
              <div className="space-y-2 text-xs">
                {demoResult?.steps.map((st) => (
                  <div
                    key={st.step}
                    onClick={() => setCurrentStep(st.step)}
                    className={clsx(
                      'p-2 rounded-lg cursor-pointer flex items-center gap-2 transition-all',
                      st.step === currentStep
                        ? 'bg-sky-500/15 text-sky-300 border border-sky-500/30'
                        : st.step < currentStep
                        ? 'text-slate-400 hover:bg-slate-800'
                        : 'text-slate-600'
                    )}
                  >
                    <span className="w-5 h-5 rounded-full bg-slate-800 flex items-center justify-center text-[10px] font-bold">
                      {st.step}
                    </span>
                    <span className="truncate">{st.title}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

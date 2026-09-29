import { Loader2 } from 'lucide-react';

export default function LoadingSpinner({ message = 'Loading...' }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16">
      <Loader2 className="w-8 h-8 text-sky-400 animate-spin" />
      <span className="text-slate-400 text-sm">{message}</span>
    </div>
  );
}

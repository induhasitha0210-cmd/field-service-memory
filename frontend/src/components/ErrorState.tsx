import { AlertTriangle, RefreshCw } from 'lucide-react';

interface Props {
  message?: string;
  onRetry?: () => void;
}

export default function ErrorState({ message = 'Something went wrong.', onRetry }: Props) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-16">
      <AlertTriangle className="w-10 h-10 text-red-400" />
      <p className="text-slate-300 text-sm max-w-md text-center">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-sm transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Retry
        </button>
      )}
    </div>
  );
}

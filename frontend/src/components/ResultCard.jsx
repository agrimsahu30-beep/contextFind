import React from 'react';
import ContextViewer from './ContextViewer';
import ScoreBreakdown from './ScoreBreakdown';
import { CheckCircle2, Award } from 'lucide-react';

export default function ResultCard({ result, isBest }) {
  const formatDate = (iso) => {
    try {
      return new Date(iso).toLocaleString('en-US', {
        month: 'short', day: 'numeric', hour: 'numeric',
        minute: '2-digit', hour12: true,
      });
    } catch { return iso; }
  };

  return (
    <article className={`overflow-hidden rounded-2xl border bg-white shadow-sm transition hover:shadow-md ${
      isBest ? 'border-indigo-200 ring-1 ring-indigo-100' : 'border-slate-200'
    }`}>
      {isBest && (
        <div className="flex items-center gap-2 border-b border-indigo-100 bg-indigo-50 px-5 py-2.5 text-xs font-semibold text-indigo-700">
          <Award className="h-4 w-4" /> Best candidate · Rank #{result.rank}
        </div>
      )}

      <div className="p-5 sm:p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <p className="font-semibold text-slate-900">{result.sender}</p>
            <p className="mt-1 text-xs text-slate-400">{formatDate(result.timestamp)}</p>
          </div>

          <div className="shrink-0 rounded-xl bg-slate-50 px-3 py-2 text-right ring-1 ring-slate-100">
            <p className="text-[9px] font-semibold uppercase tracking-wider text-slate-400">Ranking score</p>
            <p className="text-lg font-bold tabular-nums text-indigo-600">{result.score?.toFixed(3)}</p>
          </div>
        </div>

        <blockquote className="mt-5 border-l-2 border-indigo-300 pl-4 text-sm leading-7 text-slate-700 sm:text-[15px]">
          “{result.text}”
        </blockquote>

        {result.reasons?.length > 0 && (
          <div className="mt-5 flex flex-wrap gap-2">
            {result.reasons.map((reason, i) => (
              <span key={i} className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] font-medium text-emerald-700">
                <CheckCircle2 className="h-3 w-3" /> {reason}
              </span>
            ))}
          </div>
        )}

        <ScoreBreakdown breakdown={result.score_breakdown} finalScore={result.score} />
        <ContextViewer context={result.context} />
      </div>
    </article>
  );
}


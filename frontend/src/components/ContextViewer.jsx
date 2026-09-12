import React from 'react';
import { MessageSquare, Target } from 'lucide-react';

export default function ContextViewer({ context }) {
  if (!context?.length) return null;

  const formatDate = (iso) => {
    try {
      return new Date(iso).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      });
    } catch {
      return iso;
    }
  };

  return (
    <section className="mt-5 overflow-hidden rounded-xl border border-slate-200 bg-slate-50/60">
      <div className="flex items-center gap-2 border-b border-slate-200 bg-white px-4 py-3">
        <MessageSquare className="h-4 w-4 text-slate-500" />
        <div>
          <h4 className="text-xs font-semibold text-slate-800">
            Conversation context
          </h4>
          <p className="text-[10px] text-slate-400">
            Same conversation · chronological order
          </p>
        </div>
      </div>

      <div className="relative space-y-2 p-3 sm:p-4">
        <div className="absolute bottom-6 left-7.25 top-6 w-px bg-slate-200" />

        {context.map((item) => (
          <div
            key={item.id}
            className={`relative flex gap-3 rounded-lg p-3 transition-colors ${
              item.is_target
                ? 'border border-indigo-200 bg-indigo-50/70'
                : 'border border-transparent bg-white/70 hover:bg-white'
            }`}
          >
            <div
              className={`relative z-10 mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border ${
                item.is_target
                  ? 'border-indigo-200 bg-indigo-100 text-indigo-600'
                  : 'border-slate-200 bg-white text-slate-400'
              }`}
            >
              {item.is_target ? (
                <Target className="h-3 w-3" />
              ) : (
                <span className="h-1.5 w-1.5 rounded-full bg-current" />
              )}
            </div>

            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-1">
                <span className={`text-xs font-semibold ${
                  item.is_target ? 'text-indigo-700' : 'text-slate-700'
                }`}>
                  {item.sender}
                </span>

                <span className="text-[10px] tabular-nums text-slate-400">
                  {formatDate(item.timestamp)}
                </span>
              </div>

              <p className={`mt-1.5 text-xs leading-5 ${
                item.is_target ? 'font-medium text-slate-800' : 'text-slate-600'
              }`}>
                {item.text}
              </p>

              {item.is_target && (
                <span className="mt-2 inline-flex items-center rounded-full bg-indigo-100 px-2 py-0.5 text-[9px] font-bold uppercase tracking-wide text-indigo-600">
                  Retrieved message
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

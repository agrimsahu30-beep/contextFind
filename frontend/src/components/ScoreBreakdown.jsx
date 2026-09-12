import React, { useState } from 'react';
import {
  ChevronDown,
  ChevronUp,
  BarChart3,
} from 'lucide-react';

export default function ScoreBreakdown({
  breakdown,
  finalScore,
}) {
  const [open, setOpen] = useState(false);

  if (!breakdown) return null;

  const factors = [
    {
      label: 'Semantic similarity',
      weight: '60%',
      value: breakdown.semantic,
    },
    {
      label: 'Person match',
      weight: '15%',
      value: breakdown.person,
    },
    {
      label: 'Temporal match',
      weight: '10%',
      value: breakdown.temporal,
    },
    {
      label: 'Decision intent',
      weight: '10%',
      value: breakdown.decision,
    },
    {
      label: 'Context continuity',
      weight: '5%',
      value: breakdown.context,
    },
  ];

  return (
    <div className="mt-4 overflow-hidden rounded-xl border border-slate-200 bg-slate-50/70">

      {/* Toggle */}
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        aria-expanded={open}
        className="
          flex w-full items-center justify-between
          px-4 py-3
          text-left
          transition-colors
          hover:bg-slate-100
          focus:outline-none
          focus:ring-2
          focus:ring-inset
          focus:ring-indigo-500/20
        "
      >
        <div className="flex items-center gap-3">

          <div
            className="
              flex h-8 w-8 items-center justify-center
              rounded-lg
              bg-white
              text-indigo-600
              ring-1 ring-slate-200
            "
          >
            <BarChart3 className="h-4 w-4" />
          </div>

          <div>
            <p className="text-xs font-semibold text-slate-800">
              Why this score?
            </p>

            <p className="mt-0.5 text-[10px] text-slate-400">
              Ranking score: {finalScore?.toFixed(3)}
            </p>
          </div>
        </div>

        <div
          className="
            flex h-7 w-7 items-center justify-center
            rounded-md
            text-slate-400
            transition-colors
            group-hover:text-slate-600
          "
        >
          {open ? (
            <ChevronUp className="h-4 w-4" />
          ) : (
            <ChevronDown className="h-4 w-4" />
          )}
        </div>
      </button>

      {/* Breakdown */}
      {open && (
        <div className="border-t border-slate-200 bg-white">

          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3">
            <div>
              <p className="text-[11px] font-semibold text-slate-700">
                Ranking factors
              </p>

              <p className="mt-0.5 text-[10px] text-slate-400">
                Contribution of each retrieval signal
              </p>
            </div>

            <span
              className="
                rounded-full
                bg-indigo-50
                px-2 py-1
                text-[10px]
                font-semibold
                text-indigo-600
              "
            >
              Hybrid ranking
            </span>
          </div>

          {/* Factors */}
          <div className="divide-y divide-slate-100 border-t border-slate-100">
            {factors.map((factor) => {
              const value = Number(factor.value ?? 0);
              const percentage = Math.max(
                0,
                Math.min(100, value * 100)
              );

              return (
                <div
                  key={factor.label}
                  className="
                    px-4 py-3
                    transition-colors
                    hover:bg-slate-50
                  "
                >
                  <div className="flex items-center justify-between gap-4">

                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="truncate text-xs font-medium text-slate-700">
                          {factor.label}
                        </span>

                        <span className="shrink-0 text-[10px] text-slate-400">
                          {factor.weight}
                        </span>
                      </div>

                      {/* Progress */}
                      <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-100">
                        <div
                          className="
                            h-full rounded-full
                            bg-indigo-500
                            transition-all duration-500
                          "
                          style={{
                            width: `${percentage}%`,
                          }}
                        />
                      </div>
                    </div>

                    <span className="w-12 text-right text-xs font-semibold tabular-nums text-slate-700">
                      {percentage.toFixed(1)}%
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Total */}
          <div
            className="
              flex items-center justify-between
              border-t border-slate-200
              bg-slate-50
              px-4 py-3
            "
          >
            <div>
              <p className="text-xs font-semibold text-slate-800">
                Final weighted score
              </p>

              <p className="mt-0.5 text-[10px] text-slate-400">
                Combined retrieval signal
              </p>
            </div>

            <div className="text-right">
              <p className="text-lg font-bold tabular-nums text-indigo-600">
                {finalScore?.toFixed(3)}
              </p>
            </div>
          </div>

          {/* Disclaimer */}
          <div className="border-t border-slate-100 px-4 py-2.5">
            <p className="text-[10px] leading-relaxed text-slate-400">
              The ranking score is a retrieval signal produced by
              the backend. It is not a probability of correctness
              or an accuracy guarantee.
            </p>
          </div>

        </div>
      )}
    </div>
  );
}

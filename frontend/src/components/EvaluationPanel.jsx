import React from 'react';
import { BarChart3, Database, Users, Trophy, Target } from 'lucide-react';

export default function EvaluationPanel({ stats }) {
  if (!stats) return null;

  const corpus = stats.corpus || {};
  const evaluation = stats.evaluation || {};
  const hybrid = evaluation.hybrid || {};
  const semantic = evaluation.semantic || {};
  const keyword = evaluation.keyword || {};

  const methods = [
    { name: 'Keyword', data: keyword },
    { name: 'Semantic', data: semantic },
    { name: 'Hybrid', data: hybrid, active: true },
  ];

  const metrics = [
    ['Overall Top-1', 'overall_accuracy', '%'],
    ['Hard-query accuracy', 'hard_accuracy', '%'],
    ['Recall@5', 'recall_at_5', '%'],
    ['MRR', 'mrr', ''],
  ];

  const format = (value, suffix = '') =>
    value === undefined || value === null ? '—' : `${value}${suffix}`;

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">

      {/* Header */}
      <div className="flex flex-col gap-2 border-b border-slate-200 px-5 py-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
            <BarChart3 className="h-4.5 w-4.5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-900">
              Retrieval performance
            </h3>
            <p className="text-[11px] text-slate-400">
              Benchmark measurements from the indexed corpus
            </p>
          </div>
        </div>

        <span className="w-fit rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-[10px] font-medium text-slate-500">
          Benchmark data
        </span>
      </div>

      {/* Corpus stats */}
      <div className="grid grid-cols-2 divide-x divide-y divide-slate-100 border-b border-slate-200 sm:grid-cols-4 sm:divide-y-0">
        {[
          [Database, corpus.total_messages, 'Messages', true],
          [Users, corpus.participants, 'Participants', false],
          [Trophy, hybrid.hard_accuracy, 'Hard accuracy', false, '%'],
          [Target, hybrid.overall_accuracy, 'Top-1 accuracy', false, '%'],
        ].map(([Icon, value, label, comma, suffix = ''], i) => (
          <div key={label} className="p-4 sm:p-5">
            <div className="mb-3 flex h-7 w-7 items-center justify-center rounded-lg bg-slate-50 text-slate-500">
              <Icon className="h-3.5 w-3.5" />
            </div>
            <p className="text-xl font-bold tracking-tight text-slate-900">
              {value === undefined || value === null
                ? '—'
                : `${comma ? Number(value).toLocaleString() : value}${suffix}`}
            </p>
            <p className="mt-1 text-[10px] font-medium uppercase tracking-wide text-slate-400">
              {label}
            </p>
          </div>
        ))}
      </div>

      {/* Comparison */}
      <div className="p-5 sm:p-6">
        <div className="mb-4">
          <h4 className="text-xs font-semibold text-slate-800">
            Retrieval method comparison
          </h4>
          <p className="mt-1 text-[10px] text-slate-400">
            Higher values indicate stronger benchmark performance.
          </p>
        </div>

        {/* Desktop table */}
        <div className="hidden overflow-x-auto rounded-xl border border-slate-200 md:block">
          <table className="w-full min-w-155 text-left">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-wide text-slate-400">
                  Method
                </th>
                {metrics.map(([label]) => (
                  <th key={label} className="px-4 py-3 text-right text-[10px] font-semibold uppercase tracking-wide text-slate-400">
                    {label}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">
              {methods.map((method) => (
                <tr
                  key={method.name}
                  className={method.active ? 'bg-indigo-50/50' : 'bg-white'}
                >
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <span className={`h-1.5 w-1.5 rounded-full ${method.active ? 'bg-indigo-500' : 'bg-slate-300'}`} />
                      <span className={`text-xs font-semibold ${method.active ? 'text-indigo-700' : 'text-slate-600'}`}>
                        {method.name}
                      </span>
                      {method.active && (
                        <span className="rounded-full bg-indigo-100 px-2 py-0.5 text-[9px] font-semibold text-indigo-600">
                          Current
                        </span>
                      )}
                    </div>
                  </td>

                  {metrics.map(([, key, suffix]) => (
                    <td
                      key={key}
                      className={`px-4 py-3 text-right text-xs tabular-nums ${
                        method.active
                          ? 'font-bold text-slate-900'
                          : 'font-medium text-slate-600'
                      }`}
                    >
                      {format(method.data?.[key], suffix)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile cards */}
        <div className="space-y-2 md:hidden">
          {methods.map((method) => (
            <div
              key={method.name}
              className={`rounded-xl border p-4 ${
                method.active
                  ? 'border-indigo-200 bg-indigo-50/40'
                  : 'border-slate-200 bg-white'
              }`}
            >
              <div className="mb-3 flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-800">
                  {method.name}
                </span>
                {method.active && (
                  <span className="rounded-full bg-indigo-100 px-2 py-0.5 text-[9px] font-semibold text-indigo-600">
                    Current
                  </span>
                )}
              </div>

              <div className="grid grid-cols-2 gap-3">
                {metrics.map(([label, key, suffix]) => (
                  <div key={key}>
                    <p className="text-[9px] uppercase tracking-wide text-slate-400">
                      {label}
                    </p>
                    <p className="mt-1 text-sm font-bold tabular-nums text-slate-800">
                      {format(method.data?.[key], suffix)}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Disclaimer */}
        <p className="mt-4 text-[10px] leading-relaxed text-slate-400">
          Benchmark metrics represent measured performance on the evaluation
          dataset. They are not a guarantee of correctness for an individual
          search.
        </p>
      </div>
    </div>
  );
}

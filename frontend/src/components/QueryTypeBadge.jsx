import React from 'react';
import { Target, User, Calendar, MessageSquare } from 'lucide-react';

export default function QueryTypeBadge({ analysis }) {
  if (!analysis) return null;

  const { intent, person, time_range } = analysis;
  const type = intent?.toLowerCase();

  const config = {
    decision: {
      label: 'Decision',
      icon: Target,
      desc: 'Decision-aware search',
    },
    person: {
      label: person ? `Person · ${person}` : 'Person',
      icon: User,
      desc: 'Sender-aware search',
    },
    time: {
      label: 'Temporal',
      icon: Calendar,
      desc: 'Date-range constrained',
    },
  }[type] || {
    label: 'Semantic',
    icon: MessageSquare,
    desc: 'Meaning-based search',
  };

  const Icon = config.icon;

  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="inline-flex items-center gap-1.5 rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1.5 text-[11px] font-semibold text-indigo-700">
        <Icon className="h-3.5 w-3.5" />
        {config.label}
      </span>

      <span className="text-[11px] text-slate-400">
        {config.desc}
      </span>

      {time_range && (
        <span className="rounded-full border border-slate-200 bg-white px-2.5 py-1 text-[10px] text-slate-500">
          {time_range}
        </span>
      )}
    </div>
  );
}

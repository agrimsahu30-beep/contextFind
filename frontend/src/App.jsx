import React, { useEffect, useState } from 'react';
import { ArrowUpRight, CheckCircle2, Database, Search, Users } from 'lucide-react';
import SearchBar from './components/SearchBar';
import QueryTypeBadge from './components/QueryTypeBadge';
import ResultCard from './components/ResultCard';
import EvaluationPanel from './components/EvaluationPanel';
import { searchMessages, fetchStats } from './api';

const SAMPLE_QUERIES = [
  'When did we decide on the trip?',
  'What did Priya say about the budget?',
  'What did we discuss in June 2026?',
  'Who is taking care of snacks?',
];

const MODES = [
  { id: 'hybrid', label: 'Hybrid', description: 'Semantic + keyword reranking' },
  { id: 'semantic', label: 'Semantic', description: 'Meaning-based retrieval' },
  { id: 'keyword', label: 'Keyword', description: 'Exact term matching' },
];

export default function App() {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState('hybrid');
  const [loading, setLoading] = useState(false);
  const [resultsData, setResultsData] = useState(null);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats()
      .then(setStats)
      .catch((err) => console.error('Stats fetch error:', err));
  }, []);

  const handleSearch = async (searchQuery, searchMode = mode) => {
    const cleanQuery = searchQuery.trim();
    if (!cleanQuery) return;

    setQuery(cleanQuery);
    setLoading(true);
    setError(null);

    try {
      setResultsData(await searchMessages(cleanQuery, searchMode));
    } catch (err) {
      console.error(err);
      setError('Search service unavailable. Start the backend at http://localhost:8000.');
    } finally {
      setLoading(false);
    }
  };

  const handleModeChange = (newMode) => {
    setMode(newMode);
    if (query.trim()) handleSearch(query, newMode);
  };

  const results = resultsData?.results || [];
  const hasResults = results.length > 0;

  return (
    <div className="min-h-screen bg-[#f7f8fc] text-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-30 border-b border-slate-200/80 bg-white/90 backdrop-blur-xl">
        <div className="mx-auto flex h-17 max-w-280 items-center justify-between px-5 sm:px-7">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-xs font-bold text-white shadow-lg shadow-indigo-600/20">
              CF
            </div>
            <div>
              <h1 className="font-['Space_Grotesk'] text-sm font-bold tracking-tight">
                ContextFind
              </h1>
              <p className="text-[10px] text-slate-400">Conversation Intelligence</p>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-240 px-4 sm:px-6">
        {/* Hero */}
        <section className="py-14 text-center sm:py-20">
          <div className="mb-5 inline-flex items-center gap-2 text-[10px] font-bold tracking-[0.14em] text-indigo-600">
            <span className="h-px w-5 bg-indigo-600" />
            SEMANTIC CONVERSATION SEARCH
          </div>

          <h2 className="font-['Space_Grotesk'] text-[40px] font-bold leading-[1.05] tracking-[-0.045em] sm:text-[58px]">
            Find the conversation
            <br />
            <span className="text-indigo-600">behind the answer.</span>
          </h2>

          <p className="mx-auto mt-5 max-w-162.5 text-sm leading-7 text-slate-500 sm:text-base">
            Search message history using natural language. ContextFind combines
            semantic retrieval, keyword matching, and reranking to surface
            relevant conversation context.
          </p>

          <div className="mx-auto mt-8 max-w-190">
            <SearchBar
              onSearch={(q) => handleSearch(q, mode)}
              loading={loading}
              initialQuery={query}
            />
          </div>

          <div className="mt-5">
            <p className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
              Try an example
            </p>

            <div className="flex flex-wrap justify-center gap-2">
              {SAMPLE_QUERIES.map((sample) => (
                <button
                  key={sample}
                  disabled={loading}
                  onClick={() => handleSearch(sample, mode)}
                  className="group rounded-full border border-slate-200 bg-white px-3 py-2 text-[11px] text-slate-500 shadow-sm transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-600 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {sample}
                  <ArrowUpRight className="ml-1 inline h-3 w-3 opacity-40 transition group-hover:opacity-100" />
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* Controls */}
        <section className="grid gap-6 border-y border-slate-200 py-5 sm:grid-cols-[1fr_auto] sm:items-end">
          <div>
            <p className="mb-2 text-[10px] font-bold tracking-wider text-slate-400">
              RETRIEVAL MODE
            </p>

            <div className="flex w-full gap-1 rounded-xl bg-slate-100 p-1 sm:w-fit">
              {MODES.map((item) => (
                <button
                  key={item.id}
                  onClick={() => handleModeChange(item.id)}
                  className={`flex-1 rounded-lg px-3 py-2 text-left transition sm:flex-none ${
                    mode === item.id
                      ? 'bg-white text-indigo-600 shadow-sm'
                      : 'text-slate-500 hover:text-slate-700'
                  }`}
                >
                  <span className="block text-[11px] font-semibold">{item.label}</span>
                  <span className="hidden text-[9px] text-slate-400 sm:block">
                    {item.description}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {resultsData?.query_analysis && (
            <div>
              <p className="mb-2 text-[10px] font-bold tracking-wider text-slate-400">
                QUERY ANALYSIS
              </p>
              <QueryTypeBadge analysis={resultsData.query_analysis} />
            </div>
          )}
        </section>

        {/* Error */}
        {error && (
          <div className="mt-6 flex gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
            <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-red-100 text-xs font-bold">
              !
            </div>
            <div>
              <p className="text-xs font-semibold">Search unavailable</p>
              <p className="mt-1 text-[11px] text-red-600">{error}</p>
            </div>
          </div>
        )}

        {/* Results */}
        {resultsData && !error && (
          <section className={`py-10 transition-opacity ${loading ? 'opacity-50' : ''}`}>
            <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <p className="mb-1 text-[10px] font-bold tracking-wider text-slate-400">
                  RETRIEVAL RESULTS
                </p>
                <h3 className="font-['Space_Grotesk'] text-xl font-bold tracking-tight">
                  {hasResults ? `${results.length} candidates found` : 'No matching messages'}
                </h3>
              </div>

              {hasResults && (
                <p className="max-w-xs text-[10px] leading-5 text-slate-400 sm:text-right">
                  Ranking scores are retrieval signals, not guaranteed relevance.
                </p>
              )}
            </div>

            {hasResults ? (
              <div className="space-y-4">
                {results.map((result, index) => (
                  <ResultCard
                    key={result.message_id}
                    result={result}
                    isBest={index === 0}
                  />
                ))}
              </div>
            ) : (
              <div className="rounded-2xl border border-dashed border-slate-300 bg-white px-5 py-16 text-center">
                <Search className="mx-auto mb-4 h-8 w-8 text-indigo-400" />
                <h4 className="text-sm font-semibold">No matching messages found.</h4>
                <p className="mx-auto mt-2 max-w-md text-xs leading-5 text-slate-400">
                  Try removing a date, using a broader description, or choosing Hybrid mode.
                </p>
                <button
                  onClick={() => handleSearch(SAMPLE_QUERIES[0], 'hybrid')}
                  className="mt-5 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white transition hover:bg-indigo-700"
                >
                  Try a sample query
                </button>
              </div>
            )}
          </section>
        )}

        {/* Initial state */}
        {!resultsData && !loading && !error && (
          <section className="py-8">
            <div className="grid overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm sm:grid-cols-3">
              {[
                ['01', 'Ask naturally', 'Describe what you remember instead of searching for exact words.'],
                ['02', 'Retrieve intelligently', 'Compare semantic, keyword, and hybrid retrieval strategies.'],
                ['03', 'Inspect the evidence', 'Review the matched message and surrounding same-thread context.'],
              ].map(([number, title, description], index) => (
                <div
                  key={number}
                  className={`p-6 ${index < 2 ? 'border-b sm:border-b-0 sm:border-r' : ''} border-slate-200`}
                >
                  <span className="text-xs font-bold text-indigo-300">{number}</span>
                  <h4 className="mt-5 text-sm font-semibold">{title}</h4>
                  <p className="mt-2 text-xs leading-5 text-slate-500">{description}</p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Evaluation */}
        <section className="py-10 sm:py-14">
          <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="mb-1 text-[10px] font-bold tracking-wider text-slate-400">
                SYSTEM EVALUATION
              </p>
              <h3 className="font-['Space_Grotesk'] text-xl font-bold tracking-tight">
                Measured retrieval performance
              </h3>
            </div>
            <p className="max-w-sm text-[10px] leading-5 text-slate-400">
              Benchmark measurements describe system performance, not a guarantee
              for an individual search.
            </p>
          </div>

          <EvaluationPanel stats={stats} />
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto flex max-w-240 flex-col gap-2 px-5 py-5 text-[10px] text-slate-400 sm:flex-row sm:items-center sm:justify-between">
          <span className="font-semibold text-slate-500">ContextFind</span>
          <span>Semantic search · Thread-aware context · Hybrid retrieval</span>
        </div>
      </footer>
    </div>
  );
}

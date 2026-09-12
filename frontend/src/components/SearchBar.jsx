import React, { useEffect, useState } from 'react';
import { Search, X, Loader2, ArrowUpRight } from 'lucide-react';

export default function SearchBar({
  onSearch,
  loading,
  initialQuery = '',
}) {
  const [query, setQuery] = useState(initialQuery);

  // Keep the input synchronized with example queries
  useEffect(() => {
    setQuery(initialQuery);
  }, [initialQuery]);

  const handleSubmit = (e) => {
    e.preventDefault();

    const cleanQuery = query.trim();

    if (cleanQuery && !loading) {
      onSearch(cleanQuery);
    }
  };

  const handleClear = () => {
    setQuery('');
  };

  const canSearch = query.trim().length > 0 && !loading;

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div
        className={`
          group flex w-full items-center gap-2 rounded-2xl
          border bg-white p-2
          shadow-[0_8px_30px_rgba(15,23,42,0.06)]
          transition-all duration-200
          ${
            loading
              ? 'border-indigo-200'
              : 'border-slate-200 hover:border-slate-300'
          }
          focus-within:border-indigo-400
          focus-within:ring-4
          focus-within:ring-indigo-500/10
        `}
      >
        {/* Search icon */}
        <div
          className="
            flex h-12 w-12 shrink-0 items-center justify-center
            rounded-xl
            text-slate-400
            transition-colors
            group-focus-within:text-indigo-600
          "
        >
          {loading ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            <Search className="h-5 w-5" />
          )}
        </div>

        {/* Input */}
        <input
          id="search-input"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={loading}
          autoComplete="off"
          aria-label="Search conversations"
          placeholder="Search by meaning, for example: When did we finalize the trip?"
          className="
            h-12 min-w-0 flex-1
            bg-transparent
            text-sm font-medium text-slate-900
            outline-none
            placeholder:text-slate-400
            disabled:cursor-wait
            disabled:opacity-60
            sm:text-[15px]
          "
        />

        {/* Clear */}
        {query && !loading && (
          <button
            type="button"
            onClick={handleClear}
            aria-label="Clear search"
            className="
              flex h-9 w-9 shrink-0 items-center justify-center
              rounded-lg
              text-slate-400
              transition-all
              hover:bg-slate-100
              hover:text-slate-600
              focus:outline-none
              focus:ring-2
              focus:ring-indigo-500/20
            "
          >
            <X className="h-4 w-4" />
          </button>
        )}

        {/* Search button */}
        <button
          id="search-submit-btn"
          type="submit"
          disabled={!canSearch}
          className="
            flex h-12 shrink-0 items-center justify-center
            gap-2 rounded-xl
            bg-indigo-600
            px-4 sm:px-5
            text-sm font-semibold text-white
            shadow-sm
            transition-all duration-200
            hover:bg-indigo-700
            hover:shadow-md
            active:scale-[0.98]
            disabled:cursor-not-allowed
            disabled:bg-slate-100
            disabled:text-slate-400
            disabled:shadow-none
          "
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span className="hidden sm:inline">Searching</span>
            </>
          ) : (
            <>
              <span>Search</span>
              <ArrowUpRight className="h-4 w-4" />
            </>
          )}
        </button>
      </div>

      {/* Helper row */}
      <div className="mt-2 flex items-center justify-between px-1">
        <span className="text-[10px] text-slate-400 sm:text-xs">
          Search across your conversation history
        </span>

        <span className="hidden items-center gap-1.5 text-[10px] text-slate-400 sm:flex sm:text-xs">
          Press
          <kbd
            className="
              rounded-md border border-slate-200
              bg-white px-1.5 py-0.5
              font-sans text-[10px] font-medium
              text-slate-500
              shadow-sm
            "
          >
            Enter
          </kbd>
          to search
        </span>
      </div>
    </form>
  );
}


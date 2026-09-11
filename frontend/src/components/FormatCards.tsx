import type { FormatSummary } from '../api/types';
import CricketEmptyState from './CricketEmptyState';
import CricketError from './CricketError';
import CricketLoader from './CricketLoader';

const blurb: Record<string, string> = {
  ODI: 'Fifty overs. The format he bent to his will.',
  T20I: 'Twenty overs of controlled intent.',
  IPL: 'Franchise cricket, same obsession.',
};

export default function FormatCards({
  summary,
  loading,
  error,
  onRetry,
  onSelect,
}: {
  summary: FormatSummary | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
  onSelect: (f: 'ODI' | 'T20I' | 'IPL') => void;
}) {
  return (
    <section id="formats" aria-label="Formats" className="scroll-mt-20">
      <p className="text-xs font-semibold tracking-[0.3em] text-gold uppercase">02 · Formats</p>
      <h2 className="font-display mt-1 text-3xl text-zinc-50 sm:text-4xl">Three arenas</h2>

      <div className="mt-6">
        {loading && <CricketLoader label="Loading format cards" />}
        {error && !loading && (
          <CricketError message="Format numbers couldn't be loaded right now." onRetry={onRetry} />
        )}
        {!loading && !error && (!summary || summary.formats.length === 0) && (
          <CricketEmptyState message="No format data in this view yet." />
        )}
        {summary && !loading && !error && summary.formats.length > 0 && (
          <div className="grid gap-4 sm:grid-cols-3">
            {summary.formats.map((f) => (
              <button
                key={f.format}
                type="button"
                onClick={() => onSelect(f.format)}
                className="group rounded-2xl border border-line bg-panel p-6 text-left transition-all hover:-translate-y-1 hover:border-gold/50 hover:shadow-[0_20px_50px_-20px_rgba(217,169,60,0.25)]"
              >
                <div className="flex items-center justify-between">
                  <span className="font-display text-lg tracking-[0.2em] text-gold">{f.format}</span>
                  <span className="text-[11px] tracking-widest text-zinc-600 uppercase transition-colors group-hover:text-gold">
                    View →
                  </span>
                </div>
                <p className="font-display mt-3 text-4xl text-zinc-50 tabular-nums">
                  {f.runs.toLocaleString('en-IN')}
                </p>
                <p className="text-xs tracking-widest text-zinc-500 uppercase">runs</p>
                <dl className="mt-4 space-y-1.5 border-t border-line pt-3 text-sm">
                  <div className="flex justify-between">
                    <dt className="text-zinc-500">Innings</dt>
                    <dd className="text-zinc-200 tabular-nums">{f.innings}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-zinc-500">Average</dt>
                    <dd className="text-zinc-200 tabular-nums">
                      {f.average !== null ? f.average.toFixed(2) : '–'}
                    </dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-zinc-500">Highest</dt>
                    <dd className="text-zinc-200 tabular-nums">{f.highestScore ?? '–'}</dd>
                  </div>
                </dl>
                <p className="mt-4 text-xs leading-relaxed text-zinc-500">{blurb[f.format]}</p>
              </button>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

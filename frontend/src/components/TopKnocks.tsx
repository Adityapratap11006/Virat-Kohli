import type { InningsEntry } from '../api/types';
import CricketEmptyState from './CricketEmptyState';
import CricketError from './CricketError';
import CricketLoader from './CricketLoader';

function formatDate(iso: string): string {
  const [y, m, d] = iso.split('-').map(Number);
  return new Date(y, m - 1, d).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

export default function TopKnocks({
  items,
  loading,
  error,
  onRetry,
}: {
  items: InningsEntry[] | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
}) {
  return (
    <section id="top-knocks" aria-label="Top knocks" className="scroll-mt-20">
      <p className="text-xs font-semibold tracking-[0.3em] text-gold uppercase">04 · Top knocks</p>
      <h2 className="font-display mt-1 text-3xl text-zinc-50 sm:text-4xl">Top knocks by runs</h2>
      <p className="mt-1 text-sm text-zinc-500">A statistical ranking, not an editorial verdict.</p>

      <div className="mt-6">
        {loading && <CricketLoader label="Rewinding the highlights" />}
        {error && !loading && (
          <CricketError message="Top knocks couldn't be loaded right now." onRetry={onRetry} />
        )}
        {!loading && !error && (!items || items.length === 0) && (
          <CricketEmptyState message="No innings in this view yet." />
        )}
        {items && !loading && !error && items.length > 0 && (
          <ol className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {items.map((inn, idx) => (
              <li
                key={`${inn.matchId}-${inn.inningsNo}`}
                className="relative overflow-hidden rounded-2xl border border-line bg-panel p-5 transition-all hover:-translate-y-1 hover:border-gold/50"
              >
                <span
                  aria-hidden="true"
                  className="font-display pointer-events-none absolute -top-3 right-2 text-7xl text-panel-2 select-none"
                >
                  {String(idx + 1).padStart(2, '0')}
                </span>
                <p className="font-display text-5xl text-gold tabular-nums">
                  {inn.runs}
                  {!inn.dismissed && <span className="text-3xl">*</span>}
                </p>
                <p className="mt-1 text-sm font-semibold text-zinc-100">vs {inn.opposition}</p>
                <p className="mt-0.5 text-xs text-zinc-500">
                  {inn.format} · {formatDate(inn.matchDate)}
                </p>
                <p className="mt-0.5 truncate text-xs text-zinc-500">{inn.venue}</p>
                <p className="mt-3 border-t border-line pt-2 text-xs text-zinc-400 tabular-nums">
                  {inn.ballsFaced} balls
                  {inn.strikeRate !== null ? ` · SR ${inn.strikeRate.toFixed(2)}` : ''}
                  {inn.dismissalKind ? ` · ${inn.dismissalKind}` : ' · not out'}
                </p>
              </li>
            ))}
          </ol>
        )}
      </div>
    </section>
  );
}

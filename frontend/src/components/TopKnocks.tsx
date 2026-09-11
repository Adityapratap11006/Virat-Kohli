import type { InningsEntry } from '../api/types';
import { knockImageFor } from '../data/knockImages';
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
            {items.map((inn, idx) => {
              const photo = knockImageFor(inn.matchId);
              return (
              <li
                key={`${inn.matchId}-${inn.inningsNo}`}
                className="relative overflow-hidden rounded-2xl border border-line bg-panel transition-all hover:-translate-y-1 hover:border-gold/50"
              >
                {photo ? (
                  <div className="relative h-44 overflow-hidden">
                    <img
                      src={photo.imagePath}
                      alt={photo.caption}
                      loading="lazy"
                      className="h-full w-full object-cover object-top"
                      onError={(e) => {
                        (e.target as HTMLImageElement).style.display = 'none';
                      }}
                    />
                    <div
                      aria-hidden="true"
                      className="pointer-events-none absolute inset-0 bg-gradient-to-t from-panel via-panel/20 to-transparent"
                    />
                    <span className="absolute top-3 right-3 rounded bg-ink/70 px-2 py-0.5 text-[10px] tracking-widest text-gold uppercase">
                      From this exact match
                    </span>
                  </div>
                ) : (
                  <p className="border-b border-line/60 px-5 pt-4 pb-3 text-[11px] tracking-widest text-zinc-600 uppercase">
                    Exact match image unavailable
                  </p>
                )}
                <div className="p-5">
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
                {photo && (
                  <p className="mt-2 text-[11px] text-zinc-600">
                    {photo.caption} · {photo.attribution}
                  </p>
                )}
                </div>
              </li>
              );
            })}
          </ol>
        )}
      </div>
    </section>
  );
}

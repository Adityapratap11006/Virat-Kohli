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

export default function RecentForm({
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
  const chronological = items ? [...items].reverse() : null;
  const maxRuns = chronological ? Math.max(1, ...chronological.map((i) => i.runs)) : 1;

  return (
    <section id="form" aria-label="Recent form" className="scroll-mt-20">
      <p className="text-xs font-semibold tracking-[0.3em] text-gold uppercase">03 · Form</p>
      <h2 className="font-display mt-1 text-3xl text-zinc-50 sm:text-4xl">Recent innings</h2>
      <p className="mt-1 text-sm text-zinc-500">Oldest → latest. Bar length is runs scored.</p>

      <div className="mt-6">
        {loading && <CricketLoader label="Walking out to the middle" />}
        {error && !loading && (
          <CricketError message="Recent form couldn't be loaded right now." onRetry={onRetry} />
        )}
        {!loading && !error && (!chronological || chronological.length === 0) && (
          <CricketEmptyState message="No innings in this view yet." />
        )}
        {chronological && !loading && !error && chronological.length > 0 && (
          <ol className="space-y-2.5">
            {chronological.map((inn) => (
              <li
                key={`${inn.matchId}-${inn.inningsNo}`}
                className="group rounded-xl border border-line/70 bg-panel px-4 py-3 transition-colors hover:border-gold/40"
              >
                <div className="flex items-baseline justify-between gap-3">
                  <p className="min-w-0 truncate text-sm text-zinc-200">
                    <span className="mr-2 inline-block rounded bg-panel-2 px-1.5 py-0.5 text-[10px] font-bold tracking-widest text-gold">
                      {inn.format}
                    </span>
                    vs {inn.opposition}
                    <span className="ml-2 text-xs text-zinc-500">
                      {formatDate(inn.matchDate)} · {inn.venue}
                    </span>
                  </p>
                  <p className="font-display shrink-0 text-2xl tabular-nums">
                    <span className={inn.runs >= 50 ? 'text-gold' : 'text-zinc-100'}>{inn.runs}</span>
                    {!inn.dismissed && <span className="text-gold" aria-label="not out">*</span>}
                    <span className="ml-1.5 align-middle text-[11px] font-normal text-zinc-500">
                      ({inn.ballsFaced})
                    </span>
                  </p>
                </div>
                <div
                  className="mt-2 h-1 overflow-hidden rounded-full bg-panel-2"
                  role="img"
                  aria-label={`${inn.runs} runs off ${inn.ballsFaced} balls`}
                >
                  <div
                    className={`h-full rounded-full transition-all ${
                      inn.runs >= 100 ? 'bg-gold' : inn.runs >= 50 ? 'bg-gold/70' : 'bg-ball/80'
                    }`}
                    style={{ width: `${Math.max(3, (inn.runs / maxRuns) * 100)}%` }}
                  />
                </div>
              </li>
            ))}
          </ol>
        )}
      </div>
    </section>
  );
}

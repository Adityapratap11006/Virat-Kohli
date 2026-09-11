import { contextSummary, oppositionSummary, venueSummary } from '../api/playerApi';
import type { FormatFilter } from '../api/types';
import { useApi } from '../hooks/useApi';
import CricketEmptyState from './CricketEmptyState';
import CricketError from './CricketError';
import CricketLoader from './CricketLoader';

function avg(v: number | null, digits = 2): string {
  return v === null ? '–' : v.toFixed(digits);
}

function RankedRows({
  rows,
  nameOf,
  subOf,
}: {
  rows: { name: string; sub: string; innings: number; runs: number; average: number | null; strikeRate: number | null; highestScore: number | null }[];
  nameOf: string;
  subOf: string;
}) {
  const max = Math.max(1, ...rows.map((r) => r.runs));
  return (
    <ol aria-label={nameOf} className="space-y-2.5">
      {rows.map((r, i) => (
        <li
          key={r.name}
          className="rounded-xl border border-line/70 bg-panel px-4 py-3 transition-colors hover:border-gold/40"
        >
          <div className="flex items-baseline gap-3">
            <span className="font-display w-7 shrink-0 text-sm text-zinc-600 tabular-nums">
              {String(i + 1).padStart(2, '0')}
            </span>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-semibold text-zinc-100">{r.name}</p>
              <p className="truncate text-xs text-zinc-500">
                {r.innings} inns · avg {avg(r.average)} · SR {avg(r.strikeRate)} · HS {r.highestScore ?? '–'}
                {r.sub ? ` · ${r.sub}` : ''}
              </p>
            </div>
            <p className="font-display shrink-0 text-2xl tabular-nums">
              <span className={i === 0 ? 'text-gold' : 'text-zinc-100'}>{r.runs.toLocaleString('en-IN')}</span>
            </p>
          </div>
          <div className="mt-2 ml-10 h-1 overflow-hidden rounded-full bg-panel-2" aria-hidden="true">
            <div
              className={`h-full rounded-full ${i === 0 ? 'bg-gold' : 'bg-gold/50'}`}
              style={{ width: `${Math.max(3, (r.runs / max) * 100)}%` }}
            />
          </div>
          <span className="sr-only">{subOf}</span>
        </li>
      ))}
    </ol>
  );
}

export default function AnalysisSection({
  playerId,
  format,
}: {
  playerId: number;
  format: FormatFilter;
}) {
  const opp = useApi(`opp-${playerId}-${format}`, () => oppositionSummary(playerId, format));
  const ven = useApi(`ven-${playerId}-${format}`, () => venueSummary(playerId, format));
  const ctx = useApi(`ctx-${playerId}-${format}`, () => contextSummary(playerId, format));

  return (
    <section id="analysis" aria-label="Kohli against the world" className="scroll-mt-20">
      <p className="text-xs font-semibold tracking-[0.3em] text-gold uppercase">05 · Analysis</p>
      <h2 className="font-display mt-1 text-3xl text-zinc-50 sm:text-4xl">Kohli against the world</h2>
      <p className="mt-1 max-w-2xl text-sm text-zinc-500">
        Where and against whom the runs came — ranked by runs scored, ties broken
        deterministically. Every number from the database.
      </p>
      <figure className="relative mt-6 overflow-hidden rounded-2xl border border-line">
        <img
          src="/images/virat-kohli-batting-2013.jpg"
          alt="Virat Kohli batting against South Africa during the 2013 ICC Champions Trophy"
          loading="lazy"
          className="aspect-[21/8] w-full object-cover object-top"
        />
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 bg-gradient-to-t from-ink/85 via-transparent to-transparent"
        />
        <figcaption className="absolute right-4 bottom-3 text-[11px] text-zinc-400">
          Photo: Dee03, CC BY-SA 4.0, via Wikimedia Commons
        </figcaption>
        <p className="absolute bottom-3 left-5 font-display text-sm tracking-[0.25em] text-crease/90 uppercase">
          At the crease
        </p>
      </figure>

      <div className="mt-8 grid gap-10 lg:grid-cols-2">
        <div>
          <h3 className="font-display text-xl tracking-wide text-zinc-100">By opposition</h3>
          <div className="mt-4">
            {opp.loading && <CricketLoader label="Reading the scorecards" />}
            {opp.error && !opp.loading && (
              <CricketError message="Opposition numbers couldn't be loaded." onRetry={opp.retry} />
            )}
            {!opp.loading && !opp.error && (!opp.data || opp.data.length === 0) && (
              <CricketEmptyState message="No opposition data in this view yet." />
            )}
            {opp.data && !opp.loading && !opp.error && opp.data.length > 0 && (
              <RankedRows
                nameOf="Opposition"
                subOf="opposition"
                rows={opp.data.map((r) => ({
                  name: r.opposition,
                  sub: `${r.hundreds}×100 ${r.fifties}×50`,
                  innings: r.innings,
                  runs: r.runs,
                  average: r.average,
                  strikeRate: r.strikeRate,
                  highestScore: r.highestScore,
                }))}
              />
            )}
          </div>
        </div>

        <div>
          <h3 className="font-display text-xl tracking-wide text-zinc-100">Performance by venue</h3>
          <div className="mt-4">
            {ven.loading && <CricketLoader label="Touring the grounds" />}
            {ven.error && !ven.loading && (
              <CricketError message="Venue numbers couldn't be loaded." onRetry={ven.retry} />
            )}
            {!ven.loading && !ven.error && (!ven.data || ven.data.length === 0) && (
              <CricketEmptyState message="No venue data in this view yet." />
            )}
            {ven.data && !ven.loading && !ven.error && ven.data.length > 0 && (
              <RankedRows
                nameOf="Venues"
                subOf="venue"
                rows={ven.data.map((r) => ({
                  name: r.venue,
                  sub: [
                    r.city ?? 'city not recorded',
                    r.country ?? null,
                    r.sourceNames > 1 ? `${r.sourceNames} source names consolidated` : null,
                  ]
                    .filter(Boolean)
                    .join(' · '),
                  innings: r.innings,
                  runs: r.runs,
                  average: r.average,
                  strikeRate: r.strikeRate,
                  highestScore: r.highestScore,
                }))}
              />
            )}
          </div>
        </div>
      </div>

      <div className="mt-10">
        <h3 className="font-display text-xl tracking-wide text-zinc-100">Match context</h3>
        <div className="mt-4">
          {ctx.loading && <CricketLoader label="Setting the field" />}
          {ctx.error && !ctx.loading && (
            <CricketError message="Context numbers couldn't be loaded." onRetry={ctx.retry} />
          )}
          {!ctx.loading && !ctx.error && ctx.data && (
            <div className="grid gap-4 sm:grid-cols-2">
              {[
                { block: ctx.data.firstInnings, note: 'Setting a target' },
                { block: ctx.data.secondInnings, note: 'Chasing' },
              ].map(({ block, note }) =>
                block ? (
                  <div key={block.label} className="rounded-2xl border border-line bg-panel p-6">
                    <p className="text-[11px] tracking-[0.25em] text-zinc-500 uppercase">{note}</p>
                    <p className="font-display mt-1 text-lg text-zinc-100">{block.label}</p>
                    <p className="font-display mt-3 text-4xl tabular-nums">
                      <span className="text-gold">{block.runs.toLocaleString('en-IN')}</span>
                      <span className="ml-2 align-middle text-sm font-normal text-zinc-500">
                        runs · {block.innings} inns
                      </span>
                    </p>
                    <dl className="mt-4 grid grid-cols-3 gap-2 border-t border-line pt-3 text-center">
                      {[
                        ['Avg', avg(block.average)],
                        ['SR', avg(block.strikeRate)],
                        ['HS', block.highestScore === null ? '–' : String(block.highestScore)],
                      ].map(([k, v]) => (
                        <div key={k}>
                          <dd className="text-lg text-zinc-100 tabular-nums">{v}</dd>
                          <dt className="text-[10px] tracking-[0.2em] text-zinc-500 uppercase">{k}</dt>
                        </div>
                      ))}
                    </dl>
                  </div>
                ) : (
                  <CricketEmptyState key={note} message={`No ${note.toLowerCase()} innings in this view yet.`} />
                ),
              )}
            </div>
          )}
          {!ctx.loading && !ctx.error && ctx.data && ctx.data.positions.length > 0 && (
            <div className="mt-4 rounded-2xl border border-line bg-panel p-6">
              <p className="text-[11px] tracking-[0.25em] text-zinc-500 uppercase">
                By batting position · reliable records only
              </p>
              <ul className="mt-3 flex flex-wrap gap-2">
                {ctx.data.positions.map((p) => (
                  <li
                    key={p.position}
                    className="rounded-full border border-line bg-panel-2 px-4 py-2 text-sm tabular-nums"
                    title={`${p.innings} innings`}
                  >
                    <span className="font-display text-gold">No. {p.position}</span>
                    <span className="ml-2 text-zinc-300">{p.runs.toLocaleString('en-IN')} runs</span>
                    <span className="ml-2 text-zinc-500">avg {avg(p.average)}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

import { contextSummary, oppositionSummary, venueSummary } from '../api/playerApi';
import type { FormatFilter } from '../api/types';
import { preferredKnockFor } from '../data/knockImages';
import { imageFor } from '../data/oppositionImages';
import { useApi } from '../hooks/useApi';

function oppositionVisual(opposition: string) {
  const knock = preferredKnockFor(opposition);
  if (knock) {
    return {
      src: knock.imagePath,
      alt: knock.caption,
      badge: 'From this exact match',
      caption: `${knock.caption} · ${knock.attribution}`,
    };
  }
  const img = imageFor(opposition);
  if (img) {
    return {
      src: img.imagePath,
      alt: img.matchDescription,
      badge: `Kohli batting vs ${opposition}`,
      caption: `${img.matchDescription} · ${img.attribution}`,
    };
  }
  return null;
}
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
              <ol aria-label="Opposition" className="grid gap-4 sm:grid-cols-2">
                {opp.data.map((r, i) => {
                  const img = oppositionVisual(r.opposition);
                  return (
                    <li
                      key={r.opposition}
                      className="group overflow-hidden rounded-2xl border border-line/70 bg-panel transition-all hover:-translate-y-1 hover:border-gold/40"
                    >
                      {img ? (
                        <div className="relative h-40 overflow-hidden">
                          <img
                            src={img.src}
                            alt={img.alt}
                            loading="lazy"
                            className="h-full w-full object-cover object-top transition-transform duration-500 group-hover:scale-[1.03]"
                            onError={(e) => {
                              (e.target as HTMLImageElement).style.display = 'none';
                            }}
                          />
                          <div
                            aria-hidden="true"
                            className="pointer-events-none absolute inset-0 bg-gradient-to-t from-panel via-panel/20 to-transparent"
                          />
                          <span className="font-display absolute top-3 left-4 text-sm text-zinc-300 tabular-nums">
                            {String(i + 1).padStart(2, '0')}
                          </span>
                          <span className="absolute top-3 right-3 rounded bg-ink/70 px-2 py-0.5 text-[10px] tracking-widest text-zinc-300 uppercase">
                            {img.badge}
                          </span>
                          <p className="font-display absolute bottom-2 left-4 text-xl text-zinc-50">
                            {r.opposition}
                          </p>
                        </div>
                      ) : (
                        <div
                          className="relative flex h-40 items-center justify-between overflow-hidden bg-panel-2 px-5"
                          role="img"
                          aria-label={`No verified photograph available for Kohli against ${r.opposition}`}
                        >
                          <div aria-hidden="true" className="flex items-center gap-4">
                            <svg width="44" height="44" viewBox="0 0 22 22">
                              <circle cx="11" cy="11" r="10" fill="none" stroke="#3a415a" strokeWidth="1.5" />
                              <circle cx="11" cy="11" r="10" fill="#c8102e" opacity="0.25" />
                              <path
                                d="M7 4 Q11 11 7 18 M15 4 Q11 11 15 18"
                                fill="none"
                                stroke="#d9a93c"
                                strokeWidth="1"
                                strokeDasharray="2 1.6"
                              />
                            </svg>
                            <div>
                              <p className="font-display text-xl text-zinc-100">{r.opposition}</p>
                              <p className="text-[11px] tracking-widest text-zinc-500 uppercase">
                                Image unavailable
                              </p>
                            </div>
                          </div>
                          <span className="font-display text-sm text-zinc-500 tabular-nums">
                            {String(i + 1).padStart(2, '0')}
                          </span>
                        </div>
                      )}
                      <div className="px-4 py-3">
                        <div className="flex items-baseline justify-between gap-2">
                          <p className="text-xs text-zinc-500">
                            {r.innings} inns · avg {avg(r.average)} · SR {avg(r.strikeRate)} · HS{' '}
                            {r.highestScore ?? '–'}
                          </p>
                          <p className="font-display text-2xl tabular-nums">
                            <span className={i === 0 ? 'text-gold' : 'text-zinc-100'}>
                              {r.runs.toLocaleString('en-IN')}
                            </span>
                          </p>
                        </div>
                        <div
                          className="mt-2 h-1 overflow-hidden rounded-full bg-panel-2"
                          role="img"
                          aria-label={`${r.runs} runs against ${r.opposition}`}
                        >
                          <div
                            className={`h-full rounded-full ${i === 0 ? 'bg-gold' : 'bg-gold/50'}`}
                            style={{
                              width: `${Math.max(3, (r.runs / Math.max(1, opp.data?.[0]?.runs ?? 1)) * 100)}%`,
                            }}
                          />
                        </div>
                        {img ? (
                          <p className="mt-2 text-[11px] text-zinc-600">{img.caption}</p>
                        ) : (
                          <p className="mt-2 text-[11px] text-zinc-600">
                            No verified photograph for this fixture — statistics only.
                          </p>
                        )}
                      </div>
                    </li>
                  );
                })}
              </ol>
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

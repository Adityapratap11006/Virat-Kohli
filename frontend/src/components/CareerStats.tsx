import type { CareerSummary } from '../api/types';
import CricketError from './CricketError';
import { BallMark } from './CricketLoader';

function Stat({ label, value, accent }: { label: string; value: string; accent?: boolean }) {
  return (
    <div className="border-l-2 border-line pl-4">
      <dd
        className={`font-display text-3xl tabular-nums sm:text-4xl ${
          accent ? 'text-gold' : 'text-zinc-50'
        }`}
      >
        {value}
      </dd>
      <dt className="mt-1 text-[11px] tracking-[0.2em] text-zinc-500 uppercase">{label}</dt>
    </div>
  );
}

function num(n: number | null, digits = 0): string {
  if (n === null || n === undefined) return '–';
  return digits > 0 ? n.toFixed(digits) : n.toLocaleString('en-IN');
}

function ScoreboardSkeleton() {
  return (
    <div role="status" aria-label="Loading career statistics" className="py-6">
      <div className="mb-4 flex items-center gap-3">
        <BallMark size={20} />
        <p className="text-xs tracking-[0.25em] text-zinc-500 uppercase">Reading the scorebook</p>
      </div>
      <div className="grid grid-cols-2 gap-6 sm:grid-cols-4">
        {[0, 1, 2, 3].map((i) => (
          <div key={i} className="border-l-2 border-line pl-4">
            <div className="h-9 w-24 animate-pulse rounded bg-panel-2" />
            <div className="mt-2 h-3 w-16 animate-pulse rounded bg-panel-2" />
          </div>
        ))}
      </div>
    </div>
  );
}

export default function CareerStats({
  career,
  loading,
  error,
  onRetry,
  formatLabel,
}: {
  career: CareerSummary | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
  formatLabel: string;
}) {
  return (
    <section id="overview" aria-label="Career overview" className="scroll-mt-20">
      <div className="flex flex-wrap items-end justify-between gap-2">
        <div>
          <p className="text-xs font-semibold tracking-[0.3em] text-gold uppercase">01 · Overview</p>
          <h2 className="font-display mt-1 text-3xl text-zinc-50 sm:text-4xl">
            Career <span className="text-zinc-500">/ {formatLabel}</span>
          </h2>
        </div>
        {career?.lastMatchDate && (
          <p className="text-xs text-zinc-500">
            {career.firstMatchDate} → {career.lastMatchDate} · {career.innings.toLocaleString('en-IN')} innings
          </p>
        )}
      </div>

      <div className="mt-6">
        {loading && <ScoreboardSkeleton />}
        {error && !loading && (
          <CricketError message="Career numbers couldn't be loaded right now." onRetry={onRetry} />
        )}
        {career && !loading && !error && (
          <dl className="grid grid-cols-2 gap-x-4 gap-y-7 sm:grid-cols-4">
            <Stat label="Runs" value={num(career.runs)} accent />
            <Stat label="Average" value={num(career.average, 2)} />
            <Stat label="Highest" value={num(career.highestScore)} />
            <Stat label="Strike Rate" value={num(career.strikeRate, 2)} />
            <Stat label="Hundreds" value={num(career.hundreds)} />
            <Stat label="Fifties" value={num(career.fifties)} />
            <Stat label="Not Outs" value={num(career.notOuts)} />
            <Stat label="Ducks" value={num(career.ducks)} />
          </dl>
        )}
      </div>
    </section>
  );
}

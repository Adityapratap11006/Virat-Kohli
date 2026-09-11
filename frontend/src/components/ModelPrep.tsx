export default function ModelPrep() {
  return (
    <section aria-label="Expected runs model preparation" className="scroll-mt-20">
      <div className="relative overflow-hidden rounded-2xl border border-line bg-panel p-6 sm:p-8">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute -top-24 right-0 h-64 w-64 rounded-full bg-ball/10 blur-[100px]"
        />
        <p className="text-xs font-semibold tracking-[0.3em] text-gold uppercase">
          06 · Expected Runs — in preparation
        </p>
        <h2 className="font-display mt-1 text-2xl text-zinc-50 sm:text-3xl">
          What will the model predict?
        </h2>
        <dl className="mt-5 grid gap-5 sm:grid-cols-3">
          <div className="border-l-2 border-gold/60 pl-4">
            <dt className="text-[11px] tracking-[0.2em] text-zinc-500 uppercase">Unit</dt>
            <dd className="mt-1 text-sm leading-relaxed text-zinc-200">
              One batter-innings — the runs one batter scores from entry to dismissal.
            </dd>
          </div>
          <div className="border-l-2 border-gold/60 pl-4">
            <dt className="text-[11px] tracking-[0.2em] text-zinc-500 uppercase">Moment</dt>
            <dd className="mt-1 text-sm leading-relaxed text-zinc-200">
              Immediately before the batter faces their first ball — using only
              information available at that exact instant.
            </dd>
          </div>
          <div className="border-l-2 border-gold/60 pl-4">
            <dt className="text-[11px] tracking-[0.2em] text-zinc-500 uppercase">Status</dt>
            <dd className="mt-1 text-sm leading-relaxed text-zinc-200">
              Validated: XGBoost v1 scores held-out Test MAE 13.6 (R² 0.19)
              vs 14.5 for historical average. No predictions shown yet.
            </dd>
          </div>
        </dl>
        <p className="mt-4 text-[11px] text-zinc-600">
          Chronological evaluation only — trained to 2021, validated 2022, tested
          on untouched 2023+ innings.
        </p>
      </div>
    </section>
  );
}

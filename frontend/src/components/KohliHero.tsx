import type { CareerSummary } from '../api/types';

function fmt(n: number | null): string {
  return n === null || n === undefined ? '–' : n.toLocaleString('en-IN');
}

export default function KohliHero({ career }: { career: CareerSummary | null }) {
  return (
    <section id="top" className="relative overflow-hidden" aria-label="Virat Kohli hero">
      {/* floodlight glow + pitch geometry */}
      <div aria-hidden="true" className="pointer-events-none absolute inset-0">
        <div className="floodlight-pulse absolute -top-32 left-1/4 h-96 w-96 rounded-full bg-gold/10 blur-[120px]" />
        <div className="absolute top-10 right-[8%] h-72 w-72 rounded-full bg-ball/10 blur-[110px]" />
        <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-ink to-transparent" />
        <div className="absolute top-0 bottom-0 left-1/2 hidden w-px bg-gradient-to-b from-transparent via-line to-transparent lg:block" />
      </div>

      <div className="relative mx-auto grid max-w-6xl gap-8 px-4 pt-28 pb-14 sm:px-6 lg:grid-cols-[1.05fr_0.95fr] lg:items-end lg:pt-32">
        <div className="rise-in">
          <p className="flex items-center gap-3 text-xs font-semibold tracking-[0.3em] text-gold uppercase">
            <span className="inline-block h-px w-10 bg-gold/70" aria-hidden="true" />
            KohliIQ · Career Intelligence
          </p>
          <h1 className="font-display mt-4 text-[clamp(3.2rem,9vw,7rem)] leading-[0.95] font-semibold tracking-tight text-zinc-50">
            VIRAT
            <br />
            <span className="text-gold">KOHLI</span>
          </h1>
          <p className="mt-5 max-w-md text-lg text-zinc-300">
            Decode the batter behind the numbers.
          </p>
          <p className="mt-2 max-w-md text-sm leading-relaxed text-zinc-500">
            Every innings. Every phase. Every pattern
            {career ? ` — ${career.innings.toLocaleString('en-IN')} white-ball innings read ball by ball.` : '.'}
          </p>

          <dl className="mt-8 flex max-w-md gap-8 border-t border-line pt-5">
            <div>
              <dt className="text-[11px] tracking-[0.2em] text-zinc-500 uppercase">Runs</dt>
              <dd className="font-display text-3xl text-zinc-50 tabular-nums">
                {career ? fmt(career.runs) : '–'}
              </dd>
            </div>
            <div>
              <dt className="text-[11px] tracking-[0.2em] text-zinc-500 uppercase">Average</dt>
              <dd className="font-display text-3xl text-zinc-50 tabular-nums">
                {career && career.average !== null ? career.average.toFixed(2) : '–'}
              </dd>
            </div>
            <div>
              <dt className="text-[11px] tracking-[0.2em] text-zinc-500 uppercase">Highest</dt>
              <dd className="font-display text-3xl text-gold tabular-nums">
                {career ? fmt(career.highestScore) : '–'}
              </dd>
            </div>
          </dl>
        </div>

        <figure className="relative mx-auto w-full max-w-sm lg:max-w-none">
          <div
            aria-hidden="true"
            className="absolute -inset-6 rounded-[2rem] bg-[radial-gradient(ellipse_at_center,rgba(217,169,60,0.14),transparent_65%)]"
          />
          <img
            src="/images/kohli-hero-waca-2015.jpg"
            alt="Virat Kohli batting for India at the WACA under lights, World Cup 2015"
            loading="eager"
            className="relative aspect-[3/3.4] w-full rounded-[1.4rem] border border-line object-cover object-top shadow-[0_30px_80px_-20px_rgba(0,0,0,0.9)]"
          />
          <figcaption className="mt-2 text-right text-[11px] text-zinc-600">
            Photo: Bahnfrend, CC BY-SA 4.0, via Wikimedia Commons
          </figcaption>
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-x-0 bottom-8 h-24 bg-gradient-to-t from-ink/80 to-transparent"
          />
          <p className="absolute bottom-12 left-5 font-display text-sm tracking-[0.25em] text-crease/90 uppercase">
            India · Right-hand bat · No. 18
          </p>
        </figure>
      </div>
    </section>
  );
}

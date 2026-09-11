import { useState } from 'react';
import { careerSummary, formatSummary, recentForm, searchPlayers, topInnings } from './api/playerApi';
import type { FormatFilter } from './api/types';
import AnalysisSection from './components/AnalysisSection';
import CareerStats from './components/CareerStats';
import CricketError from './components/CricketError';
import CricketLoader from './components/CricketLoader';
import Footer from './components/Footer';
import FormatCards from './components/FormatCards';
import FormatSwitcher from './components/FormatSwitcher';
import KohliHero from './components/KohliHero';
import Navbar from './components/Navbar';
import RecentForm from './components/RecentForm';
import TopKnocks from './components/TopKnocks';
import { useApi } from './hooks/useApi';

async function resolveKohli() {
  const list = await searchPlayers('V Kohli');
  const exact = list.find((p) => p.name === 'V Kohli');
  if (!exact) throw new Error('Virat Kohli was not found in the database.');
  return exact;
}

const formatLabel: Record<FormatFilter, string> = {
  ALL: 'All formats',
  ODI: 'ODI',
  T20I: 'T20I',
  IPL: 'IPL',
};

export default function App() {
  const [format, setFormat] = useState<FormatFilter>('ALL');
  const player = useApi('kohli-player', resolveKohli);
  const pid = player.data?.id ?? null;

  const careerAll = useApi(pid === null ? null : `career-all-${pid}`, () =>
    careerSummary(pid as number, 'ALL'),
  );
  const careerFmt = useApi(pid === null ? null : `career-${pid}-${format}`, () =>
    careerSummary(pid as number, format),
  );
  const formats = useApi(pid === null ? null : `formats-${pid}`, () => formatSummary(pid as number));
  const recent = useApi(pid === null ? null : `recent-${pid}-${format}`, () =>
    recentForm(pid as number, format, 12),
  );
  const top = useApi(pid === null ? null : `top-${pid}-${format}`, () =>
    topInnings(pid as number, format, 6),
  );

  const selectFormat = (f: Exclude<FormatFilter, 'ALL'>) => {
    setFormat(f);
    document.getElementById('overview')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-ink text-zinc-100 antialiased">
      <Navbar />
      <main>
        {player.loading && (
          <div className="flex min-h-screen items-center justify-center px-4">
            <div className="w-full max-w-md">
              <p className="floodlight-pulse mb-2 text-center font-display text-sm tracking-[0.3em] text-gold uppercase">
                KohliIQ
              </p>
              <CricketLoader label="Walking out to the middle" />
            </div>
          </div>
        )}
        {player.error && !player.loading && (
          <div className="mx-auto max-w-md px-4 pt-32">
            <CricketError
              title="That delivery didn't reach the server."
              message="KohliIQ couldn't reach the backend. Start Spring Boot, then try again."
              onRetry={player.retry}
            />
          </div>
        )}
        {player.data && (
          <>
            <KohliHero career={careerAll.data} />
            <div className="mx-auto max-w-6xl space-y-20 px-4 pb-4 sm:px-6">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <FormatSwitcher value={format} onChange={setFormat} />
                <p className="text-xs text-zinc-500">
                  {player.data.name} · {player.data.ambiguous ? 'shared name — resolved by registry' : 'registry-verified'}
                </p>
              </div>
              <CareerStats
                career={careerFmt.data}
                loading={careerFmt.loading}
                error={careerFmt.error}
                onRetry={careerFmt.retry}
                formatLabel={formatLabel[format]}
              />
              <FormatCards
                summary={formats.data}
                loading={formats.loading}
                error={formats.error}
                onRetry={formats.retry}
                onSelect={selectFormat}
              />
              <RecentForm
                items={recent.data}
                loading={recent.loading}
                error={recent.error}
                onRetry={recent.retry}
              />
              <TopKnocks items={top.data} loading={top.loading} error={top.error} onRetry={top.retry} />
              {pid !== null && <AnalysisSection playerId={pid} format={format} />}
            </div>
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}

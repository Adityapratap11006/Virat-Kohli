export default function Footer() {
  return (
    <footer className="mt-20 border-t border-line">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-8 text-xs text-zinc-500 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <p className="font-display tracking-[0.18em] text-zinc-300">
          KOHLI<span className="text-gold">IQ</span>
          <span className="ml-2 font-body font-normal tracking-normal text-zinc-500">
            Ball-by-ball intelligence from Cricsheet data.
          </span>
        </p>
        <p className="max-w-xl leading-relaxed">
          Hero photo: Bahnfrend, CC BY-SA 4.0, via{' '}
          <a
            href="https://commons.wikimedia.org/wiki/File:Virat_Kohli_portrait.jpg"
            className="underline decoration-zinc-600 underline-offset-2 hover:text-gold"
          >
            Wikimedia Commons
          </a>
          . Not affiliated with BCCI, ICC, or any franchise.
        </p>
      </div>
    </footer>
  );
}

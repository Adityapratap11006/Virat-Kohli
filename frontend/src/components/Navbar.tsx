const links = [
  { href: '#overview', label: 'Overview' },
  { href: '#formats', label: 'Formats' },
  { href: '#form', label: 'Form' },
  { href: '#top-knocks', label: 'Top Knocks' },
  { href: '#analysis', label: 'Analysis' },
];

export default function Navbar() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-line/70 bg-ink/85 backdrop-blur-md">
      <nav
        aria-label="Primary"
        className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6"
      >
        <a href="#top" className="flex items-center gap-2.5" aria-label="KohliIQ home">
          <svg width="26" height="26" viewBox="0 0 22 22" aria-hidden="true">
            <circle cx="11" cy="11" r="10" fill="#c8102e" />
            <path
              d="M7 4 Q11 11 7 18 M15 4 Q11 11 15 18"
              fill="none"
              stroke="#f3e9d4"
              strokeWidth="1.2"
              strokeDasharray="2 1.6"
            />
          </svg>
          <span className="font-display text-lg tracking-[0.18em] text-zinc-100">
            KOHLI<span className="text-gold">IQ</span>
          </span>
        </a>
        <ul className="hidden items-center gap-7 text-sm text-zinc-400 sm:flex">
          {links.map((l) => (
            <li key={l.href}>
              <a href={l.href} className="transition-colors hover:text-gold">
                {l.label}
              </a>
            </li>
          ))}
        </ul>
        <a
          href="#formats"
          className="rounded-full border border-gold/50 px-4 py-1.5 text-xs font-semibold tracking-widest text-gold uppercase transition-colors hover:bg-gold hover:text-ink sm:hidden"
        >
          Stats
        </a>
      </nav>
    </header>
  );
}

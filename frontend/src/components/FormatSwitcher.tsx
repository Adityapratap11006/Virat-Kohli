import type { FormatFilter } from '../api/types';

const options: { value: FormatFilter; label: string }[] = [
  { value: 'ALL', label: 'All' },
  { value: 'ODI', label: 'ODI' },
  { value: 'T20I', label: 'T20I' },
  { value: 'IPL', label: 'IPL' },
];

export default function FormatSwitcher({
  value,
  onChange,
}: {
  value: FormatFilter;
  onChange: (f: FormatFilter) => void;
}) {
  return (
    <div
      role="group"
      aria-label="Cricket format"
      className="inline-flex rounded-full border border-line bg-panel p-1"
    >
      {options.map((o) => {
        const active = o.value === value;
        return (
          <button
            key={o.value}
            type="button"
            aria-pressed={active}
            onClick={() => onChange(o.value)}
            className={`rounded-full px-4 py-1.5 text-sm font-semibold tracking-wide transition-all sm:px-6 ${
              active
                ? 'bg-gold text-ink shadow-[0_0_18px_rgba(217,169,60,0.35)]'
                : 'text-zinc-400 hover:text-zinc-100'
            }`}
          >
            {o.label}
          </button>
        );
      })}
    </div>
  );
}

function Ball() {
  return (
    <svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true" className="seam-spin">
      <circle cx="11" cy="11" r="10" fill="#c8102e" />
      <circle cx="11" cy="11" r="10" fill="none" stroke="#7d0a1e" strokeWidth="1.5" />
      <path
        d="M7 4 Q11 11 7 18 M15 4 Q11 11 15 18"
        fill="none"
        stroke="#f3e9d4"
        strokeWidth="1.2"
        strokeDasharray="2 1.6"
      />
    </svg>
  );
}

export function BallMark({ size = 22 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 22 22" aria-hidden="true">
      <circle cx="11" cy="11" r="10" fill="#c8102e" />
      <circle cx="11" cy="11" r="10" fill="none" stroke="#7d0a1e" strokeWidth="1.5" />
      <path
        d="M7 4 Q11 11 7 18 M15 4 Q11 11 15 18"
        fill="none"
        stroke="#f3e9d4"
        strokeWidth="1.2"
        strokeDasharray="2 1.6"
      />
    </svg>
  );
}

export default function CricketLoader({ label = 'Loading innings data' }: { label?: string }) {
  return (
    <div role="status" aria-live="polite" className="py-10">
      <p className="mb-3 text-center text-xs tracking-[0.25em] text-zinc-500 uppercase">{label}</p>
      <div className="relative mx-auto h-[22px] w-56 overflow-hidden">
        <div className="absolute inset-x-0 top-1/2 h-px -translate-y-1/2 bg-gradient-to-r from-transparent via-[#3a415a] to-transparent" />
        <div className="cricket-ball-track absolute top-0 left-0">
          <Ball />
        </div>
      </div>
    </div>
  );
}

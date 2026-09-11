import { BallMark } from './CricketLoader';

export default function CricketEmptyState({
  message = 'No innings in this view yet.',
}: {
  message?: string;
}) {
  return (
    <div className="flex flex-col items-center gap-3 rounded-xl border border-dashed border-line bg-panel/60 px-6 py-10 text-center">
      <span className="opacity-60">
        <BallMark size={26} />
      </span>
      <p className="text-sm text-zinc-400">{message}</p>
    </div>
  );
}

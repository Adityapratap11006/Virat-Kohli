import { BallMark } from './CricketLoader';

export default function CricketError({
  title = 'The ball went out of play.',
  message = "Couldn't load this cricket data right now.",
  onRetry,
}: {
  title?: string;
  message?: string;
  onRetry?: () => void;
}) {
  return (
    <div
      role="alert"
      className="flex flex-col items-center gap-3 rounded-xl border border-line bg-panel px-6 py-10 text-center"
    >
      <BallMark size={30} />
      <p className="font-display text-xl tracking-wide text-zinc-100">{title}</p>
      <p className="max-w-sm text-sm text-zinc-400">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-1 rounded-full border border-gold/60 px-5 py-2 text-sm font-semibold text-gold transition-colors hover:bg-gold hover:text-ink"
        >
          Try again
        </button>
      )}
    </div>
  );
}

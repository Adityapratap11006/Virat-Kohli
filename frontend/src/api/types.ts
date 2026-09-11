// Response shapes per docs/frontend-contract.md. No `any`.
export interface Player {
  id: number;
  name: string;
  registryId: string | null;
  ambiguous: boolean;
}

export interface CareerSummary {
  player: Player;
  format: 'ODI' | 'T20I' | 'IPL' | null;
  innings: number;
  runs: number;
  highestScore: number | null;
  average: number | null;
  strikeRate: number | null;
  notOuts: number;
  fifties: number;
  hundreds: number;
  ducks: number;
  firstMatchDate: string | null;
  lastMatchDate: string | null;
}

export interface PerFormat {
  format: 'ODI' | 'T20I' | 'IPL';
  innings: number;
  runs: number;
  highestScore: number | null;
  average: number | null;
}

export interface FormatSummary {
  player: Player;
  formats: PerFormat[];
}

export interface InningsEntry {
  matchDate: string;
  format: 'ODI' | 'T20I' | 'IPL';
  opposition: string;
  venue: string;
  runs: number;
  ballsFaced: number;
  strikeRate: number | null;
  inningsNo: number;
  dismissalKind: string | null;
  dismissed: boolean;
  matchId: string;
}

export interface OppositionRow {
  opposition: string;
  innings: number;
  runs: number;
  average: number | null;
  strikeRate: number | null;
  highestScore: number | null;
  fifties: number;
  hundreds: number;
  ducks: number;
  notOuts: number;
}

export interface VenueRow {
  venue: string;
  city: string | null;
  country: string | null;
  sourceNames: number;
  innings: number;
  runs: number;
  average: number | null;
  strikeRate: number | null;
  highestScore: number | null;
  fifties: number;
  hundreds: number;
  notOuts: number;
}

export interface ContextBlock {
  label: string;
  chase: boolean;
  innings: number;
  runs: number;
  average: number | null;
  strikeRate: number | null;
  highestScore: number | null;
  fifties: number;
  hundreds: number;
  ducks: number;
  notOuts: number;
}

export interface PositionRow {
  position: number;
  innings: number;
  runs: number;
  average: number | null;
  strikeRate: number | null;
}

export interface ContextSummary {
  player: Player;
  format: 'ODI' | 'T20I' | 'IPL' | null;
  firstInnings: ContextBlock | null;
  secondInnings: ContextBlock | null;
  positions: PositionRow[];
}

export interface MatchDetail {
  matchId: string;
  format: string;
  date: string;
  season: string;
  venue: string;
  city: string | null;
  team1: string;
  team2: string;
  tossWinner: string;
  tossDecision: 'bat' | 'field';
  event: string | null;
  dlsMethod: string | null;
}

export type FormatFilter = 'ALL' | 'ODI' | 'T20I' | 'IPL';

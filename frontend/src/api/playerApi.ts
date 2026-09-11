import { apiGet } from './client';
import type {
  CareerSummary,
  FormatFilter,
  FormatSummary,
  InningsEntry,
  MatchDetail,
  Player,
} from './types';

export function searchPlayers(query: string): Promise<Player[]> {
  return apiGet<Player[]>(`/players?search=${encodeURIComponent(query)}`);
}

export function careerSummary(playerId: number, format: FormatFilter): Promise<CareerSummary> {
  const q = format === 'ALL' ? '' : `?format=${format}`;
  return apiGet<CareerSummary>(`/players/${playerId}/career-summary${q}`);
}

export function formatSummary(playerId: number): Promise<FormatSummary> {
  return apiGet<FormatSummary>(`/players/${playerId}/format-summary`);
}

export function recentForm(
  playerId: number,
  format: FormatFilter,
  limit = 12,
): Promise<InningsEntry[]> {
  const q = format === 'ALL' ? `?limit=${limit}` : `?format=${format}&limit=${limit}`;
  return apiGet<InningsEntry[]>(`/players/${playerId}/recent-form${q}`);
}

export function topInnings(
  playerId: number,
  format: FormatFilter,
  limit = 6,
): Promise<InningsEntry[]> {
  const q = format === 'ALL' ? `?limit=${limit}` : `?format=${format}&limit=${limit}`;
  return apiGet<InningsEntry[]>(`/players/${playerId}/top-innings${q}`);
}

export function matchDetail(matchId: string): Promise<MatchDetail> {
  return apiGet<MatchDetail>(`/matches/${matchId}`);
}

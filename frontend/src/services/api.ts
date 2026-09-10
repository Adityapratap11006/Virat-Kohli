// Typed HTTP client for the Spring Boot API. Endpoints arrive in Phase 4+.
const baseUrl = import.meta.env.VITE_API_BASE_URL ?? '/api';

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${baseUrl}${path}`);
  if (!res.ok) {
    throw new Error(`API ${res.status}: ${path}`);
  }
  return res.json() as Promise<T>;
}

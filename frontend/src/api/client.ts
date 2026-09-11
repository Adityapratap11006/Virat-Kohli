// Single HTTP entry point for the Spring Boot API.
const baseUrl = import.meta.env.VITE_API_BASE_URL ?? '/api';

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export async function apiGet<T>(path: string): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${baseUrl}${path}`);
  } catch {
    throw new ApiError(0, 'The server could not be reached.');
  }
  if (!res.ok) {
    let message = `Request failed (${res.status}).`;
    try {
      const body = (await res.json()) as { message?: string };
      if (body.message) message = body.message;
    } catch {
      // keep default
    }
    throw new ApiError(res.status, message);
  }
  return res.json() as Promise<T>;
}

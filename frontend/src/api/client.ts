import type { Envelope, ErrorEnvelope } from '../types/api'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const API_ROLE = import.meta.env.VITE_API_ROLE ?? 'viewer'

export class ApiClientError extends Error {
  code: string
  details: unknown

  constructor(message: string, code = 'api_error', details: unknown = {}) {
    super(message)
    this.code = code
    this.details = details
  }
}

export async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      'X-Role': API_ROLE,
    },
  })

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as ErrorEnvelope | null
    throw new ApiClientError(
      payload?.error?.message ?? `HTTP ${response.status}`,
      payload?.error?.code ?? 'http_error',
      payload?.error?.details ?? {},
    )
  }

  return (await response.json()) as T
}

export async function getEnvelope<T>(path: string): Promise<Envelope<T>> {
  return getJson<Envelope<T>>(path)
}

export async function getHealth(): Promise<{ status: string }> {
  return getJson<{ status: string }>('/health')
}

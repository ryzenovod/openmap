import type { Envelope, ErrorEnvelope } from '../types/api'

export const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim().replace(/\/+$/, '') ||
  'http://localhost:8000'
const API_ROLE = import.meta.env.VITE_API_ROLE ?? 'viewer'

type RequestOptions = {
  signal?: AbortSignal
}

export class ApiClientError extends Error {
  code: string
  details: unknown
  status?: number
  url: string

  constructor(
    message: string,
    code = 'api_error',
    details: unknown = {},
    url = '',
    status?: number,
  ) {
    super(message)
    this.code = code
    this.details = details
    this.status = status
    this.url = url
  }
}

export function isAbortError(error: unknown): boolean {
  return error instanceof Error && error.name === 'AbortError'
}

export function apiErrorDiagnostics(error: unknown): {
  url?: string
  message: string
  code?: string
  status?: number
} {
  if (error instanceof ApiClientError) {
    return {
      url: error.url || undefined,
      message: error.message,
      code: error.code,
      status: error.status,
    }
  }
  if (error instanceof Error) {
    return { message: error.message }
  }
  return { message: String(error) }
}

export async function getJson<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const url = `${API_BASE_URL}${path}`
  let response: Response
  try {
    response = await fetch(url, {
      headers: {
        'X-Role': API_ROLE,
      },
      signal: options.signal,
    })
  } catch (error) {
    if (isAbortError(error)) {
      throw error
    }
    const message = error instanceof Error ? error.message : String(error)
    throw new ApiClientError(message, 'network_error', {}, url)
  }

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as ErrorEnvelope | null
    throw new ApiClientError(
      payload?.error?.message ?? `HTTP ${response.status}`,
      payload?.error?.code ?? 'http_error',
      payload?.error?.details ?? {},
      url,
      response.status,
    )
  }

  return (await response.json()) as T
}

export async function getEnvelope<T>(
  path: string,
  options: RequestOptions = {},
): Promise<Envelope<T>> {
  return getJson<Envelope<T>>(path, options)
}

export async function getHealth(): Promise<{ status: string }> {
  return getJson<{ status: string }>('/health')
}

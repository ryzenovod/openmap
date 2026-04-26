import { ApiClientError } from '../api/client'

type Props = { error: unknown }

export default function ApiErrorView({ error }: Props) {
  const err = error as ApiClientError
  return (
    <div className="error-box">
      <strong>Error:</strong> {err?.message ?? 'Unknown error'}
      <div className="error-meta">Code: {err?.code ?? 'unknown'}</div>
    </div>
  )
}

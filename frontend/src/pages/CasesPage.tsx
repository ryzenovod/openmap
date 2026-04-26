import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { api } from '../api/endpoints'
import ApiErrorView from '../components/ApiErrorView'
import EmptyView from '../components/EmptyView'
import LoadingView from '../components/LoadingView'
import type { CaseListRow } from '../types/api'

export default function CasesPage() {
  const [rows, setRows] = useState<CaseListRow[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<unknown>(null)
  const [search, setSearch] = useSearchParams()
  const limit = Number(search.get('limit') ?? '10')
  const offset = Number(search.get('offset') ?? '0')
  const sortBy = search.get('sort_by') ?? 'id'
  const sortOrder = search.get('sort_order') ?? 'asc'

  useEffect(() => {
    setLoading(true)
    setError(null)
    api
      .cases(`?limit=${limit}&offset=${offset}&sort_by=${sortBy}&sort_order=${sortOrder}`)
      .then((resp) => setRows(resp.data))
      .catch(setError)
      .finally(() => setLoading(false))
  }, [limit, offset, sortBy, sortOrder])

  if (loading) return <LoadingView />
  if (error) return <ApiErrorView error={error} />
  if (!rows.length) return <EmptyView text="No cases" />

  return (
    <div>
      <h3>Cases</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Registration date</th>
            <th>Diagnosis</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.registration_date}</td>
              <td>{row.diagnosis_raw}</td>
              <td>
                <Link to={`/cases/${row.id}`}>Details</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="pagination">
        <button onClick={() => setSearch({ limit: String(limit), offset: String(Math.max(offset - limit, 0)), sort_by: sortBy, sort_order: sortOrder })}>Prev</button>
        <button onClick={() => setSearch({ limit: String(limit), offset: String(offset + limit), sort_by: sortBy, sort_order: sortOrder })}>Next</button>
      </div>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { api } from '../api/endpoints'
import ApiErrorView from '../components/ApiErrorView'
import EmptyView from '../components/EmptyView'
import LoadingView from '../components/LoadingView'
import type { StructurePayload, YearlyRow } from '../types/api'

export default function ChartsPage() {
  const [yearly, setYearly] = useState<YearlyRow[]>([])
  const [structure, setStructure] = useState<StructurePayload | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<unknown>(null)

  useEffect(() => {
    setLoading(true)
    Promise.all([api.yearly(), api.structure()])
      .then(([y, s]) => {
        setYearly(y.data)
        setStructure(s.data)
      })
      .catch(setError)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingView />
  if (error) return <ApiErrorView error={error} />
  if (!structure) return <EmptyView />

  return (
    <div className="charts-grid">
      <section>
        <h3>Yearly dynamics</h3>
        <ul>
          {yearly.map((row) => (
            <li key={row.year}>
              {row.year}: {row.case_count}
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h3>Structure by MKB</h3>
        <ul>
          {structure.by_mkb.slice(0, 10).map((row, idx) => (
            <li key={`${row.bucket}-${idx}`}>
              {row.bucket}: {row.case_count}
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h3>Structure by age groups</h3>
        <ul>
          {structure.by_age_group.map((row, idx) => (
            <li key={`${row.bucket}-${idx}`}>
              {row.bucket}: {row.case_count}
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}

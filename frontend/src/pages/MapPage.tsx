import { useEffect, useMemo, useState } from 'react'
import { api } from '../api/endpoints'
import EmptyView from '../components/EmptyView'
import FilterPanel, { type MapFilters } from '../components/FilterPanel'
import LoadingView from '../components/LoadingView'
import MapView from '../components/MapView'
import type { MapAggregateRow } from '../types/api'
import ApiErrorView from '../components/ApiErrorView'
import Layout from '../components/Layout'

function toQuery(filters: MapFilters): string {
  const params = new URLSearchParams()
  if (filters.dateFrom) params.set('date_from', filters.dateFrom)
  if (filters.dateTo) params.set('date_to', filters.dateTo)
  if (filters.level) params.set('level', filters.level)
  if (filters.territory) params.set('territory', filters.territory)
  if (filters.mkb) params.set('mkb', filters.mkb)
  if (filters.gdu) params.set('gdu', filters.gdu)
  if (filters.cv) params.set('cv', filters.cv)
  if (filters.mbt) params.set('mbt', filters.mbt)
  return `?${params.toString()}`
}

export default function MapPage({ healthStatus }: { healthStatus: string }) {
  const [rows, setRows] = useState<MapAggregateRow[]>([])
  const [selected, setSelected] = useState<MapAggregateRow | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<unknown>(null)
  const [filters, setFilters] = useState<MapFilters>({
    dateFrom: '2025-01-01',
    dateTo: '2025-12-31',
    level: '',
    territory: '',
    mkb: '',
    gdu: '',
    cv: '',
    mbt: '',
  })

  useEffect(() => {
    setLoading(true)
    setError(null)
    api
      .mapAggregate(toQuery(filters))
      .then((resp) => setRows(resp.data))
      .catch(setError)
      .finally(() => setLoading(false))
  }, [filters])

  const summary = useMemo(() => {
    if (!selected) return <div>Select map point</div>
    return (
      <div>
        <h4>{selected.territory_name ?? `Territory ${selected.territory_id}`}</h4>
        <ul>
          <li>case_count: {selected.case_count}</li>
          <li>mbt_positive_count: {selected.mbt_positive_count}</li>
          <li>cv_positive_count: {selected.cv_positive_count}</li>
          <li>children_count: {selected.children_count}</li>
          <li>incidence_per_100k: {selected.incidence_per_100k ?? 'n/a'}</li>
        </ul>
      </div>
    )
  }, [selected])

  const content = loading ? (
    <LoadingView />
  ) : error ? (
    <ApiErrorView error={error} />
  ) : rows.length === 0 ? (
    <EmptyView text="No map aggregates" />
  ) : (
    <MapView rows={rows} onSelect={setSelected} />
  )

  return (
    <Layout healthStatus={healthStatus} sidebar={<FilterPanel onApply={setFilters} />} summary={summary}>
      {content}
    </Layout>
  )
}

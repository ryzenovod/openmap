import { useEffect, useMemo, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { api } from '../api/endpoints'
import EmptyView from '../components/EmptyView'
import FilterPanel, { DEFAULT_FILTERS, type MapFilters } from '../components/FilterPanel'
import LoadingView from '../components/LoadingView'
import MapView from '../components/MapView'
import type { MapAggregateRow } from '../types/api'
import ApiErrorView from '../components/ApiErrorView'
import Layout from '../components/Layout'

const GEOMETRY_ENABLED = import.meta.env.VITE_MAP_GEOMETRY_ENABLED === 'true'

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
  const { t } = useTranslation()
  const [rows, setRows] = useState<MapAggregateRow[]>([])
  const [selected, setSelected] = useState<MapAggregateRow | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<unknown>(null)
  const [filters, setFilters] = useState<MapFilters>(DEFAULT_FILTERS)

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
    if (!selected) {
      return <EmptyView text={t('map.selectTerritory')} />
    }

    return (
      <div className="space-y-3">
        <h3 className="text-base font-semibold text-slate-900">{t('map.summary')}</h3>
        <p className="text-sm text-slate-600">{selected.territory_name ?? `Территория ${selected.territory_id}`}</p>
        <Stat label={t('map.caseCount')} value={selected.case_count} />
        <Stat label={t('map.mbtPositive')} value={selected.mbt_positive_count} />
        <Stat label={t('map.cvPositive')} value={selected.cv_positive_count} />
        <Stat label={t('map.childrenCount')} value={selected.children_count} />
        <Stat label={t('map.incidence')} value={selected.incidence_per_100k ?? t('common.notSpecified')} />
      </div>
    )
  }, [selected, t])

  const totalCases = rows.reduce((acc, row) => acc + row.case_count, 0)

  const content = loading ? (
    <LoadingView />
  ) : error ? (
    <ApiErrorView error={error} />
  ) : rows.length === 0 ? (
    <EmptyView text={t('common.noDataPeriod')} />
  ) : !GEOMETRY_ENABLED ? (
    <div className="space-y-3">
      <EmptyView text={t('map.readyNoGeometry')} />
      <p className="text-sm text-slate-500">{t('map.mapHint')}</p>
      <MapView rows={rows} onSelect={setSelected} />
    </div>
  ) : (
    <MapView rows={rows} onSelect={setSelected} />
  )

  return (
    <Layout
      healthStatus={healthStatus}
      sidebar={<FilterPanel onApply={setFilters} />}
      summary={summary}
    >
      <div className="space-y-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">{t('map.title')}</h2>
          <p className="text-sm text-slate-500">{t('map.subtitle')}</p>
        </div>

        <div className="grid gap-3 md:grid-cols-3">
          <Widget title={t('widgets.total')} value={totalCases} />
          <Widget title={t('widgets.territories')} value={rows.length} />
          <Widget title={t('widgets.period')} value={`${filters.dateFrom} → ${filters.dateTo}`} />
        </div>

        {content}
      </div>
    </Layout>
  )
}

function Widget({ title, value }: { title: string; value: string | number }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-3 transition hover:-translate-y-0.5 hover:shadow-sm">
      <p className="text-xs uppercase tracking-wide text-slate-500">{title}</p>
      <p className="mt-1 text-lg font-semibold text-slate-900">{value}</p>
    </div>
  )
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-slate-200 px-3 py-2 text-sm">
      <span className="text-slate-600">{label}</span>
      <span className="font-semibold text-slate-900">{value}</span>
    </div>
  )
}

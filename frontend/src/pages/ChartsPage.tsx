import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { api } from '../api/endpoints'
import ApiErrorView from '../components/ApiErrorView'
import EmptyView from '../components/EmptyView'
import LoadingView from '../components/LoadingView'
import type { StructurePayload, YearlyRow } from '../types/api'

export default function ChartsPage() {
  const { t } = useTranslation()
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
  if (!structure) return <EmptyView text={t('common.noDataPeriod')} />

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-slate-900">{t('charts.title')}</h2>
      <div className="grid gap-4 xl:grid-cols-3">
        <ChartCard title={t('charts.yearly')} items={yearly.map((row) => `${row.year}: ${row.case_count}`)} />
        <ChartCard
          title={t('charts.mkb')}
          items={structure.by_mkb.slice(0, 10).map((row) => `${row.bucket}: ${row.case_count}`)}
        />
        <ChartCard
          title={t('charts.age')}
          items={structure.by_age_group.map((row) => `${row.bucket}: ${row.case_count}`)}
        />
      </div>
    </div>
  )
}

function ChartCard({ title, items }: { title: string; items: string[] }) {
  return (
    <section className="rounded-xl border border-slate-200 p-4 shadow-sm transition hover:shadow-md">
      <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">{title}</h3>
      <ul className="space-y-2 text-sm text-slate-700">
        {items.map((item) => (
          <li key={item} className="rounded-md bg-slate-50 px-3 py-2">
            {item}
          </li>
        ))}
      </ul>
    </section>
  )
}

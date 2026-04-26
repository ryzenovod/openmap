import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { api } from '../api/endpoints'
import ApiErrorView from '../components/ApiErrorView'
import EmptyView from '../components/EmptyView'
import LoadingView from '../components/LoadingView'
import type { CaseListRow } from '../types/api'

export default function CasesPage() {
  const { t } = useTranslation()
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
  if (!rows.length) return <EmptyView text={t('common.noDataPeriod')} />

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-slate-900">{t('cases.title')}</h2>
      <div className="overflow-hidden rounded-xl border border-slate-200">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-100 text-slate-600">
            <tr>
              <th className="px-3 py-2">{t('cases.id')}</th>
              <th className="px-3 py-2">{t('cases.date')}</th>
              <th className="px-3 py-2">{t('cases.diagnosis')}</th>
              <th className="px-3 py-2">{t('cases.actions')}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 bg-white">
            {rows.map((row) => (
              <tr key={row.id} className="transition hover:bg-slate-50">
                <td className="px-3 py-2">{row.id}</td>
                <td className="px-3 py-2">{row.registration_date}</td>
                <td className="px-3 py-2">{row.diagnosis_raw}</td>
                <td className="px-3 py-2">
                  <Link to={`/cases/${row.id}`} className="text-sky-700 transition hover:text-sky-900">
                    {t('common.details')}
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex gap-2">
        <button
          className="btn-secondary"
          onClick={() =>
            setSearch({
              limit: String(limit),
              offset: String(Math.max(offset - limit, 0)),
              sort_by: sortBy,
              sort_order: sortOrder,
            })
          }
        >
          {t('cases.prev')}
        </button>
        <button
          className="btn-secondary"
          onClick={() =>
            setSearch({
              limit: String(limit),
              offset: String(offset + limit),
              sort_by: sortBy,
              sort_order: sortOrder,
            })
          }
        >
          {t('cases.next')}
        </button>
      </div>
    </div>
  )
}

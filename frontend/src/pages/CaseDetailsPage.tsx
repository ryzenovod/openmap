import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { api } from '../api/endpoints'
import type { CaseDetailRow } from '../types/api'
import LoadingView from '../components/LoadingView'
import ApiErrorView from '../components/ApiErrorView'
import EmptyView from '../components/EmptyView'

export default function CaseDetailsPage() {
  const { t } = useTranslation()
  const { id } = useParams<{ id: string }>()
  const [data, setData] = useState<CaseDetailRow | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<unknown>(null)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    api
      .caseDetail(Number(id))
      .then((resp) => setData(resp.data))
      .catch(setError)
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <LoadingView />
  if (error) return <ApiErrorView error={error} />
  if (!data) return <EmptyView text={t('common.noDataPeriod')} />

  return (
    <div className="space-y-4">
      <Link to="/cases" className="inline-flex text-sm text-sky-700 transition hover:text-sky-900">
        ← {t('common.back')}
      </Link>
      <h2 className="text-xl font-semibold text-slate-900">{t('cases.detailsTitle', { id: data.id })}</h2>
      <div className="grid gap-2 rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm">
        <Row label={t('cases.patient')} value={data.patient_id} />
        <Row label={t('cases.date')} value={data.registration_date} />
        <Row label={t('cases.diagnosis')} value={data.diagnosis_raw} />
        <Row label="ГДУ" value={data.gdu_code ?? t('common.notSpecified')} />
        <Row label="КВ" value={data.cv_code ?? t('common.notSpecified')} />
        <Row label="МБТ" value={data.mbt_code ?? t('common.notSpecified')} />
      </div>
    </div>
  )
}

function Row({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex justify-between rounded-lg border border-slate-200 bg-white px-3 py-2">
      <span className="text-slate-600">{label}</span>
      <span className="font-medium text-slate-900">{value}</span>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api/endpoints'
import type { CaseDetailRow } from '../types/api'
import LoadingView from '../components/LoadingView'
import ApiErrorView from '../components/ApiErrorView'

export default function CaseDetailsPage() {
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
  if (!data) return <div>No case details</div>

  return (
    <div>
      <Link to="/cases">← Back</Link>
      <h3>Case #{data.id}</h3>
      <ul>
        <li>patient_id: {data.patient_id}</li>
        <li>registration_date: {data.registration_date}</li>
        <li>diagnosis_raw: {data.diagnosis_raw}</li>
        <li>gdu: {data.gdu_code ?? 'n/a'}</li>
        <li>cv: {data.cv_code ?? 'n/a'}</li>
        <li>mbt: {data.mbt_code ?? 'n/a'}</li>
      </ul>
    </div>
  )
}

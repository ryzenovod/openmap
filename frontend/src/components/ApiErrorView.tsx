import { useTranslation } from 'react-i18next'
import { ApiClientError } from '../api/client'

type Props = { error: unknown }

export default function ApiErrorView({ error }: Props) {
  const { t } = useTranslation()
  const err = error as ApiClientError

  return (
    <div className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-rose-900">
      <p className="font-semibold">{t('error.title')}</p>
      <p className="mt-1 text-sm">{err?.message ?? t('common.notSpecified')}</p>
      <p className="mt-1 text-xs opacity-80">
        {t('error.code')}: {err?.code ?? 'unknown'}
      </p>
    </div>
  )
}

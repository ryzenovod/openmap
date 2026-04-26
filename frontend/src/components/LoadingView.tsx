import { useTranslation } from 'react-i18next'

export default function LoadingView() {
  const { t } = useTranslation()

  return <div className="rounded-xl bg-slate-100 p-8 text-center text-slate-600">{t('common.loading')}</div>
}

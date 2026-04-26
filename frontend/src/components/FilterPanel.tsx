import { useState } from 'react'
import { useTranslation } from 'react-i18next'

export type MapFilters = {
  dateFrom: string
  dateTo: string
  level: string
  territory: string
  mkb: string
  gdu: string
  cv: string
  mbt: string
}

export const DEFAULT_FILTERS: MapFilters = {
  dateFrom: '2025-01-01',
  dateTo: '2025-12-31',
  level: '',
  territory: '',
  mkb: '',
  gdu: '',
  cv: '',
  mbt: '',
}

export default function FilterPanel({ onApply }: { onApply: (f: MapFilters) => void }) {
  const { t } = useTranslation()
  const [filters, setFilters] = useState<MapFilters>(DEFAULT_FILTERS)

  return (
    <div className="space-y-4">
      <h3 className="text-base font-semibold text-slate-900">{t('filters.title')}</h3>

      <FilterField
        label={t('filters.dateFrom')}
        type="date"
        value={filters.dateFrom}
        onChange={(v) => setFilters((prev) => ({ ...prev, dateFrom: v }))}
      />
      <FilterField
        label={t('filters.dateTo')}
        type="date"
        value={filters.dateTo}
        onChange={(v) => setFilters((prev) => ({ ...prev, dateTo: v }))}
      />

      <FilterField
        label={t('filters.level')}
        value={filters.level}
        onChange={(v) => setFilters((prev) => ({ ...prev, level: v }))}
      />
      <FilterField
        label={t('filters.territory')}
        value={filters.territory}
        onChange={(v) => setFilters((prev) => ({ ...prev, territory: v }))}
      />
      <FilterField
        label={t('filters.mkb')}
        value={filters.mkb}
        onChange={(v) => setFilters((prev) => ({ ...prev, mkb: v }))}
      />
      <FilterField
        label={t('filters.gdu')}
        value={filters.gdu}
        onChange={(v) => setFilters((prev) => ({ ...prev, gdu: v }))}
      />
      <FilterField
        label={t('filters.cv')}
        value={filters.cv}
        onChange={(v) => setFilters((prev) => ({ ...prev, cv: v }))}
      />
      <FilterField
        label={t('filters.mbt')}
        value={filters.mbt}
        onChange={(v) => setFilters((prev) => ({ ...prev, mbt: v }))}
      />

      <div className="flex gap-2 pt-2">
        <button className="btn-primary" onClick={() => onApply(filters)}>
          {t('common.apply')}
        </button>
        <button
          className="btn-secondary"
          onClick={() => {
            setFilters(DEFAULT_FILTERS)
            onApply(DEFAULT_FILTERS)
          }}
        >
          {t('common.reset')}
        </button>
      </div>
    </div>
  )
}

function FilterField({
  label,
  value,
  onChange,
  type = 'text',
}: {
  label: string
  value: string
  onChange: (value: string) => void
  type?: string
}) {
  return (
    <label className="block space-y-1">
      <span className="text-sm text-slate-600">{label}</span>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={label}
        className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-100"
      />
    </label>
  )
}

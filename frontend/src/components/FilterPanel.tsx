import { useState } from 'react'

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

const DEFAULTS: MapFilters = {
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
  const [filters, setFilters] = useState<MapFilters>(DEFAULTS)

  return (
    <div>
      <h3>Filters</h3>
      {Object.entries(filters).map(([key, value]) => (
        <label key={key} className="filter-field">
          <span>{key}</span>
          <input
            value={value}
            onChange={(e) => setFilters((prev) => ({ ...prev, [key]: e.target.value }))}
            placeholder={key}
          />
        </label>
      ))}
      <div className="filter-actions">
        <button onClick={() => onApply(filters)}>Apply</button>
        <button
          onClick={() => {
            setFilters(DEFAULTS)
            onApply(DEFAULTS)
          }}
        >
          Reset
        </button>
      </div>
    </div>
  )
}

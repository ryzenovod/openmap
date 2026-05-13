import { useMemo, useState } from 'react'
import type { Feature, GeoJsonObject, Geometry } from 'geojson'
import type { Layer, PathOptions, TileErrorEvent } from 'leaflet'
import { useTranslation } from 'react-i18next'
import { GeoJSON, MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import type { MapAggregateRow, TerritoryGeoJson, TerritoryGeoJsonProperties } from '../types/api'

const center: [number, number] = [43.12, 131.9]

// Примерные границы Приморского края с запасом, центр во Владивостоке. Это ограничит перемещение карты за пределы региона, но позволит видеть всю его территорию.
// Формат Leaflet: [[southWestLat, southWestLng], [northEastLat, northEastLng]]
const primoryeBounds: [[number, number], [number, number]] = [
  [42.1, 130.0],
  [48.6, 140.0],
]

const legacyTileUrl = (import.meta.env.VITE_LEGACY_TILE_URL as string | undefined)?.trim()

type TerritoryFeature = Feature<Geometry | null, TerritoryGeoJsonProperties>

type MapViewProps = {
  rows: MapAggregateRow[]
  territoriesGeoJson?: TerritoryGeoJson | null
  vectorNotice?: string | null
  onSelect: (r: MapAggregateRow) => void
}

const neutralStyle: PathOptions = {
  color: '#64748b',
  fillColor: '#e2e8f0',
  fillOpacity: 0.22,
  opacity: 0.85,
  weight: 1,
}

const choroplethPalette = ['#dbeafe', '#bfdbfe', '#7dd3fc', '#38bdf8', '#0284c7']

export default function MapView({ rows, territoriesGeoJson, vectorNotice, onSelect }: MapViewProps) {
  const { t } = useTranslation()
  const [tilesUnavailable, setTilesUnavailable] = useState(!legacyTileUrl)
  const hasTerritoryFeatures = Boolean(territoriesGeoJson?.features.length)
  const aggregateByTerritory = useMemo(() => {
    return new Map(rows.map((row) => [row.territory_id, row]))
  }, [rows])
  const maxMetric = useMemo(() => {
    return rows.reduce((max, row) => Math.max(max, metricValue(row)), 0)
  }, [rows])
  const geoJsonLayerKey = useMemo(() => {
    const rowKey = rows
      .map((row) => `${row.territory_id}:${row.case_count}:${row.incidence_per_100k ?? ''}`)
      .join('|')
    return `${territoriesGeoJson?.features.length ?? 0}:${rowKey}`
  }, [rows, territoriesGeoJson])

  const territoryStyle = (feature?: TerritoryFeature): PathOptions => {
    const territoryId = getFeatureTerritoryId(feature)
    const aggregate = territoryId ? aggregateByTerritory.get(territoryId) : undefined
    const value = aggregate ? metricValue(aggregate) : 0
    if (!aggregate || value <= 0 || maxMetric <= 0) {
      return neutralStyle
    }

    return {
      ...neutralStyle,
      color: '#0f766e',
      fillColor: colorForMetric(value, maxMetric),
      fillOpacity: 0.48,
      weight: 1.2,
    }
  }

  const bindTerritoryFeature = (feature: TerritoryFeature, layer: Layer) => {
    const territoryId = getFeatureTerritoryId(feature)
    const aggregate = territoryId ? aggregateByTerritory.get(territoryId) : undefined
    const territoryName =
      feature.properties?.territory_name ??
      aggregate?.territory_name ??
      (territoryId ? `Территория ${territoryId}` : 'Территория')

    if (aggregate) {
      layer.on({ click: () => onSelect(aggregate) })
    }

    layer.bindPopup(buildTerritoryPopup(territoryName, aggregate))
  }

  return (
    <div className="relative overflow-hidden rounded-xl">
      <MapContainer
        center={center}
        zoom={10}
        minZoom={7}
        maxZoom={19}
        maxBounds={primoryeBounds}
        maxBoundsViscosity={1.0}
        style={{ height: '560px', width: '100%' }}
      >
        {legacyTileUrl ? (
          <TileLayer
            attribution="Локальная растровая подложка"
            url={legacyTileUrl}
            minZoom={7}
            maxZoom={19}
            minNativeZoom={0}
            maxNativeZoom={19}
            bounds={primoryeBounds}
            eventHandlers={{
              tileerror: (e: TileErrorEvent) => {
                // Ошибка одного тайла не означает, что вся локальная подложка недоступна.
                console.warn('Tile load error:', e.tile?.src)
              },
              tileload: () => setTilesUnavailable(false),
            }}
          />
        ) : null}
        {hasTerritoryFeatures ? (
          <GeoJSON
            key={geoJsonLayerKey}
            data={territoriesGeoJson as GeoJsonObject}
            style={(feature) => territoryStyle(feature as TerritoryFeature | undefined)}
            onEachFeature={(feature, layer) =>
              bindTerritoryFeature(feature as TerritoryFeature, layer)
            }
          />
        ) : null}
        {!hasTerritoryFeatures ? rows.map((row, idx) => (
          <Marker
            key={`${row.territory_id}-${idx}`}
            position={[43 + idx * 0.1, 131 + idx * 0.1]}
            eventHandlers={{ click: () => onSelect(row) }}
          >
            <Popup>
              <strong>{row.territory_name ?? `Территория ${row.territory_id}`}</strong>
              <div>Случаев: {row.case_count}</div>
            </Popup>
          </Marker>
        )) : null}
      </MapContainer>
      {tilesUnavailable ? (
        <div className="pointer-events-none absolute inset-x-4 top-4 z-[1000] rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-medium text-amber-900 shadow-sm">
          {t('map.localTilesUnavailable')}
        </div>
      ) : null}
      {vectorNotice ? (
        <div className="pointer-events-none absolute inset-x-4 bottom-4 z-[1000] rounded-lg border border-slate-200 bg-white/95 px-4 py-3 text-sm font-medium text-slate-700 shadow-sm">
          {vectorNotice}
        </div>
      ) : null}
    </div>
  )
}

function metricValue(row: MapAggregateRow): number {
  return row.incidence_per_100k ?? row.case_count
}

function colorForMetric(value: number, maxMetric: number): string {
  const ratio = value / maxMetric
  if (ratio <= 0.2) return choroplethPalette[0]
  if (ratio <= 0.4) return choroplethPalette[1]
  if (ratio <= 0.6) return choroplethPalette[2]
  if (ratio <= 0.8) return choroplethPalette[3]
  return choroplethPalette[4]
}

function getFeatureTerritoryId(feature?: TerritoryFeature): number | null {
  const rawId = feature?.properties?.territory_id
  if (rawId === null || rawId === undefined || rawId === '') {
    return null
  }

  const territoryId = Number(rawId)
  return Number.isFinite(territoryId) ? territoryId : null
}

function buildTerritoryPopup(territoryName: string, aggregate?: MapAggregateRow): string {
  if (!aggregate) {
    return `<strong>${escapeHtml(territoryName)}</strong><div>Нет агрегатов для территории</div>`
  }

  const rows = [
    `<strong>${escapeHtml(territoryName)}</strong>`,
    `<div>Случаев: ${aggregate.case_count}</div>`,
  ]
  if (aggregate.incidence_per_100k !== null) {
    rows.push(
      `<div>Заболеваемость на 100 тыс.: ${formatNumber(aggregate.incidence_per_100k)}</div>`,
    )
  }
  return rows.join('')
}

function formatNumber(value: number): string {
  return new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 1 }).format(value)
}

function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, (char) => {
    const replacements: Record<string, string> = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;',
    }
    return replacements[char]
  })
}

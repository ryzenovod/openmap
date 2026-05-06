import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import type { MapAggregateRow } from '../types/api'

const center: [number, number] = [43.12, 131.9]

// Примерные границы Приморского края с запасом, центр во Владивостоке. Это ограничит перемещение карты за пределы региона, но позволит видеть всю его территорию.
// Формат Leaflet: [[southWestLat, southWestLng], [northEastLat, northEastLng]]
const primoryeBounds: [[number, number], [number, number]] = [
  [42.1, 130.0],
  [48.6, 140.0],
]

const legacyTileUrl = (import.meta.env.VITE_LEGACY_TILE_URL as string | undefined)?.trim()

export default function MapView({ rows, onSelect }: { rows: MapAggregateRow[]; onSelect: (r: MapAggregateRow) => void }) {
  const { t } = useTranslation()
  const [tilesUnavailable, setTilesUnavailable] = useState(!legacyTileUrl)

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
              tileerror: (e: any) => {
                // Ошибка одного тайла не означает, что вся локальная подложка недоступна.
                console.warn('Tile load error:', e.tile?.src)
              },
              tileload: () => setTilesUnavailable(false),
            }}
          />
        ) : null}
        {rows.map((row, idx) => (
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
        ))}
      </MapContainer>
      {tilesUnavailable ? (
        <div className="pointer-events-none absolute inset-x-4 top-4 z-[1000] rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-medium text-amber-900 shadow-sm">
          {t('map.localTilesUnavailable')}
        </div>
      ) : null}
    </div>
  )
}

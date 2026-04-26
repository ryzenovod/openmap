import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import type { MapAggregateRow } from '../types/api'

const center: [number, number] = [43.1, 131.9]
const legacyTiles = import.meta.env.VITE_LEGACY_TILE_URL as string | undefined

export default function MapView({ rows, onSelect }: { rows: MapAggregateRow[]; onSelect: (r: MapAggregateRow) => void }) {
  const tileUrl = legacyTiles?.trim() || 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

  return (
    <MapContainer center={center} zoom={7} style={{ height: '560px', width: '100%' }} className="rounded-xl">
      <TileLayer attribution="&copy; OpenStreetMap contributors" url={tileUrl} />
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
  )
}

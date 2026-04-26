import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import type { MapAggregateRow } from '../types/api'

const center: [number, number] = [43.1, 131.9]

export default function MapView({ rows, onSelect }: { rows: MapAggregateRow[]; onSelect: (r: MapAggregateRow) => void }) {
  return (
    <MapContainer center={center} zoom={7} style={{ height: '420px', width: '100%' }}>
      <TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {rows.map((row, idx) => (
        <Marker key={`${row.territory_id}-${idx}`} position={[43 + idx * 0.1, 131 + idx * 0.1]} eventHandlers={{ click: () => onSelect(row) }}>
          <Popup>
            <strong>{row.territory_name ?? `Territory ${row.territory_id}`}</strong>
            <div>cases: {row.case_count}</div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}

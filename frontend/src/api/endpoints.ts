import { getEnvelope, getHealth, getJson } from './client'
import type {
  CaseDetailRow,
  CaseListRow,
  MapAggregateRow,
  StructurePayload,
  TerritoryGeoJson,
  YearlyRow,
} from '../types/api'

type RequestOptions = {
  signal?: AbortSignal
}

export const api = {
  health: () => getHealth(),
  mapAggregate: (query: string, options: RequestOptions = {}) =>
    getEnvelope<MapAggregateRow[]>(`/api/v1/map/aggregate${query}`, options),
  mapTerritoriesGeoJson: (options: RequestOptions = {}) =>
    getJson<TerritoryGeoJson>('/api/v1/map/territories.geojson', options),
  yearly: () => getEnvelope<YearlyRow[]>('/api/v1/charts/yearly'),
  structure: () => getEnvelope<StructurePayload>('/api/v1/charts/structure'),
  cases: (query: string) => getEnvelope<CaseListRow[]>(`/api/v1/cases${query}`),
  caseDetail: (id: number) => getEnvelope<CaseDetailRow>(`/api/v1/cases/${id}`),
}

import { getEnvelope, getHealth } from './client'
import type {
  CaseDetailRow,
  CaseListRow,
  MapAggregateRow,
  StructurePayload,
  YearlyRow,
} from '../types/api'

export const api = {
  health: () => getHealth(),
  mapAggregate: (query: string) => getEnvelope<MapAggregateRow[]>(`/api/v1/map/aggregate${query}`),
  yearly: () => getEnvelope<YearlyRow[]>('/api/v1/charts/yearly'),
  structure: () => getEnvelope<StructurePayload>('/api/v1/charts/structure'),
  cases: (query: string) => getEnvelope<CaseListRow[]>(`/api/v1/cases${query}`),
  caseDetail: (id: number) => getEnvelope<CaseDetailRow>(`/api/v1/cases/${id}`),
}

export type ErrorEnvelope = {
  error: {
    code: string
    message: string
    details: unknown
  }
}

export type Envelope<T> = {
  data: T
  meta?: Record<string, unknown>
}

export type HealthResponse = { status: string }

export type MapAggregateRow = {
  aggregation_date: string
  territory_id: number
  territory_name: string | null
  territory_type_code: string | null
  case_count: number
  mbt_positive_count: number
  cv_positive_count: number
  children_count: number
  incidence_per_100k: number | null
}

export type YearlyRow = { year: number; case_count: number }

export type StructureRow = {
  year: number
  dimension: string
  bucket: string
  territory_id: number | null
  case_count: number
}

export type StructurePayload = {
  by_mkb: StructureRow[]
  by_sex: StructureRow[]
  by_age_group: StructureRow[]
  territorial_comparison: StructureRow[]
}

export type CaseListRow = {
  id: number
  patient_id: number
  legacy_case_num: string | null
  registration_date: string
  diagnosis_raw: string
}

export type CaseDetailRow = CaseListRow & {
  gdu_code: string | null
  cv_code: string | null
  mbt_code: string | null
}

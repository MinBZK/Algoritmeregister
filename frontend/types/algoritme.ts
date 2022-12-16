export interface Algoritme {
  id: string
  slug: string
  name: string
  organization: string
  department: string
  description_short: string
  type: string
  category: string
  website: string
  status: string
}

type AggregationValue = {
  aggregation_value: string
  count: number
}

export type AggregatedAlgoritme = {
  aggregation_attribute: string
  // aggregationType: string
  values: AggregationValue[]
}

export type AlgoritmeFilter = {
  attribute: string
  value: string | string[]
}

export interface AlgNameIdOrg {
  id: string
  name: string
  organization: string
  slug: string
}

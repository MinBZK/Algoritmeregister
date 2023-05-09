export interface Algoritme {
  algoritme_id: string
  name: string
  lars: string
  standard_version: string

  [key: string]: string
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

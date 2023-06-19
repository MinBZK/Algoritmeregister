export interface Algoritme {
  algoritme_id: string
  name: string
  lars: string
  standard_version: string

  [key: string]: null | string | string[]
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

export interface AlgorithmFieldDisplay {
  key: string
  value: string
  keyDescription: string
  keyLabel: string
}

export interface AlgorithmDisplay {
  key: string
  keyLabel: string
  properties: AlgorithmFieldDisplay[]
}

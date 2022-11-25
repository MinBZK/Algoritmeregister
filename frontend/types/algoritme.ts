export interface Algoritme {
  id: string
  name: string
  organization: string
  department: string
  description_short: string
  type: string
  category: string
  website: string
  status: string
}

export type AggregatedAlgoritmes = {
  aggregationAttribute: string
  aggregationType: string
  aggregatedValues: Record<string, number>
}

export type AlgoritmeFilter = {
  attribute: string
  value: string
}

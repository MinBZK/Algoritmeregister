import type { FilterData, QueryBase } from '.'

export interface AlgoritmeFilterQuery {
  organisation?: string
  publicationcategory?: string
  organisationtype?: string
  impact_assessment?: string
}

export type AlgoritmeQuery = QueryBase & AlgoritmeFilterQuery

export interface AlgoritmeSelectedFilter {
  key: keyof AlgoritmeFilterQuery | 'searchtext'
  value?: string
}

export type AlgoritmeFilterData = {
  [K in keyof AlgoritmeFilterQuery]: FilterData[]
}

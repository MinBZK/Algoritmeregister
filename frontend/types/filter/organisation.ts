import type { FilterData, QueryBase } from '.'

export interface OrganisationFilterQuery {
  organisationtype?: string
}

export type OrganisationQuery = QueryBase & OrganisationFilterQuery

export interface OrganisationSelectedFilter {
  key: keyof OrganisationFilterQuery | 'searchtext'
  value?: string
}

export type OrganisationFilterData = {
  [K in keyof OrganisationFilterQuery]: FilterData[]
}

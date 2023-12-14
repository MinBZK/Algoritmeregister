import { OrgType } from './organisation'

export interface OrganisationPresenceCount {
  name: string
  count: number
}

export interface OrganisationFilterGroup {
  type: OrgType
  organisations: OrganisationPresenceCount[]
}

export interface FilterData {
  organisation: OrganisationFilterGroup[]
}

export interface SelectedFilter {
  name: string
  value?: string
}

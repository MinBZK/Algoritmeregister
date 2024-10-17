import { FastApiResponse } from '.'
import { Language } from './misc'

export interface OrganisationDetails {
  about: string
  contact_info: string
  organisation_id: number
  id: number
  create_dt: string
  language: Language
}

export interface OrganisationDetailsResponse extends FastApiResponse {
  data: OrganisationDetails
}

export interface UpdateOrganisationDetailsResponse extends FastApiResponse {
  data: OrganisationDetails
}

import type { Algoritme } from './algoritme'
import type {
  OrganisationFilterData,
  OrganisationSelectedFilter,
} from './filter/organisation'

export interface OrganisationPage {
  contact_info: string
  about: string
  name: string
  show_page: boolean
  algoritme_versions: Algoritme[]
}

export interface Organisation {
  code: string
  count: string
  name: string
  show_page: boolean
  type: string
  org_id: string
}

export interface OrganisationMappingResult {
  name: string
  code: string
  org_id: string
  show_page: boolean
  count: number
}

export interface OrganisationSearchSuggestionResponse {
  organisations: OrganisationMappingResult[]
}

export interface OrganisationQueryResult {
  results: Organisation[]
  total_count: number
  filter_data: OrganisationFilterData
  selected_filters: OrganisationSelectedFilter[]
}

export interface OrganisationCodeResponse {
  code: string
  org_id: string
}

export interface OrganisationRelationHierarchy {
  org_id: string
  name: string | null
}

export interface OrganisationRelationResponse {
  org_id: string
  hierarchy_path: string
  hierarchy: OrganisationRelationHierarchy[]
}

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
}

export interface OrganisationMappingResult {
  name: string
  code: string
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

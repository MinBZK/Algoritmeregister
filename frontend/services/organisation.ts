import type { Language } from '@/types/algoritme'
import type { OrganisationQuery } from '@/types/filter/organisation'
import type {
  OrganisationPage,
  OrganisationQueryResult,
  OrganisationSearchSuggestionResponse,
} from '@/types/organisation'

const getOne = (orgCode: string, language: Language) =>
  useFetch<OrganisationPage>(`/organisation-details/${orgCode}/${language}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getMany = (query: OrganisationQuery, language: Language) => {
  if (!query.searchtext) {
    delete query.searchtext
  }
  return useFetch<OrganisationQueryResult>(`/organisation/${language}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'POST',
    body: query,
  })
}

const getFullNameOrganisation = (search: string, language: Language) =>
  useFetch<OrganisationSearchSuggestionResponse | null>(
    `/organisation/${language}/${search}`,
    {
      baseURL: useRuntimeConfig().public.apiBaseUrl,
    }
  )

const getCountOrganisation = (language: Language) =>
  useFetch<number>(`/organisation-count/${language}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

export default {
  getOne,
  getMany,
  getFullNameOrganisation,
  getCountOrganisation,
}

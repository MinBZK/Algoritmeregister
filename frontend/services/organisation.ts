import type { Language } from '@/types/algoritme'
import type { OrganisationQuery } from '@/types/filter/organisation'
import type {
  OrganisationCodeResponse,
  OrganisationPage,
  OrganisationQueryResult,
  OrganisationRelationResponse,
  OrganisationSearchSuggestionResponse,
} from '@/types/organisation'

const getOne = (orgId: string, language: Language) =>
  useFetch<OrganisationPage>(`/organisation-details/${orgId}/${language}`, {
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

const getOrgIdByCode = async (orgCode: string) => {
  return await $fetch<OrganisationCodeResponse>(`/organisation/${orgCode}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })
}

const getOrgRelationById = (orgId: string) => {
  return useFetch<OrganisationRelationResponse>(
    `/organisation-relation/${orgId}`,
    {
      baseURL: useRuntimeConfig().public.apiBaseUrl,
    }
  )
}

export default {
  getOne,
  getMany,
  getFullNameOrganisation,
  getCountOrganisation,
  getOrgIdByCode,
  getOrgRelationById,
}

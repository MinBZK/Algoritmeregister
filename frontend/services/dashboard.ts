import type { DocumentCount } from './aggregates'
import type { Language } from '@/types/algoritme'
import type {
  OrganisationTop20,
  PublicationCategoriesCount,
  MonthlyCount,
  HtmlFiguresRecent,
  NationalOrganisationsCountDashboard,
} from '@/types/dashboard'

const getJoinedOrg = () => {
  return useFetch<MonthlyCount[]>('/organisation/joined-permonth', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })
}

const getPublishedAlg = () => {
  return useFetch<MonthlyCount[]>('/algorithm/published-permonth', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })
}

const getOrgTop20 = (language: Language) => {
  return useFetch<OrganisationTop20[]>(`/organisation/top-20/${language}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })
}

const getPubCategories = (language: Language) => {
  return useFetch<PublicationCategoriesCount[]>(
    `/algorithm/publication-categories/${language}`,
    {
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      method: 'GET',
    }
  )
}

const getNationalOrgs = (language: Language) => {
  return useFetch<NationalOrganisationsCountDashboard[]>(
    `/algorithm/national-organisations/${language}`,
    {
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      method: 'GET',
    }
  )
}

const getMunicipalityData = () => {
  return useFetch<DocumentCount[]>('/organisation/municipalities', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })
}

const getProvinceData = () => {
  return useFetch<DocumentCount[]>('/organisation/provinces', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })
}

const getWaterAuthorityData = () => {
  return useFetch<DocumentCount[]>('/organisation/water-authorities', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })
}

const getEnvironmentalServiceData = () => {
  return useFetch<DocumentCount[]>('/organisation/environmental-services', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })
}

const getSafetyData = () => {
  return useFetch<DocumentCount[]>('/organisation/safety-regions', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })
}

const getHtmlFiguresRecent = () =>
  useFetch<HtmlFiguresRecent>(`/dashboard/figures`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

export default {
  getHtmlFiguresRecent,
  getJoinedOrg,
  getPublishedAlg,
  getOrgTop20,
  getNationalOrgs,
  getPubCategories,
  getMunicipalityData,
  getProvinceData,
  getWaterAuthorityData,
  getEnvironmentalServiceData,
  getSafetyData,
}

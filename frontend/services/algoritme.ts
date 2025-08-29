import type {
  Algoritme,
  Language,
  HighlightedAlgoritme,
  Suggestion,
} from '@/types/algoritme'
import type {
  AlgoritmeFilterData,
  AlgoritmeSelectedFilter,
  AlgoritmeQuery,
} from '@/types/filter/algoritme'

export type AlgoritmeQueryResult = {
  scores: number[] | null
  results: Algoritme[]
  total_count: number
  filter_data: AlgoritmeFilterData
  selected_filters: AlgoritmeSelectedFilter[]
}

export type SearchSuggestionResult = {
  algorithms: Suggestion[]
}

const getAll = (query: AlgoritmeQuery, language: Language) => {
  if (!query.searchtext) {
    delete query.searchtext
  }
  return useFetch<AlgoritmeQueryResult>(`/algoritme/${language}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'POST',
    body: query,
  })
}

// 'Get' version of the getAll service, but does not seem to load properly.
// const getAll = (query: AlgoritmeQuery) => {
//   if (!query.searchtext) {
//     delete query.searchtext
//   }
//   return useFetch<AlgoritmeQueryResult>('/algoritme/', {
//     baseURL: useRuntimeConfig().public.apiBaseUrl,
//     query,
//   })
// }

const getOne = (id: string, language: Language) =>
  useFetch<Algoritme>(`/algoritme/${language}/${id}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getCount = (column: string) =>
  useFetch<any>(`/db-count/${column}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getTotalCount = () =>
  useFetch<number>(`/algoritme/total-count`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getHighlighted = (language: Language) =>
  useFetch<HighlightedAlgoritme[]>(`/precomputed/${language}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getColumns = () =>
  // useFetch<[{ table_name: string; column_name: string; is_nullable: string }]>(
  useFetch<{ column_name: string; is_nullable: string }[]>(`/columns/`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getCountWithFilledColumns = (columns: string[] | string) =>
  useFetch<any>(`/completeness/`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    query: { columns },
  })

const getApiStandard = (version: string) =>
  useFetch<any>('/v' + version.replace(/\./g, '_') + '/openapi.json', {
    baseURL: useRuntimeConfig().public.aanleverBaseUrl,
  })

const downloadAllUrl = (language: Language) => {
  return `${useRuntimeConfig().public.apiBaseUrl}/downloads/${language}`
}

const downloadAllPublishedVersionsUrl = (language: Language) => {
  return `${useRuntimeConfig().public.apiBaseUrl}/downloads/history/${language}`
}

const downloadOneUrl = (lars: string, language: Language) => {
  return `${
    useRuntimeConfig().public.apiBaseUrl
  }/downloads/algorithms/${lars}/${language}`
}

const downloadAllPublishedVersionsOneUrl = (
  lars: string,
  language: Language
) => {
  return `${
    useRuntimeConfig().public.apiBaseUrl
  }/downloads/history/algorithms/${lars}/${language}`
}

const getSearchSuggestion = (search: string, language: Language) =>
  useFetch<SearchSuggestionResult>(`/suggestion/${language}/${search}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getSimilar = (lars: string, language: Language) => {
  return useFetch<AlgoritmeQueryResult>(
    `/algoritme/${language}/similar/${lars}`,
    {
      baseURL: useRuntimeConfig().public.apiBaseUrl,
    }
  )
}

export default {
  getAll,
  getOne,
  getCount,
  getHighlighted,
  getTotalCount,
  getColumns,
  getCountWithFilledColumns,
  getApiStandard,
  downloadAllUrl,
  downloadAllPublishedVersionsUrl,
  downloadOneUrl,
  downloadAllPublishedVersionsOneUrl,
  getSearchSuggestion,
  getSimilar,
}

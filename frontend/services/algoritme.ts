import type {
  Algoritme,
  AlgNameIdOrg,
  AlgoritmeFilter,
  AggregatedAlgoritme,
} from '@/types/algoritme'

type AlgoritmeQuery = {
  filters: AlgoritmeFilter[]
  page: number
  limit: number
  search?: string
}

type AlgoritmeQueryResult = {
  results: Algoritme[]
  total_count: number
  aggregations: AggregatedAlgoritme[]
}

const getAll = (query: AlgoritmeQuery) =>
  useFetch<AlgoritmeQueryResult>('/algoritme/', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'POST',
    body: query,
  })

const getOne = (slug: string) =>
  useFetch<Algoritme>(`/algoritme/${slug}/`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getNameIdOrg = () =>
  useFetch<AlgNameIdOrg[]>('/algoritme-simple-list/', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getCount = (column: string) =>
  useFetch<any>(`/db-count/${column}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getTotalCount = () =>
  useFetch<number>(`/db-count/`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getColumns = () =>
  // useFetch<[{ table_name: string; column_name: string; is_nullable: string }]>(
  useFetch<any>(`/columns/`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getCountWithFilledColumns = (columns: string[] | string) =>
  useFetch<any>(`/completeness/`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    query: { columns },
  })

const downloadUrl = () =>
  `${useRuntimeConfig().public.apiBaseUrl}/file/algoritme`

export default {
  getAll,
  getOne,
  getNameIdOrg,
  getCount,
  getTotalCount,
  getColumns,
  getCountWithFilledColumns,
  downloadUrl,
}

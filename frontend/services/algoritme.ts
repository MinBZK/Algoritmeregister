import type { Algoritme, AlgNameIdOrg } from '@/types/algoritme'

const getAll = () =>
  useFetch<Algoritme[]>('/algoritme/', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
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

// import { apiFetch } from '@/utils/fetchApi'
import type { Algoritme, AlgNameIdOrg } from '@/types/algoritme'

const getAll = () =>
  useFetch<Algoritme[]>('/algoritme/', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getOne = (id: string) =>
  useFetch<Algoritme>(`/algoritme/${id}/`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getNameIdOrg = () =>
  useFetch<AlgNameIdOrg[]>('/algoritme-simple-list/', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

export default { getAll, getOne, getNameIdOrg }

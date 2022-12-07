// import { apiFetch } from '@/utils/fetchApi'
import type { Algoritme, AlgNamesOnly } from '@/types/algoritme'

const getAll = () =>
  useFetch<Algoritme[]>('/algoritme/', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getOne = (id: string) =>
  useFetch<Algoritme>(`/algoritme/${id}/`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getNames = () =>
  useFetch<AlgNamesOnly[]>('/algoritme-simple-list/', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

export default { getAll, getOne, getNames }

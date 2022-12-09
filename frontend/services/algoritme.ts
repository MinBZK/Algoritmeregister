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

export default { getAll, getOne, getNameIdOrg }

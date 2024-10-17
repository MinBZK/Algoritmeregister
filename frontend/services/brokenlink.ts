import type { Language } from '@/types/algoritme'
import type { BrokenLink } from '@/types/brokenlink'

const getBrokenLinks = (language: Language) =>
  useFetch<BrokenLink[]>(`/broken-links/${language}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

export default {
  getBrokenLinks,
}

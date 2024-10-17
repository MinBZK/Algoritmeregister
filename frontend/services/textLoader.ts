import type { SupportingText } from '@/types/textLoader'

const getAllContent = async () =>
  await useFetch<SupportingText>(`/supporting-text`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })

export { getAllContent }

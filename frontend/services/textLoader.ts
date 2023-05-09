import { SupportingText } from '@/types/textLoader'

const getAllContent = () =>
  useFetch<SupportingText>(`/supporting-text`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })

export { getAllContent }

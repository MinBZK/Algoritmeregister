import { NoOrgResponse } from '@/types/algorithm'
import { useFormDataStore } from '@/store/form-data'
import content from '@/content.json'

export function noOrgSelectedResponse(): NoOrgResponse {
  const dataStore = useFormDataStore()
  dataStore.feedback.error = content.Misc.noOrgSelected.error
  return { status: 400, data: null }
}

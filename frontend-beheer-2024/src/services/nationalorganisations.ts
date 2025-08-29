import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'
import { NationalOrganisationsCountResponse } from '@/types/nationalorganisations'

export async function getNationalOrganisations(): Promise<NationalOrganisationsCountResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/algorithm/national-organisations/NLD',
  }
  return backendRequest(request)
}
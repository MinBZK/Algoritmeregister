import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'
import { BrokenLinkResponse } from '@/types/brokenlink'

export async function getBrokenLinks(): Promise<BrokenLinkResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/broken-links/NLD',
  }
  return backendRequest(request)
}
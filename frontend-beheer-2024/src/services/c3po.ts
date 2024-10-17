import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'
import { C3poResponse } from '@/types/c3po'

export async function postC3poRequest(text: string): Promise<C3poResponse> {
  const request: AxiosRequestConfig = {
    method: 'POST',
    url: '/c3po/processing-request',
    data: { text },
  }
  return backendRequest(request) as unknown as Promise<C3poResponse>
}

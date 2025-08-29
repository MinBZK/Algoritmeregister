import { Organisation } from '@/types/organisation'
import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'

export async function getFileOne(
  organisation: Organisation,
  lars: string,
  filetype: 'pdf' | 'word' | 'excel'
) {
  const request: AxiosRequestConfig = {
    method: 'GET',
    responseType: 'blob',
    url: `downloads/organizations/${organisation.org_id}/algorithms/${lars}`,
    params: { filetype: filetype },
  }
  return backendRequest(request)
}

export async function getFileMany(
  organisation: Organisation,
  filetype: 'pdf' | 'word' | 'excel'
) {
  const request: AxiosRequestConfig = {
    method: 'GET',
    responseType: 'blob',
    url: `downloads/organizations/${organisation.org_id}`,
    params: { filetype: filetype },
  }
  return backendRequest(request)
}

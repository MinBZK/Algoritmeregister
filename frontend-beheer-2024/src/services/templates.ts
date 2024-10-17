import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'
import { TemplateListResponse, TemplateResponse } from '@/types/templates'

export async function getTemplateList(
  standardVersion: string
): Promise<TemplateListResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `templates/${standardVersion}`,
  }
  return backendRequest(request)
}

export async function getTemplate(
  standardVersion: string,
  id: string
): Promise<TemplateResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `templates/${standardVersion}/${id}`,
  }
  return backendRequest(request)
}

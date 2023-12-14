import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'
import {
  C3poPostResponse,
  C3poRequestBody,
  C3poRulesResponse,
} from '@/types/c3po'

export async function postC3poRequest(
  data: C3poRequestBody
): Promise<C3poPostResponse> {
  const request: AxiosRequestConfig = {
    method: 'POST',
    url: '/c3po/processing-request',
    data,
  }
  return backendRequest(request)
}

export async function getC3poRules(): Promise<C3poRulesResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/c3po/rule',
  }
  return backendRequest(request)
}

import axios, { AxiosRequestConfig, AxiosResponse } from 'axios'
import { MetaDataResponse } from '@/types/openapi'

export function backendRequest<FastApiResponse>(
  config: AxiosRequestConfig
): Promise<AxiosResponse<FastApiResponse>> {
  return new Promise((resolve, reject) => {
    axios(config)
      .then((response) => {
        resolve(response)
      })
      .catch((error) => {
        reject({
          status: error.response?.status ?? 500,
          data: error.response?.data.detail ?? 'Er is iets misgegaan.',
        })
      })
  })
}

export async function getMetaDataStandard(
  version: string
): Promise<MetaDataResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `v${version.replace(/\./g, '_')}/openapi.json`,
  }
  return backendRequest(request)
}

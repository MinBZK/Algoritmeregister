import axios, { AxiosRequestConfig, AxiosResponse } from 'axios'
import config from '@/app-config'
import { Organization } from '@/types'
import { MetaDataResponse } from '@/types/form'
import {
  AlgorithmForm,
  AlgorithmListResponse,
  AlgorithmResponse,
  AlgorithmPreviewResponse,
  UpdateAlgorithmResponse,
  CreateAlgorithmResponse,
  RemoveAlgorithmResponse,
} from '@/types/algorithm'

const MDS_VERSION =
  'v' + config.metaDataStandard.preferredVersion.replace(/\./g, '_')

function backendRequest<FastApiResponse>(
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

export async function getAlgorithm(
  organization: Organization,
  lars: string
): Promise<AlgorithmResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `${MDS_VERSION}/organizations/${organization.id}/algorithms/${lars}`,
  }
  return backendRequest(request)
}

export async function getAlgorithmList(
  organization: Organization
): Promise<AlgorithmListResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `${MDS_VERSION}/organizations/${organization.id}/algorithms`,
  }
  return backendRequest(request)
}

export async function createAlgorithm(
  organization: Organization,
  data: AlgorithmForm
): Promise<CreateAlgorithmResponse> {
  delete data.created_by
  delete data.create_dt
  delete data.lars
  delete data.released
  delete data.published

  const request: AxiosRequestConfig = {
    method: 'POST',
    url: `v${data.standard_version.replace(/\./g, '_')}/organizations/${
      organization.id
    }/algorithms`,
    data,
  }
  return backendRequest(request)
}

export async function updateAlgorithm(
  organization: Organization,
  lars: string,
  data: AlgorithmForm
): Promise<UpdateAlgorithmResponse> {
  const sendData: AlgorithmForm = { ...data }
  delete sendData.create_dt
  delete sendData.lars
  delete sendData.released
  delete sendData.published

  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `v${sendData.standard_version.replace(/\./g, '_')}/organizations/${
      organization.id
    }/algorithms/${lars}`,
    data: sendData,
  }
  return backendRequest(request)
}

export async function publishAlgorithm(
  organization: Organization,
  lars: string
): Promise<AlgorithmResponse> {
  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `${MDS_VERSION}/organizations/${organization.id}/algorithms/${lars}/publish`,
  }
  return backendRequest(request)
}

export async function releaseAlgorithm(
  organization: Organization,
  lars: string
): Promise<AlgorithmResponse> {
  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `${MDS_VERSION}/organizations/${organization.id}/algorithms/${lars}/release`,
  }
  return backendRequest(request)
}

export async function retractAlgorithm(
  organization: Organization,
  lars: string
): Promise<AlgorithmResponse> {
  const request: AxiosRequestConfig = {
    method: 'DELETE',
    url: `${MDS_VERSION}/organizations/${organization.id}/published-algorithms/${lars}/retract`,
  }
  return backendRequest(request)
}

export async function generatePreview(
  organization: Organization,
  lars: string
): Promise<AlgorithmPreviewResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `${MDS_VERSION}/organizations/${organization.id}/algorithms/${lars}/preview`,
  }
  return backendRequest(request)
}

export async function removeAlgorithm(
  organization: Organization,
  lars: string
): Promise<RemoveAlgorithmResponse> {
  const request: AxiosRequestConfig = {
    method: 'DELETE',
    url: `${MDS_VERSION}/organizations/${organization.id}/algorithms/${lars}/remove`,
  }
  return backendRequest(request)
}

export async function getExcelFile(organization: Organization) {
  const request: AxiosRequestConfig = {
    method: 'GET',
    responseType: 'blob',
    url: `${MDS_VERSION}/organizations/${organization.id}/algorithms/download-excel`,
  }
  return backendRequest(request)
}

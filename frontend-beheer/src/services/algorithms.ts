import {
  AlgorithmForm,
  AlgorithmResponse,
  AlgorithmOwnerResponse,
  AlgorithmPreviewResponse,
  UpdateAlgorithmResponse,
  CreateAlgorithmResponse,
  RemoveAlgorithmResponse,
  AlgorithmListResponse,
  AlgorithmTotalCountResponse,
  ColumnResponse,
  ColumnCountResponse,
} from '@/types/algorithm'
import { Organisation } from '@/types/organisation'
import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'
import publicationStandard from '@/config/publication-standard'

const MDS_VERSION =
  'v' + publicationStandard.preferredVersion.replace(/\./g, '_')

export async function getAlgorithmList(
  organisation: Organisation
): Promise<AlgorithmListResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `${MDS_VERSION}/organizations/${organisation.org_id}/algorithms`,
  }
  return backendRequest(request)
}

export async function getAlgorithm(
  organisation: Organisation,
  lars: string
): Promise<AlgorithmResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `${MDS_VERSION}/organizations/${organisation.org_id}/algorithms/${lars}`,
  }
  return backendRequest(request)
}

export async function createAlgorithm(
  organisation: Organisation,
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
      organisation.org_id
    }/algorithms`,
    data,
  }
  return backendRequest(request)
}

export async function updateAlgorithm(
  organisation: Organisation,
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
      organisation.org_id
    }/algorithms/${lars}`,
    data: sendData,
  }
  return backendRequest(request)
}

export async function publishAlgorithm(
  organisation: Organisation,
  lars: string
): Promise<AlgorithmResponse> {
  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `${MDS_VERSION}/organizations/${organisation.org_id}/algorithms/${lars}/publish`,
  }
  return backendRequest(request)
}

export async function releaseAlgorithm(
  organisation: Organisation,
  lars: string
): Promise<AlgorithmResponse> {
  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `${MDS_VERSION}/organizations/${organisation.org_id}/algorithms/${lars}/release`,
  }
  return backendRequest(request)
}

export async function retractAlgorithm(
  organisation: Organisation,
  lars: string
): Promise<AlgorithmResponse> {
  const request: AxiosRequestConfig = {
    method: 'DELETE',
    url: `${MDS_VERSION}/organizations/${organisation.org_id}/published-algorithms/${lars}/retract`,
  }
  return backendRequest(request)
}

export async function generatePreview(
  organisation: Organisation,
  lars: string
): Promise<AlgorithmPreviewResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `${MDS_VERSION}/organizations/${organisation.org_id}/algorithms/${lars}/preview`,
  }
  return backendRequest(request)
}

export async function removeAlgorithm(
  organisation: Organisation,
  lars: string
): Promise<RemoveAlgorithmResponse> {
  const request: AxiosRequestConfig = {
    method: 'DELETE',
    url: `${MDS_VERSION}/organizations/${organisation.org_id}/algorithms/${lars}/remove`,
  }
  return backendRequest(request)
}

export async function getAlgorithmOwner(
  lars: string
): Promise<AlgorithmOwnerResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `/algoritme/find/${lars}`,
  }
  return backendRequest(request)
}

export async function getTotalCount(): Promise<AlgorithmTotalCountResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/algoritme/total-count',
  }
  return backendRequest(request)
}

export async function getColumns(): Promise<ColumnResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/columns/',
  }
  return backendRequest(request)
}

export async function getCount(column: string): Promise<ColumnCountResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `/db-count/${column}`,
  }
  return backendRequest(request)
}

export async function getCountWithFilledColumns(
  columns: string[] | string
): Promise<any> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/completeness/',
    params: { columns },
  }
  return backendRequest(request)
}

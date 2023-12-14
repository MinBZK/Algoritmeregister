import {
  Organisation,
  OrganisationListResponse,
  CreateOrganisationResponse,
  UpdateOrganisationResponse,
} from '@/types/organisation'
import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'

export async function getOrganisationList(): Promise<OrganisationListResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/organization',
  }
  return backendRequest(request)
}

export async function createOrganisation(
  organisation: Organisation
): Promise<CreateOrganisationResponse> {
  const request: AxiosRequestConfig = {
    method: 'POST',
    url: '/organization',
    data: organisation,
  }
  return backendRequest(request)
}

export async function updateOrganisation(
  org_code: string,
  organisation: Organisation
): Promise<UpdateOrganisationResponse> {
  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `/organization/${org_code}`,
    data: organisation,
  }
  return backendRequest(request)
}

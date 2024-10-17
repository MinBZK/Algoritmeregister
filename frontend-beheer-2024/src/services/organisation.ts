import {
  OrganisationsResponse,
  CreateOrganisationResponse,
  UpdateOrganisationResponse,
  UpdateOptInResponse,
  OrganisationUpdate,
  DeleteOrganisationResponse,
} from '@/types/organisation'
import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'

export interface getOrgQuery {
  limit?: number
  skip?: number
  q?: string
}

export async function getOrganisations(
  query?: getOrgQuery
): Promise<OrganisationsResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/organisation',
    params: query,
  }
  return backendRequest(request)
}

export async function createOrganisation(
  organisation: OrganisationUpdate
): Promise<CreateOrganisationResponse> {
  const request: AxiosRequestConfig = {
    method: 'POST',
    url: '/organisation',
    data: organisation,
  }
  return backendRequest(request)
}

export async function updateOrganisation(
  org_code: string,
  organisation: OrganisationUpdate
): Promise<UpdateOrganisationResponse> {
  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `/organisation/${org_code}`,
    data: organisation,
  }
  return backendRequest(request)
}

export async function updateOrganisationOptIn(
  org_code: string,
  change_to: boolean
): Promise<UpdateOptInResponse> {
  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `/organisation/${org_code}/show_page/${change_to}`,
  }
  return backendRequest(request)
}

export async function deleteOrganisation(
  org_code: string
): Promise<DeleteOrganisationResponse> {
  const request: AxiosRequestConfig = {
    method: 'DELETE',
    url: `/organisation/${org_code}`,
  }
  return backendRequest(request)
}

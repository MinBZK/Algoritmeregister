import {
  Organisation,
  OrganisationListResponse,
  CreateOrganisationResponse,
  UpdateOrganisationResponse,
  UpdateOptInResponse,
} from '@/types/organisation'
import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'

export async function getOrganisationList(): Promise<OrganisationListResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/organisation',
  }
  return backendRequest(request)
}

export async function createOrganisation(
  organisation: Organisation
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
  organisation: Organisation
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

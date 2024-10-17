import {
  OrganisationDetails,
  OrganisationDetailsResponse,
  UpdateOrganisationDetailsResponse,
} from '@/types/organisationDetails'
import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'

export async function getOrganisationDetails(
  orgCode: string
): Promise<OrganisationDetailsResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `/organisation-details/${orgCode}`,
  }
  return backendRequest(request)
}

export async function updateOrganisationDetails(
  org_code: string,
  organisationDetails: OrganisationDetails
): Promise<UpdateOrganisationDetailsResponse> {
  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `/organisation-details/${org_code}`,
    data: organisationDetails,
  }
  return backendRequest(request)
}

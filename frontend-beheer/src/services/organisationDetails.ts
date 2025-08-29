import {
  OrganisationDetails,
  OrganisationDetailsResponse,
  UpdateOrganisationDetailsResponse,
} from '@/types/organisationDetails'
import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'

export async function getOrganisationDetails(
  org_id: string
): Promise<OrganisationDetailsResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `/organisation-details/${org_id}`,
  }
  return backendRequest(request)
}

export async function updateOrganisationDetails(
  org_id: string,
  organisationDetails: OrganisationDetails
): Promise<UpdateOrganisationDetailsResponse> {
  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `/organisation-details/${org_id}`,
    data: organisationDetails,
  }
  return backendRequest(request)
}

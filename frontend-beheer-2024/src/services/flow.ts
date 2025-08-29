import { FlowResponse } from '@/types/flow'
import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'

export async function getFlowInstructions(
  org_id: string
): Promise<FlowResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `/organisation/${org_id}/flow`,
  }
  return backendRequest(request)
}

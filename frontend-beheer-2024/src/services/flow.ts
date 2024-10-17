import { FlowResponse } from '@/types/flow'
import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'

export async function getFlowInstructions(
  org_code: string
): Promise<FlowResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `/organisation/${org_code}/flow`,
  }
  return backendRequest(request)
}

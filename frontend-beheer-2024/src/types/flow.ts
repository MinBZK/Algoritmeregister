import { FastApiResponse } from '.'
import { User } from './user'

export interface FlowRole {
  key: string
  alias: string
  min_required: number
  members: User[]
}

export interface Flow {
  key: string
  alias: string
  roles: FlowRole[]
}

export interface FlowResponse extends FastApiResponse {
  data: Flow
}

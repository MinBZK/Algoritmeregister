import { FastApiResponse } from '.'
import { Organisation } from './organisation'

export interface UserCore {
  organisations: Organisation[]
  roles: string[]
  first_name: string
  last_name: string
}

export interface User extends UserCore {
  username: string
  id: string
}

export interface UserUpdate {
  groups?: string[]
  roles?: string[]
  first_name?: string
  last_name?: string
}

export interface UserNew extends UserUpdate {
  username: string
}

export interface GetUserResponse extends FastApiResponse {
  data: User
}

export interface GetUsersResponse extends FastApiResponse {
  data: {
    users: User[]
    count: number
  }
}

export interface CreateUserResponse extends FastApiResponse {
  data: User
}

export interface UpdateUserResponse extends FastApiResponse {
  data: User
}

export interface DeleteUserResponse extends FastApiResponse {
  data: null
}

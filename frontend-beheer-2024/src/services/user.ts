import {
  CreateUserResponse,
  UpdateUserResponse,
  GetUsersResponse,
  GetUserResponse,
  DeleteUserResponse,
  UserNew,
  UserUpdate,
} from '@/types/user'
import { AxiosRequestConfig } from 'axios'
import { backendRequest } from '.'

export interface getUserQuery {
  role?: string
  org?: string
  limit?: number
  skip?: number
  q?: string
}

export async function getMe(): Promise<GetUserResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/user/me',
  }
  return backendRequest(request)
}

export async function getUsers(
  query?: getUserQuery
): Promise<GetUsersResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: '/user',
    params: query,
  }
  return backendRequest(request)
}

export async function createUser(user: UserNew): Promise<CreateUserResponse> {
  const request: AxiosRequestConfig = {
    method: 'POST',
    url: '/user',
    data: user,
  }
  return backendRequest(request)
}

export async function getUser(user_id: string): Promise<GetUserResponse> {
  const request: AxiosRequestConfig = {
    method: 'GET',
    url: `/user/${user_id}`,
  }
  return backendRequest(request)
}

export async function updateUser(
  user_id: string,
  user: UserUpdate
): Promise<UpdateUserResponse> {
  const request: AxiosRequestConfig = {
    method: 'PUT',
    url: `/user/${user_id}`,
    data: user,
  }
  return backendRequest(request)
}

export async function deleteUser(user_id: string): Promise<DeleteUserResponse> {
  const request: AxiosRequestConfig = {
    method: 'DELETE',
    url: `/user/${user_id}`,
  }
  return backendRequest(request)
}

import { FastApiResponse } from '.'
import { AlgorithmForm } from './algorithm'

export interface AlgorithmDescription {
  name: string
  id: string
}

export interface Supplier {
  name: string
  algorithm_descriptions: AlgorithmDescription[]
}

export interface TemplateListResponse extends FastApiResponse {
  data: Supplier[]
}

export interface TemplateResponse extends FastApiResponse {
  data: AlgorithmForm
}

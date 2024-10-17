import { FastApiResponse } from '.'
import { Language } from './misc'

export interface BrokenLink {
  id: number
  name: string
  lars: string
  broken_links: [string, number][]
  language: Language
  create_dt: Date
  organisation: string
  batch: number
}

export interface BrokenLinkResponse extends FastApiResponse {
  data: BrokenLink[]
}

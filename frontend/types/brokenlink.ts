import type { Language } from '@/types/algoritme'

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

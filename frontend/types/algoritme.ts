export enum Language {
  NLD = 'NLD',
  ENG = 'ENG',
  FRY = 'FRY',
  PAP = 'PAP',
}

export interface Algoritme {
  algoritme_id: string
  name: string
  lars: string
  standard_version: string
  language: Language
  organization: string
  description_short: string
  code: string
  org_id: string

  [key: string]: null | string | string[]
}

export interface HighlightedAlgoritme {
  name: string
  lars: string
  organization: string
}

interface AlgorithmFieldDisplay {
  key: string
  value: string
  keyDescription: string
  keyLabel: string
}

export interface AlgorithmDisplay {
  key: string
  keyLabel: string
  properties: AlgorithmFieldDisplay[]
}

export type Suggestion = {
  lars: string
  organization: string
  name: string
}

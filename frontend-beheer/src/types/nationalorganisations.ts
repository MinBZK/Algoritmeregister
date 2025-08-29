import { FastApiResponse } from '.'

export interface NationalOrganisationsCount {
    name: string
    Total: number
    KD: number
    UTO: number
    BOO: number
    Overig: number
  }
  
  export interface NationalOrganisationsCountResponse extends FastApiResponse {
    data: NationalOrganisationsCount[]
  }
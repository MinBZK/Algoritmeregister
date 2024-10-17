import { FastApiResponse } from '.'

export enum OrgType {
  adviescollege = 'adviescollege',
  agentschap = 'agentschap',
  brandweer = 'brandweer',
  caribisch_openbaar_lichaam = 'caribisch_openbaar_lichaam',
  gemeente = 'gemeente',
  grensoverschrijdend_regionaal_samenwerkingsorgaan = 'grensoverschrijdend_regionaal_samenwerkingsorgaan',
  hoog_college_van_staat = 'hoog_college_van_staat',
  interdepartementale_commissie = 'interdepartementale_commissie',
  kabinet_van_de_koning = 'kabinet_van_de_koning',
  koepelorganisatie = 'koepelorganisatie',
  ministerie = 'ministerie',
  openbaar_lichaam_voor_beroep_en_bedrijf = 'openbaar_lichaam_voor_beroep_en_bedrijf',
  organisatie_met_overheidsbemoeienis = 'organisatie_met_overheidsbemoeienis',
  organisatieonderdeel = 'organisatieonderdeel',
  politie = 'politie',
  provincie = 'provincie',
  rechtspraak = 'rechtspraak',
  regionaal_samenwerkingsorgaan = 'regionaal_samenwerkingsorgaan',
  waterschap = 'waterschap',
  zelfstandig_bestuursorgaan = 'zelfstandig_bestuursorgaan',
  overig = 'overig',
}

export interface OrganisationUpdate {
  name: string
  code: string
  type: OrgType
  flow: string
}

export interface Organisation {
  id: number
  name: string
  code: string
  type: OrgType
  show_page: boolean
  flow: string
}

export interface OrganisationsResponse extends FastApiResponse {
  data: {
    organisations: Organisation[]
    count: number
  }
}

export interface CreateOrganisationResponse extends FastApiResponse {
  data: Organisation
}

export interface UpdateOrganisationResponse extends FastApiResponse {
  data: Organisation
}

export interface UpdateOptInResponse extends FastApiResponse {
  data: Organisation
}

export interface DeleteOrganisationResponse extends FastApiResponse {
  data: null
}

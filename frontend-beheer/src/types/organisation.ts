import { FastApiResponse } from '.'

export enum OrgType {
  adviescollege = 'Adviescollege',
  agentschap = 'Agentschap',
  brandweer = 'Brandweer',
  caribisch_openbaar_lichaam = 'Caribisch openbaar lichaam',
  gemeente = 'Gemeente',
  grensoverschrijdend_regionaal_samenwerkingsorgaan = 'Grensoverschrijdend regionaal samenwerkingsorgaan',
  hoog_college_van_staat = 'Hoog College van Staat',
  interdepartementale_commissie = 'Interdepartementale commissie',
  kabinet_van_de_koning = 'Kabinet van de Koning',
  koepelorganisatie = 'Koepelorganisatie',
  ministerie = 'Ministerie',
  openbaar_lichaam_voor_beroep_en_bedrijf = 'Openbaar lichaam voor beroep en bedrijf',
  organisatie_met_overheidsbemoeienis = 'Organisatie met overheidsbemoeienis',
  organisatieonderdeel = 'Organisatieonderdeel',
  politie = 'Politie',
  provincie = 'Provincie',
  rechtspraak = 'Rechtspraak',
  regionaal_samenwerkingsorgaan = 'Regionaal samenwerkingsorgaan',
  waterschap = 'Waterschap',
  zelfstandig_bestuursorgaan = 'Zelfstandig bestuursorgaan',
  overig = 'Overig',
}

export interface Organisation {
  name: string
  code: string
  type: OrgType | null
}

export interface OrganisationListResponse extends FastApiResponse {
  data: Organisation[]
}

export interface CreateOrganisationResponse extends FastApiResponse {
  data: null
}

export interface UpdateOrganisationResponse extends FastApiResponse {
  data: null
}

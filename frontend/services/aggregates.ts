export interface DocumentCount {
  name: string
  identifier: string
  number_of_algorithmdescriptions: number
  show_page: boolean
  joined: boolean
  code: string
  org_id: string
}

export interface DataObject {
  key: string
  count: number
  showPage: boolean
  joined: boolean
  code: string
  orgId: string
}

export interface GeoJson {
  type: string
  name?: string
  features: Array<{
    type: string
    id?: string
    properties: {
      id: number
      jrstatcode?: string
      rubriek?: string
      statcode?: string
      statnaam?: string
      geometry_g?: string
      waterschap?: string
      KVK?: number
      od_code?: string
      od_naam?: string
      naam_alt?: string
    }
    bbox?: number[]
    geometry: {
      type: string
      coordinates: number[][][][]
    }
  }>
  crs: {
    type: string
    properties: {
      name: string
    }
  }
  bbox?: number[]
  numberMatched?: number
  numberReturned?: number
  timeStamp?: string
  totalFeatures?: number
}

export interface ToolTipData {
  orgName: string
  algoCount: number
  orgPage: string
  orgPageUrl: string
  classificationColour: string | undefined
  orgCode: string
  joined: boolean
  algoKey: string
  algoPublished: string
  orgId: string
}

export const OrganisationTypes = {
  Province: 'province',
  Municipality: 'municipality',
  WaterAuthority: 'waterAuthority',
  EnvironmentalService: 'environmentalService',
  SafetyRegion: 'safetyRegion',
} as const

export interface DocumentCount {
  name: string
  identifier: string
  number_of_algorithmdescriptions: number
  show_page: boolean
  joined: boolean
}

export interface DataObject {
  key: string
  count: number
  showPage: boolean
  joined: boolean
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
      gag_id?: string | null
      hierarchie?: string | null
      hierarch_1?: string | null
      inspire_id?: string | null
      sde_id?: string | null
      land_code?: string | null
      inspire__1?: string | null
      inspire__2?: string | null
      wbh_code_o?: string | null
      einde_leve?: string | null
      laatste_wi?: string | null
      admin_code?: string | null
      waterschap?: string
      publiceren?: string
      Aangemeld?: number
      Actief?: number
      KVK?: number
      tnostatus?: number | null
      CPT?: number
      GMW?: number
      BHR?: number
      ASV?: number | null
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

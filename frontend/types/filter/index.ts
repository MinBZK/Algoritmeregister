export interface FilterData {
  label: string
  key: string
  count: number
}

export interface QueryBase {
  page?: string
  limit?: string
  searchtext?: string
}

export interface GenericQuery extends QueryBase {
  [key: string]: any
}

export interface GenericSelectedFilter {
  key: string
  value?: string
}

export interface FastApiResponse {
  status: number | null
  data: any

  [key: string]: any
}

export interface Organization {
  id: string
  name: string
}

export interface Breadcrumb {
  text: string;
  to: string;
}

export interface FastApiResponse {
  status: number | null
  data: any

  [key: string]: any
}

export interface Breadcrumb {
  title: string
  href: string
}

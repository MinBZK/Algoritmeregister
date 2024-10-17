export interface HtmlFiguresRecent {
  date: string
  html: string
  static: Record<string, any>
  static_data: Record<string, any>
}

export interface OrganisationTop20 {
  name: string
  count: number
}

export interface PublicationCategoriesCount {
  category: string
  count: number
}

export interface MonthlyCount {
  date: string
  count: number
}

export interface DashboardItem {
  show: boolean
  title: string
  count?: number
  description: string
  showTable: boolean
  graph?: string
  icon: string
}

export interface DashboardMap {
  show: boolean
  organisationType: string
  title: string
  count: number
  description: string
  clickOn: string
  icon: string
  geojsonFile: string
}

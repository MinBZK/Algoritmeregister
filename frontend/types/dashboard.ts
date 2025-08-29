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
  legendaDescription?: string
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

export interface NationalOrganisationsCount {
  name: string
  Total: number
  KD: number
  UTO: number
  BOO: number
  Overig: number
}

export interface NationalOrganisationsCountDashboard {
  name: string
  Total: number
  KD: number
  Agentschap: number
  Overig: number
}

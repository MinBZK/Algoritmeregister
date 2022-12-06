export type FooterPage = {
  path: string
  key: string
  label?: string
}

export type FooterColumn = {
  [key: string]: FooterPage[]
}

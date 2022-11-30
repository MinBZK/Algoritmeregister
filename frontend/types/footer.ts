export type FooterPage = {
  label: string
  path: string
}

export type FooterColumn = {
  key: string
  title: string
  pages: FooterPage[]
}

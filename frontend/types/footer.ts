export type FooterPage = {
  path: string
  key: string
  label?: string
}

export type FooterColumn = {
  [key: string]: FooterPage[]
}

export interface FooterFaqQuestion {
  key: string
  anchor: string
  question: string
  answer: string
}

export interface FooterFaqQuestionGroup {
  key: string
  label: string
  anchor: string
  questions: FooterFaqQuestion[]
}

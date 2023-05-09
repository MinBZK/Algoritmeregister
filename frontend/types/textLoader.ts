export type LanguageCode = 'nl' | 'en' | 'fy' | 'pap'
export interface SupportingTextField {
  html: string
  json?: Record<string, string>
}

export interface SupportingText {
  [key: string]: any
}

export interface apiStandardField {
  title: string
  maxLength?: string
  type: string
  example: string
  help_text: string
  show_always: boolean
  instructions: string
  allOf?: { $ref: string }[]
  allowed_html_tags?: string[]
}

export interface AlgorithmIn {
  [key: string]: apiStandardField
}

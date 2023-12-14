export interface FormFieldProperties {
  title: string
  maxLength?: number
  maxItems?: number
  type: string
  example?: string | string[]
  show_always: boolean
  help_text: string
  instructions: string
  rules?: ((v: any) => boolean | string)[]
  required: boolean
  allowedItems?: string[]
  recommendedItems?: string[]
  fixedValue?: string
  placeholder?: string
  allowedHtmlTags?: string[]
}

export interface FormProperties {
  [key: string]: FormFieldProperties
}

export interface ListWithLinks {
  title: string | null
  link: string | null
}

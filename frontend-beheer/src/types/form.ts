import { FastApiResponse } from '@/types/index'

export interface FormFieldProperties {
  title: string
  maxLength?: number
  type: string
  example: string
  showAlways: boolean
  helpText: string
  instructions: string
  rules?: ((v: any) => boolean | string)[]
  required: boolean
  allowedItems?: string[]
  recommendedItems?: string[]
  fixedValue?: string
  placeholder?: string
}

export interface FormProperties {
  [key: string]: FormFieldProperties
}

export interface SchemaProperties {
  title: string
  maxLength?: number
  type: string
  allOf: { $ref: string }[]
  items?: { $ref?: string; type?: string }
  example: string
  show_always: boolean
  help_text: string
  instructions: string
  recommended_items?: string[]
}

export interface OpenApiSchemas {
  [key: string]: any

  AlgorithmIn?: {
    [key: string]: any
    properties: {
      [key: string]: SchemaProperties
    }
    required?: string[]
  }
}

export interface MetaDataResponse extends FastApiResponse {
  data: {
    [key: string]: any
    components: {
      [key: string]: any
      schemas: OpenApiSchemas
    }
  }
}

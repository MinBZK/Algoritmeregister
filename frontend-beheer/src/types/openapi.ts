import { FastApiResponse } from '@/types/index'

export type OpenApiSchema =
  | ObjectSchema
  | StringSchema
  | EnumReferenceSchema
  | ArraySchema
  | ArrayOptionalSchema
  | BooleanSchema
  | EnumSchema

export interface AlgorithmInSchema {
  title: string
  required: string[]
  type: 'object'
  properties: {
    [key: string]:
      | ObjectSchema
      | StringSchema
      | EnumReferenceSchema
      | ArraySchema
      | ArrayOptionalSchema
  }
}

export interface BaseOpenApiSchema {
  title: string
  example: string | string[]
  show_always: boolean
  help_text: string
  instructions: string
}

export interface ObjectSchema extends BaseOpenApiSchema {
  type: 'object'
  required?: string[]
  properties: {
    [key: string]: OpenApiSchema
  }
}

export interface StringSchema extends BaseOpenApiSchema {
  type: 'string'
  max_length_without_html: number
  allowed_html_tags?: string[]
}

export interface ArraySchema extends BaseOpenApiSchema {
  type: 'array'
  maxItems?: number
  items: {
    $ref: string
  }
}

export interface ArrayOptionalSchema extends BaseOpenApiSchema {
  type: 'array'
  items: {
    type: string
  }
  recommended_items: string[]
}

export interface EnumReferenceSchema extends BaseOpenApiSchema {
  type: 'enum'
  allOf: {
    $ref: string
  }[]
}

export interface BooleanSchema {
  type: 'boolean'
  title: string
}

export interface EnumSchema {
  type: 'string'
  title: string
  enum: string[]
  description: string
}

export interface MetaDataResponse extends FastApiResponse {
  data: {
    [key: string]: any
    components: {
      [key: string]: any
      schemas: {
        [key: string]: OpenApiSchema
      }
    }
  }
}

// Store for managing the algorithms that the user has access to.
import { getMetaDataStandard } from '@/services'
import type {
  OpenApiSchema,
  EnumSchema,
  ArraySchema,
  AlgorithmInSchema,
  ObjectSchema,
} from '@/types/openapi'
import { FormFieldProperties, FormProperties } from '@/types/form'
import { defineStore } from 'pinia'
import content from '@/content.json'
import { buildRulesFromProperties } from '@/utils/form'
import { useAuthStore } from './auth'
import { useFormDataStore } from './form-data'

const authStore = useAuthStore()

export const useSchemaStore = defineStore('schema', {
  state: () => ({
    rawSchemas: {} as { [key: string]: OpenApiSchema },
    loadedSchema: '' as string,
    loaded: true as boolean,
    feedback: { success: '', error: '' },
  }),
  getters: {
    formProperties(self): FormProperties {
      if (!self.rawSchemas.AlgorithmIn) return {}
      if (authStore.organisations.length == 0) return {}
      const dataStore = useFormDataStore()

      const mainSchema = self.rawSchemas.AlgorithmIn as AlgorithmInSchema
      const hiddenFields = ['publication_dt', 'lars']
      const formProperties = Object.fromEntries(
        Object.entries(mainSchema.properties).flatMap(([key, v]) => {
          if (hiddenFields.includes(key)) return []
          // Build properties per field based on values in AlgorithmIn schema.
          const required = mainSchema.required.includes(key)
          const formFieldProperties: FormFieldProperties = {
            ...v,
            required,
          }
          let allowedItems
          if (v.type == 'enum' && v.$ref) {
            // EnumReferenceSchema, single select enumeration
            const schema = v.$ref.split('/').slice(-1)[0]!
            allowedItems = (self.rawSchemas[schema] as EnumSchema).enum
            formFieldProperties['type'] = 'select'
          }
          if (v.type == 'enum' && v.anyOf) {
            // EnumStandardVersion
            const schema = v.anyOf[0]?.$ref.split('/').slice(-1)[0]!
            allowedItems = (self.rawSchemas[schema] as EnumSchema).enum
          } else if (v.type == 'string') {
            // StringSchema
            formFieldProperties['maxLength'] = v.max_length_without_html
            if (v.allowed_html_tags) {
              formFieldProperties['allowedHtmlTags'] = v.allowed_html_tags
              formFieldProperties['type'] = 'rich-textarea'
            } else {
              formFieldProperties['type'] = 'textarea'
            }
          } else if (v.type == 'array') {
            // ArraySchema or ObjectSchema
            const schema = v.anyOf[0]?.items.$ref.split('/').slice(-1)[0]!
            if (v.anyOf[0]?.items.$ref.includes('Enum', 27)) {
              // ArraySchema, multi-select enumeration
              allowedItems = (self.rawSchemas[schema] as EnumSchema).enum
              formFieldProperties['type'] = 'multi-select'
              formFieldProperties['maxItems'] = (v as ArraySchema).maxItems
            } else if (v.anyOf[0]?.items.$ref.includes('Object', 27)) {
              // ObjectSchema. Only works for 1.0
              const schemaData = self.rawSchemas[schema] as ObjectSchema
              const titleProperty = schemaData.properties?.title
              const recommendedItems =
                titleProperty && 'recommended_items' in titleProperty
                  ? titleProperty.recommended_items
                  : undefined
              formFieldProperties['recommendedItems'] = recommendedItems
              formFieldProperties['type'] = 'list-with-links'
            }
            // } else if (v.type == 'array' && v.items && 'type' in v.items) {
            //   // ArrayOptionalSchema, multi-select with recommended items
            //   const recommendedItems = (v as ArrayOptionalSchema)
            //     .recommended_items
            //   formFieldProperties['recommendedItems'] = recommendedItems
            //   formFieldProperties['type'] = 'optional-select'
          }
          if (key == 'organization') {
            const organisations = authStore.organisations
            // Matching the organisation with selectedOrg fixes the value.
            if (dataStore.data.organization === authStore.selectedOrg?.name) {
              formFieldProperties['fixedValue'] = dataStore.data.organization
              formFieldProperties['type'] = 'fixed'
            } else {
              allowedItems = organisations.map((org) => org.name)
              formFieldProperties['type'] = 'select'
            }
          } else if (key == 'name') {
            formFieldProperties['type'] = 'name-textarea'
          }

          if (allowedItems) {
            if (allowedItems.length == 1) {
              formFieldProperties['type'] = 'fixed'
              formFieldProperties['fixedValue'] = allowedItems[0]
              delete formFieldProperties.allowedItems
              dataStore.data[key] = formFieldProperties['fixedValue']
            } else {
              formFieldProperties['allowedItems'] = allowedItems
            }
          }

          formFieldProperties['rules'] =
            buildRulesFromProperties(formFieldProperties)

          return [[key, formFieldProperties]]
        })
      )
      return formProperties
    },
  },
  actions: {
    async fetchSchema(version: string): Promise<void> {
      this.loaded = false
      this.rawSchemas = {}
      this.loadedSchema = ''
      try {
        const data = (await getMetaDataStandard(version)).data
        this.rawSchemas = data.components.schemas
        this.loadedSchema = version
      } catch (error) {
        console.error(error)
        this.feedback.error = content.formGenerator.fetchMetadata.error
      } finally {
        this.loaded = true
      }
    },
  },
})

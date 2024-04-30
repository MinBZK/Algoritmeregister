// Store for managing the algorithms that the user has access to.
import { getMetaDataStandard } from '@/services'
import { getC3poRules } from '@/services/c3po'
import type {
  OpenApiSchema,
  EnumSchema,
  ArraySchema,
  ArrayOptionalSchema,
  AlgorithmInSchema,
} from '@/types/openapi'
import { FormFieldProperties, FormProperties } from '@/types/form'
import { RuleSet } from '@/types/c3po'
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
    ruleSets: [] as RuleSet[],
  }),
  getters: {
    formProperties(self): FormProperties {
      if (!self.rawSchemas.AlgorithmIn) return {}
      if (authStore.organisations.length == 0) return {}
      const dataStore = useFormDataStore()

      const mainSchema = self.rawSchemas.AlgorithmIn as AlgorithmInSchema
      const formProperties = Object.fromEntries(
        Object.entries(mainSchema.properties).map(([key, v]) => {
          // Build properties per field based on values in AlgorithmIn schema.
          const required = mainSchema.required.includes(key)
          const formFieldProperties: FormFieldProperties = {
            ...v,
            required,
          }

          let allowedItems
          if (v.type == 'enum') {
            // EnumReferenceSchema, single select enumeration
            const schema = v.allOf[0]!.$ref.split('/').slice(-1)[0]!
            allowedItems = (self.rawSchemas[schema] as EnumSchema).enum
            formFieldProperties['type'] = 'select'
          } else if (v.type == 'string') {
            // StringSchema
            formFieldProperties['maxLength'] = v.max_length_without_html
            if (v.allowed_html_tags) {
              formFieldProperties['allowedHtmlTags'] = v.allowed_html_tags
              formFieldProperties['type'] = 'rich-textarea'
            } else {
              formFieldProperties['type'] = 'textarea'
            }
          } else if (v.type == 'array' && '$ref' in v.items) {
            // ArraySchema or ObjectSchema
            const schema = v.items.$ref.split('/').slice(-1)[0]!
            if (v.items.$ref.includes('Enum', 29)) {
              // ArraySchema, multi-select enumeration
              allowedItems = (self.rawSchemas[schema] as EnumSchema).enum
              formFieldProperties['type'] = 'multi-select'
              formFieldProperties['maxItems'] = (v as ArraySchema).maxItems
            } else if (v.items.$ref.includes('Object', 29)) {
              // ObjectSchema. Only works for 1.0.0
              formFieldProperties['type'] = 'list-with-links'
            }
          } else if (v.type == 'array' && 'type' in v.items) {
            // ArrayOptionalSchema, multi-select with recommended items
            const recommendedItems = (v as ArrayOptionalSchema)
              .recommended_items
            formFieldProperties['recommendedItems'] = recommendedItems
            formFieldProperties['type'] = 'optional-select'
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

          return [key, formFieldProperties]
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

      if (authStore.canPublish) {
        try {
          const ruleData = (await getC3poRules()).data
          this.ruleSets = ruleData
        } catch (error) {
          console.error(error)
        }
      }
    },
  },
})

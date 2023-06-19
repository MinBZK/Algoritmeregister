// Store for managing the algorithms that the user has access to.
import { getMetaDataStandard } from '@/services'
import {
  FormFieldProperties,
  FormProperties,
  OpenApiSchemas,
} from '@/types/form'
import { defineStore } from 'pinia'
import content from '@/content.json'
import {
  buildRulesFromProperties,
  buildPlaceholderFromSchema,
} from '@/util/form'
import { useAuthStore } from './auth'
import { useFormDataStore } from './form-data'

const authStore = useAuthStore()

export const useSchemaStore = defineStore('schema', {
  state: () => ({
    rawSchemas: {} as OpenApiSchemas,
    loadedSchema: '' as string,
    loaded: true as boolean,
    feedback: { success: '', error: '' },
  }),
  getters: {
    formProperties(self): FormProperties {
      if (self.rawSchemas.AlgorithmIn) {
        const schemaEntries = Object.entries(
          self.rawSchemas.AlgorithmIn.properties
        )
        const formProperties = Object.fromEntries(
          schemaEntries.map(([k, v]) => {
            let allowedItems: string[] | undefined = undefined
            let recommendedItems: string[] | undefined = undefined
            let type: string | undefined = undefined
            if (v.type == 'enum' && v.allOf) {
              // The enumerations are in their own schema, on the same depth as the main schema.
              // The $ref is a path string, but only the final bit is needed.
              const schema: string | undefined = v.allOf[0]?.$ref
                .split('/')
                .slice(-1)[0]
              if (schema) {
                allowedItems = self.rawSchemas[schema].enum
              }
            } else if (v.type == 'array' && v.items?.$ref) {
              const schema: string | undefined = v.items?.$ref
                .split('/')
                .slice(-1)[0]
              if (schema) {
                allowedItems = self.rawSchemas[schema].enum
              }
            } else if (
              v.type == 'array' &&
              v.items?.type == 'string' &&
              v.recommended_items
            ) {
              recommendedItems = v.recommended_items
            }

            const dataStore = useFormDataStore()
            let fixedValue: string | undefined = undefined
            if (k == 'organization') {
              const organizations = authStore.organizations
              // absence of ...data.lars means organization can still be chosen.
              if (!dataStore.data.lars) {
                if (organizations.length > 1) {
                  allowedItems = organizations.map((org) => org.name)
                  type = 'enum'
                } else if (organizations.length == 1) {
                  fixedValue = organizations[0]!.name
                  dataStore.data.organization = fixedValue
                  type = 'fixed'
                }
              } else {
                if (
                  dataStore.data.organization === authStore.selectedOrg?.name
                ) {
                  fixedValue = dataStore.data.organization
                  type = 'fixed'
                } else {
                  allowedItems = organizations.map((org) => org.name)
                  type = 'enum'
                }
              }
            } else if (k == 'standard_version') {
              // Standard_version cannot be adjusted.
              type = 'fixed'
              fixedValue = allowedItems![0]
            }

            const required: boolean =
              self.rawSchemas.AlgorithmIn?.required?.includes(k) || false

            const placeholder: string = buildPlaceholderFromSchema(v)

            let formFieldProperties: FormFieldProperties = {
              title: v.title,
              maxLength: v.maxLength,
              type: type || v.type,
              example: v.example,
              showAlways: v.show_always,
              helpText: v.help_text,
              instructions: v.instructions,
              required,
              allowedItems,
              recommendedItems,
              fixedValue,
              placeholder,
            }

            const rules = buildRulesFromProperties(formFieldProperties)

            formFieldProperties = { ...formFieldProperties, rules: rules }

            return [k, formFieldProperties]
          })
        )
        return formProperties
      } else {
        return {}
      }
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

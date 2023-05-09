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
    loaded: false as boolean,
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
            let allowedValues = undefined
            if (v.allOf) {
              // The enumerations are in their own schema, on the same depth as the main schema.
              // The $ref is a path string, but only the final bit is needed.
              const schema: string | undefined = v.allOf[0]?.$ref
                .split('/')
                .slice(-1)[0]
              if (schema) {
                allowedValues = self.rawSchemas[schema].enum
              }
            }

            const dataStore = useFormDataStore()
            let fixedValue: string | undefined = undefined
            if (k == 'organization') {
              const organizations = authStore.organizations
              if (!dataStore.data.lars) {
                if (organizations.length > 1) {
                  allowedValues = organizations.map((org) => org.name)
                  v.type = 'enum'
                } else if (organizations.length == 1) {
                  fixedValue = organizations[0]!.name
                  dataStore.data.organization = fixedValue
                  v.type = 'fixed'
                }
              } else {
                v.type = 'fixed'
                if (
                  organizations.includes(
                    dataStore.orgFromData || { id: '', name: '' }
                  )
                ) {
                  fixedValue = dataStore.data.organization
                } else {
                  fixedValue = authStore.selectedOrg.name
                  dataStore.data.organization = fixedValue
                }
              }
            } else if (k == 'standard_version') {
              // Standard_version cannot be adjusted.
              v.type = 'fixed'
              fixedValue = allowedValues[0]
            }

            const required: boolean =
              self.rawSchemas.AlgorithmIn?.required?.includes(k) || false

            const placeholder: string = buildPlaceholderFromSchema(v)

            let formFieldProperties: FormFieldProperties = {
              title: v.title,
              maxLength: v.maxLength,
              type: v.type,
              example: v.example,
              showAlways: v.show_always,
              helpText: v.help_text,
              instructions: v.instructions,
              required,
              allowedValues,
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
      await getMetaDataStandard(version)
        .then((response) => {
          this.rawSchemas = response.data.components.schemas
          this.loaded = true
          this.loadedSchema = version
        })
        .catch((error) => {
          console.error(error.data)
          this.feedback.error = content.formGenerator.fetchMetadata.error
          this.rawSchemas = {}
          this.loaded = true
          this.loadedSchema = ''
        })
    },
  },
})

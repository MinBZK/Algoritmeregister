// Store for managing the algorithms that the user has access to.
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import { useSchemaStore } from './schema'
import {
  getAlgorithm,
  updateAlgorithm,
  createAlgorithm,
  retractAlgorithm,
  publishAlgorithm,
  releaseAlgorithm,
  generatePreview,
  removeAlgorithm,
} from '@/services'
import {
  AlgorithmForm,
  CreateAlgorithmResponse,
  RemoveAlgorithmResponse,
  UpdateAlgorithmResponse,
  NoOrgResponse,
} from '@/types/algorithm'
import content from '@/content.json'
import { Organization } from '@/types'
import { noOrgSelectedResponse } from '@/util'
import router from '@/router'

const authStore = useAuthStore()

export const useFormDataStore = defineStore('form-data', {
  state: () => ({
    schemaStore: useSchemaStore(),
    data: {} as AlgorithmForm,
    loaded: true,
    feedback: { success: '', error: '', errorList: [] },
    previewLoading: false,
    unsavedChanges: false,
  }),
  getters: {
    cleanedData(): AlgorithmForm {
      return Object.fromEntries(
        Object.entries(this.data).filter(([, v]) => {
          if (Array.isArray(v) && v.length == 0) return false
          if (v === '') return false
          return true
        })
      )
    },
    orgFromData(): Organization | undefined {
      return authStore.organizations.find(
        (org) => org.name == this.data.organization
      )
    },
  },
  actions: {
    async fetchData(lars: string): Promise<void> {
      // We do not know which organisation the algorithm belongs to.
      this.data = {}
      this.loaded = false
      // A good try is to use the current selected org (= sometimes based on localStorage)
      try {
        this.data = (await getAlgorithm(authStore.selectedOrg!, lars)).data
      } catch (error) {
        // Loop through all of them.
        for (let i = 0; i < authStore.organizations.length; i++) {
          try {
            this.data = (
              await getAlgorithm(authStore.organizations[i]!, lars)
            ).data
            break
          } catch (error) {
            continue
          }
        }
      }
      this.loaded = true
      if (Object.keys(this.data).length == 0) {
        // Data not available, push to home
        router.push({ name: 'algorithm.index' })
        return
      }
      // No duplicate loading if the schema in local cache is already good.
      if (this.schemaStore.loadedSchema !== this.data.standard_version) {
        this.schemaStore.fetchSchema(this.data.standard_version)
      }
    },
    resetFeedback(): void {
      this.feedback = { success: '', error: '', errorList: [] }
    },
    async handleUpdate(
      lars: string
    ): Promise<UpdateAlgorithmResponse | NoOrgResponse> {
      if (!this.orgFromData) return noOrgSelectedResponse()
      return await updateAlgorithm(this.orgFromData, lars, this.cleanedData)
        .then((response) => {
          if (response.data?.message != 'Version has no changes.') {
            this.data.released = false
            this.data.published = false
            this.unsavedChanges = false
          }
          this.feedback.success = content.formDataStore.update.success
          return response
        })
        .catch((response) => {
          if (response.status == 422) {
            this.feedback.errorList = response.data.map(
              (error: any) =>
                this.schemaStore.formProperties[error.loc[1]]!.title
            )
          }
          this.feedback.error = content.formDataStore.update.error
          return response
        })
    },
    async handleCreate(): Promise<CreateAlgorithmResponse | NoOrgResponse> {
      if (!this.orgFromData) return noOrgSelectedResponse()
      return await createAlgorithm(this.orgFromData, this.cleanedData)
        .then((response) => {
          this.data.lars = response.data.lars_code
          this.unsavedChanges = false
          // Change organization based on the saved algorithm. Needed for loading from cookies
          authStore.selectOrganization(this.orgFromData!.id)
          this.feedback.success = content.formDataStore.create.success
          return response
        })
        .catch((response) => {
          if (response.status == 422) {
            this.feedback.errorList = response.data.map(
              (error: any) =>
                this.schemaStore.formProperties[error.loc[1]]!.title
            )
          }
          this.feedback.error = content.formDataStore.create.error
          return response
        })
    },
    async handleRetract(lars: string): Promise<void | NoOrgResponse> {
      if (!this.orgFromData) return noOrgSelectedResponse()
      await retractAlgorithm(this.orgFromData, lars)
        .then(() => {
          this.data.published = false
          this.data.released = false
          this.feedback.success = content.formDataStore.retract.success
        })
        .catch(() => {
          this.feedback.error = content.formDataStore.retract.error
        })
    },
    async handlePublish(lars: string): Promise<void | NoOrgResponse> {
      if (!this.orgFromData) return noOrgSelectedResponse()
      await publishAlgorithm(this.orgFromData, lars)
        .then(() => {
          this.data.published = true
          this.feedback.success = content.formDataStore.publish.success
        })
        .catch(() => {
          this.feedback.error = content.formDataStore.publish.error
        })
    },
    async handleRelease(lars: string): Promise<void | NoOrgResponse> {
      if (!this.orgFromData) return noOrgSelectedResponse()
      await releaseAlgorithm(this.orgFromData, lars)
        .then(() => {
          this.data.released = true
          this.feedback.success = content.formDataStore.release.success
        })
        .catch((response) => {
          if (response.status == 409) {
            this.feedback.error =
              content.formDataStore.release.noReleaseOnPublished
          } else {
            this.feedback.error = content.formDataStore.release.error
          }
        })
    },
    async handleRemove(
      lars: string
    ): Promise<RemoveAlgorithmResponse | NoOrgResponse> {
      if (!this.orgFromData) return noOrgSelectedResponse()
      return await removeAlgorithm(this.orgFromData, lars)
        .then((response) => {
          this.unsavedChanges = false
          this.feedback.success = content.formDataStore.remove.success
          return response
        })
        .catch((response) => {
          this.feedback.error = content.formDataStore.remove.error
          return response
        })
    },
    async handlePreview(lars: string): Promise<void | NoOrgResponse> {
      if (!this.orgFromData) return noOrgSelectedResponse()
      this.previewLoading = true
      generatePreview(this.orgFromData, lars)
        .then((response) => {
          // open response.url in new tab
          window.open(response.data.url, '_blank')
        })
        .catch(() => {
          this.feedback.error = content.formDataStore.preview.error
        })
        .finally(() => {
          this.previewLoading = false
        })
    },
    pruneData(): void {
      // Removes all data keys that do not appear in the current schema
      const formProperties = this.schemaStore.formProperties
      Object.keys(this.data).forEach((element) => {
        if (!(element in formProperties) && element != 'lars') {
          delete this.data[element]
        }
      })
    },
  },
})

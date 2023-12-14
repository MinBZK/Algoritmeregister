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
  getAlgorithmOwner,
} from '@/services/algorithms'
import {
  AlgorithmForm,
  CreateAlgorithmResponse,
  RemoveAlgorithmResponse,
  UpdateAlgorithmResponse,
  NoOrgResponse,
} from '@/types/algorithm'
import content from '@/content.json'
import { Organisation } from '@/types/organisation'
import { noOrgSelectedResponse } from '@/utils'
import router from '@/router'
import { useAlgorithmStore } from './overview'

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
    orgFromData(): Organisation | undefined {
      return authStore.organisations.find(
        (org) => org.name == this.data.organization
      )
    },
  },
  actions: {
    async fetchData(lars: string): Promise<void> {
      // We do not know which organisation the algorithm belongs to.
      this.data = {}
      this.loaded = false
      // Ask backend where to find the algoritmebeschrijving
      const algorithmStore = useAlgorithmStore()
      try {
        const owner = (await getAlgorithmOwner(lars)).data
        this.data = (await getAlgorithm(owner, lars)).data
        algorithmStore.error = ''
      } catch (error) {
        console.log(error)
        router.push({ name: 'algorithm.index' })

        // algorithmStore displays its errors on the algorithm.index page
        algorithmStore.error =
          'Algoritme niet gevonden. U bent teruggestuurd naar uw homepagina.'
        return
      } finally {
        this.loaded = true
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
          if (response.data?.message != 'NO_CHANGES') {
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
          // Change organisation based on the saved algorithm. Needed for loading from cookies
          authStore.selectOrganisation(this.orgFromData!.code)
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
    handleSchemaSwap(oldVersion: string, newVersion: string): void {
      // Certain migrations need additional attention to detail
      const dataStore = useFormDataStore()
      if (oldVersion == '0.4.0' && newVersion == '1.0.0') {
        dataStore.data.impacttoetsen = null
      }
    },
  },
})

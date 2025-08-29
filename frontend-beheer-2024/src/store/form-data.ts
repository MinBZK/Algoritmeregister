// Store for managing the algorithms that the user has access to.
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import { useSchemaStore } from './schema'
import {
  getAlgorithm,
  updateAlgorithm,
  createAlgorithm,
  generatePreview,
  removeAlgorithm,
  getAlgorithmOwner,
  getAvailableActions,
  updateAlgorithmState,
} from '@/services/algorithms'
import {
  AlgorithmForm,
  CreateAlgorithmResponse,
  RemoveAlgorithmResponse,
  UpdateAlgorithmResponse,
  NoOrgResponse,
  StateChangeAction,
} from '@/types/algorithm'
import { notifications } from '@/config/notifications'
import { Organisation } from '@/types/organisation'
import { noOrgSelectedResponse, unknownError } from '@/utils'
import router from '@/router'
import { useSnackbarStore } from './snackbar'

export const useFormDataStore = defineStore('form-data', {
  state: () => ({
    authStore: useAuthStore(),
    schemaStore: useSchemaStore(),
    snackbarStore: useSnackbarStore(),
    data: {} as AlgorithmForm,
    availableActions: [] as StateChangeAction[],
    loaded: true,
    saving: false,
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
      return this.authStore.organisations.find(
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
      await getAlgorithmOwner(lars)
        .then(async (response) => {
          await getAlgorithm(response.data, lars)
            .then((response) => {
              this.data = response.data
            })
            .catch((error) => {
              if (error.status == 403) {
                this.snackbarStore.add(notifications.noAccessRights!)
              } else {
                this.snackbarStore.add(notifications.unknownError!)
              }
              router.push({ name: 'algorithm.index' })
            })
        })
        .catch((error) => {
          if (error.status == 404) {
            this.snackbarStore.add(notifications.cannotFindAlgorithmError!)
          } else {
            this.snackbarStore.add(notifications.unknownError!)
          }
          router.push({ name: 'algorithm.index' })
        })

      this.loaded = true
      // No duplicate loading if the schema in local cache is already good.
      if (this.schemaStore.loadedSchema !== this.data.standard_version) {
        this.schemaStore.fetchSchema(this.data.standard_version)
      }
    },
    async fetchAvailableActions(lars: string) {
      if (!this.orgFromData) return noOrgSelectedResponse()
      await getAvailableActions(this.orgFromData.org_id, lars).then(
        (response) => {
          this.availableActions = response.data
        }
      )
    },
    async handleUpdate(
      lars: string
    ): Promise<UpdateAlgorithmResponse | NoOrgResponse> {
      if (!this.orgFromData) return noOrgSelectedResponse()
      this.saving = true
      return await updateAlgorithm(this.orgFromData, lars, this.cleanedData)
        .then(async (response) => {
          // check c3po changes
          if (response.data?.message != 'NO_CHANGES') {
            this.unsavedChanges = false
            this.data.state = 'STATE_1'
            await this.fetchAvailableActions(lars).catch(() => unknownError())
            this.snackbarStore.add(notifications.updateSuccess!)
          } else {
            this.snackbarStore.add(notifications.updateNoChanges!)
            this.unsavedChanges = false
          }
          return response
        })
        .catch((response) => {
          if (response.status == 422) {
            const errorList = response.data.map(
              (error: any) =>
                this.schemaStore.formProperties[error.loc[1]]!.title
            )
            this.snackbarStore.add({
              ...notifications.updateValidationError!,
              list: errorList,
            })
          } else {
            this.snackbarStore.add(notifications.updateGenericError!)
          }
          return response
        })
        .finally(() => {
          this.saving = false
        })
    },
    async handleCreate(): Promise<CreateAlgorithmResponse | NoOrgResponse> {
      if (!this.orgFromData) return noOrgSelectedResponse()
      this.saving = true
      return await createAlgorithm(this.orgFromData, this.cleanedData)
        .then(async (response) => {
          this.data.lars = response.data.lars_code
          this.unsavedChanges = false
          this.data.state = 'STATE_1'
          await this.fetchAvailableActions(response.data.lars_code).catch(() =>
            unknownError()
          )
          // Change organisation based on the saved algorithm. Needed for loading from cookies
          this.authStore.selectOrganisation(this.orgFromData!.org_id)
          this.snackbarStore.add(notifications.createSuccess!)
          return response
        })
        .catch((response) => {
          if (response.status === 422) {
            const errorList = response.data.map(
              (error: any) =>
                this.schemaStore.formProperties[error.loc[1]]!.title
            )
            this.snackbarStore.add({
              ...notifications.createValidationError!,
              list: errorList,
            })
          } else {
            this.snackbarStore.add(notifications.createGenericError!)
          }
          return response
        })
        .finally(() => {
          this.saving = false
        })
    },
    async handleStateChange(lars: string, action: StateChangeAction) {
      if (!this.orgFromData) return noOrgSelectedResponse()
      await updateAlgorithmState(this.orgFromData.org_id, lars, action)
        .then(async () => {
          await this.fetchAvailableActions(lars).catch(() => unknownError())
          this.data.state = action.target_state
        })
        .catch(() => unknownError())
    },
    async handleRemove(
      lars: string
    ): Promise<RemoveAlgorithmResponse | NoOrgResponse> {
      if (!this.orgFromData) return noOrgSelectedResponse()
      return await removeAlgorithm(this.orgFromData, lars)
        .then((response) => {
          this.unsavedChanges = false
          this.snackbarStore.add(notifications.removeSuccess!)
          return response
        })
        .catch((response) => {
          this.snackbarStore.add(notifications.removeError!)
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
          this.snackbarStore.add(notifications.previewError!)
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
      if (oldVersion == '0.4' && newVersion == '1.0') {
        dataStore.data.impacttoetsen = null
      }
    },
  },
})

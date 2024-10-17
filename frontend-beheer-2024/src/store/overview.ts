// Store for managing the algorithms that the user has access to.
import { defineStore } from 'pinia'
import { Algorithm } from '@/types/algorithm'
import { getAlgorithmList } from '@/services/algorithms'
import { notifications } from '@/config/notifications'
import { Organisation } from '@/types/organisation'
import { useAuthStore } from './auth'
import { useSnackbarStore } from './snackbar'
import { formatDateTime } from '@/utils/datetime'

export const useAlgorithmStore = defineStore('algorithm', {
  state: () => ({
    snackbarStore: useSnackbarStore(),
    algorithms: [] as Algorithm[],
    loaded: true as boolean,
    authStore: useAuthStore(),
  }),
  getters: {
    algorithmsFormatted(): Algorithm[] {
      return this.algorithms.map((algorithm) => {
        algorithm.last_update_dt_formatted = formatDateTime(algorithm.last_update_dt)
        return algorithm
      })
    },
  },
  actions: {
    async fetchAlgorithms(organisation: Organisation): Promise<void> {
      this.algorithms = []

      // User has no organisations, exit
      if (this.authStore.organisations.length == 0) {
        return
      }

      this.loaded = false
      let algorithms = []
      try {
        algorithms = (await getAlgorithmList(organisation)).data
      } catch (error: any) {
        console.error(error.data)
        this.snackbarStore.add(notifications.fetchOverviewError!)
        this.loaded = true
        return
      }

      this.algorithms = algorithms.map((a) => {
        let overviewStatus
        if (a.current_version_published) {
          overviewStatus = 'Gepubliceerd'
        } else if (a.current_version_released && !a.published) {
          overviewStatus = 'Vrijgegeven'
        } else if (a.published && a.current_version_released) {
          overviewStatus = 'Gepubliceerd, nieuwe versie vrijgegeven'
        } else if (a.published) {
          overviewStatus = 'Gepubliceerd, nieuwe versie wordt nog bewerkt'
        } else {
          overviewStatus = 'Wordt nog bewerkt'
        }
        return { ...a, overviewStatus: overviewStatus }
      })
      this.loaded = true
    },
  },
})

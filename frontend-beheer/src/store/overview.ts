// Store for managing the algorithms that the user has access to.
import { defineStore } from 'pinia'
import { Algorithm } from '@/types/algorithm'
import { getAlgorithmList } from '@/services'
import content from '@/content.json'
import { Organization } from '@/types'
import { useAuthStore } from './auth'

export const useAlgorithmStore = defineStore('algorithm', {
  state: () => ({
    algorithms: [] as Algorithm[],
    loaded: true as boolean,
    error: '',
    success: '',
  }),
  getters: {
    algorithmsFormatted(): Algorithm[] {
      const algorithmsSorted = this.algorithms.sort(
        (a, b) =>
          new Date(b.last_update_dt).getTime() -
          new Date(a.last_update_dt).getTime()
      )
      return algorithmsSorted.map((algorithm) => {
        const date = new Date(algorithm.last_update_dt)
          .toLocaleDateString()
          .replaceAll('/', '-')
        const time = new Date(algorithm.last_update_dt).toLocaleTimeString()
        algorithm.last_update_dt = `${date} ${time}`
        return algorithm
      })
    },
  },
  actions: {
    async fetchAlgorithms(organization: Organization): Promise<void> {
      this.algorithms = []

      const authStore = useAuthStore()
      // User has no organizations, exit
      if (authStore.organizations.length == 0) {
        return
      }

      this.loaded = false
      try {
        this.algorithms = (await getAlgorithmList(organization)).data
      } catch (error: any) {
        console.error(error.data)
        this.error = content.overviewTable.fetchAlgoritms.error
        this.loaded = true
        return
      }

      this.algorithms = this.algorithms.map((a) => {
        let overviewStatus
        if (a.current_version_published) {
          overviewStatus = 'Gepubliceerd'
        } else if (a.current_version_released && !a.published) {
          overviewStatus = 'Vrijgegeven'
        } else if (a.published && a.current_version_released) {
          overviewStatus = 'Gepubliceerd, nieuwe versie vrijgegeven'
        } else if (a.published) {
          overviewStatus = 'Gepubliceerd, nieuwe versie in ontwikkeling'
        } else {
          overviewStatus = 'In ontwikkeling'
        }
        return { ...a, overviewStatus: overviewStatus }
      })
      this.loaded = true
    },
  },
})

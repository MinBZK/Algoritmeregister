// Store for managing the algorithms that the user has access to.
import { defineStore } from 'pinia'
import { Algorithm } from '@/types/algorithm'
import { getAlgorithmList } from '@/services'
import content from '@/content.json'
import { Organization } from '@/types'

export const useAlgorithmStore = defineStore('algorithm', {
  state: () => ({
    algorithms: [] as Algorithm[],
    loaded: false as boolean,
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
    fetchAlgorithms(organization: Organization): void {
      if (Object.keys(organization).length !== 0) {
        this.loaded = false
        this.algorithms = []
        getAlgorithmList(organization)
          .then((response) => {
            this.algorithms = response.data.map((a) => {
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
          })
          .catch((error) => {
            console.error(error.data)
            this.error = content.overviewTable.fetchAlgoritms.error
            this.loaded = true
          })
      } else {
        this.loaded = true
      }
    },
  },
})

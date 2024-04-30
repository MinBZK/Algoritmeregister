// Store for managing the algorithms that the user has access to.
import { defineStore } from 'pinia'
import { useFormDataStore } from './form-data'
import scoreConfig from '@/config/score'

const formDataStore = useFormDataStore()

export const useScoreStore = defineStore('score', {
  getters: {
    progress(): number {
      const data = formDataStore.data
      if (!(data.standard_version in scoreConfig)) {
        console.error(
          'Cannot find standard_version score configuration specified in data'
        )
        return 0
      }

      const config =
        scoreConfig[data.standard_version as keyof typeof scoreConfig]
      let score: number = 0
      let maxScore: number = 0
      Object.entries(config).forEach(([key, value]) => {
        maxScore += value
        if (data[key] === null) return
        if (data[key] === '') return
        if (data[key] === undefined) return
        if (data[key].length === 0) return
        score += value
      })
      // Return score between 0 and 100 for linear progress bar.
      const normalizedScore: number = Math.ceil((score / maxScore) * 100)
      return normalizedScore
    },
    summaryVariant(): 'orange' | 'yellow' | 'green' {
      if (this.progress < 60) return 'orange'
      if (this.progress < 85) return 'yellow'
      else return 'green'
    },
  },
})

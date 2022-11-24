// useVuetify.ts
import { getCurrentInstance, toRaw } from 'vue'

export function useVuetify() {
  const instance = getCurrentInstance()
  if (!instance) {
    throw new Error(`useVuetify should be called in setup().`)
  }
  console.log(toRaw(instance.proxy)?.$vuetify)
  return instance.proxy.$vuetify
}

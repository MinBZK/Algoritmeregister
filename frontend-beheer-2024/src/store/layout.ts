import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLayoutStore = defineStore('layout', () => {
  const showTemplateDrawer = ref<boolean>(false)
  const showVersionDrawer = ref<boolean>(false)

  return { showTemplateDrawer, showVersionDrawer }
})

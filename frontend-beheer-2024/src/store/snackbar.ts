import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'

export enum SnackbarTheme {
  error = 'error',
  success = 'success',
}

export interface Notification {
  list?: string[]
  message: string
  theme?: SnackbarTheme
  duration?: number
}

export const useSnackbarStore = defineStore('snackbar', () => {
  const timeout = ref()
  const queue = ref<Notification[]>([])

  const show = computed(() => {
    if (queue.value.length > 0) return true
    return false
  })
  const activeItem = computed(() => {
    return queue.value[0]
  })

  function showNext() {
    clearTimeout(timeout.value)
    queue.value.shift()
  }
  function add(newItem: Notification) {
    queue.value.push(newItem)
  }

  watch(
    queue,
    async () => {
      if (queue.value.length === 0) {
        return
      }
      timeout.value = setTimeout(() => {
        showNext()
      }, activeItem.value?.duration ?? 4000)
    },
    { deep: true }
  )

  return { showNext, add, activeItem, show }
})

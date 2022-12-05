import { useWindowSize } from '@vueuse/core'

export const useMobileBreakpoint = () => {
  const { width } = useWindowSize()

  const isMobile = ref(true)

  watch(
    width,
    (v) => {
      isMobile.value = width.value < 1200
    },
    { immediate: true }
  )

  return isMobile
}

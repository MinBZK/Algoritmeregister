import { useWindowSize } from '@vueuse/core'

export const useMobileBreakpoint = () => {
  const { width } = useWindowSize()
  return computed(() => width.value < 1200)
}

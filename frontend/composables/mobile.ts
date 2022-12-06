// import { useWindowSize } from '@vueuse/core'
import { useDisplay } from 'vuetify'

export const useMobileBreakpoint = () => {
  // const { width } = useWindowSize()

  // const isMobile = ref(true)

  // watch(
  //   width,
  //   (v) => {
  //     isMobile.value = width.value < 1200
  //   },
  //   { immediate: true }
  // )

  return useDisplay().smAndDown
}

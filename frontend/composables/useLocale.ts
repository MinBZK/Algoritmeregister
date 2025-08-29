export const useLocale = () => {
  const router = useRouter()
  const { locale } = useI18n()
  const $switchLocalePath = useSwitchLocalePath()

  const setLocale = (newLocale: 'nl' | 'en' | 'fy') => {
    locale.value = newLocale

    router.push({ path: $switchLocalePath(newLocale) })
  }

  return { setLocale, currentLocale: locale }
}

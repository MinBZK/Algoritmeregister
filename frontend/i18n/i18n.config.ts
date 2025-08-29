import en from '@/locales/en.json'
import nl from '@/locales/nl.json'
import fy from '@/locales/fy.json'

export default defineI18nConfig(() => ({
  fallbackLocale: 'nl',
  globalInjection: true,
  messages: {
    nl,
    en,
    fy,
  },
}))

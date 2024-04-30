import en from './locales/en.json'
import nl from './locales/nl.json'

export default defineI18nConfig(() => ({
  fallbackLocale: 'nl',
  messages: {
    nl,
    en,
  },
}))

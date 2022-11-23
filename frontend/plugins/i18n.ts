import { createI18n } from 'vue-i18n'
import en from '@/locales/en.json'
import nl from '@/locales/nl.json'

export default defineNuxtPlugin(({ vueApp }) => {
  const i18n = createI18n({
    legacy: false,
    globalInjection: true,
    locale: 'nl',
    fallbackLocale: 'nl',
    messages: {
      en,
      nl,
    },
  })

  vueApp.use(i18n)
})

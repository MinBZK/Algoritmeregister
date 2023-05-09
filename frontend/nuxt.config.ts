import en from './locales/en.json'
import nl from './locales/nl.json'
// https://next.vuetifyjs.com/en/features/treeshaking/#automatic-treeshaking
// import vuetify from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  app: {
    head: {
      link: [{ rel: 'icon', type: 'image/png', href: '/favicon.ico' }],
    },
  },
  modules: ['nuxt-icon', '@nuxtjs/i18n'],
  i18n: {
    strategy: 'prefix',
    locales: ['nl', 'en'],
    defaultLocale: 'nl',
    vueI18n: {
      globalInjection: true,
      locale: 'nl',
      fallbackLocale: 'nl',
      messages: {
        en,
        nl,
      },
    },
  },
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          // https://stackoverflow.com/a/71071183
          // https://stackoverflow.com/a/71540999
          additionalData: `@import "@/assets/styles/global.scss";`,
        },
      },
    },
  },
  css: ['@/assets/styles/main.scss'],
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || '',
      NUXT_APP_BASE_URL: process.env.NUXT_APP_BASE_URL || '/',
      aanleverBaseUrl: process.env.NUXT_AANLEVER_BASE_URL || '',
    },
  },
  typescript: {
    typeCheck: true,
  },
})

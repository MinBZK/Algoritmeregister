import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'url'
import VueI18nVitePlugin from '@intlify/unplugin-vue-i18n/vite'
// https://next.vuetifyjs.com/en/features/treeshaking/#automatic-treeshaking
import vuetify from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  app: {
    head: {
      link: [{ rel: 'icon', type: 'image/png', href: '/favicon.ico' }],
    },
  },
  modules: [
    async (options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) =>
        // @ts-ignore
        config.plugins.push(vuetify())
      )
    },
  ],
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
    plugins: [
      VueI18nVitePlugin({
        include: [
          resolve(dirname(fileURLToPath(import.meta.url)), './locales/*.json'),
        ],
      }),
    ],
  },
  css: ['@/assets/styles/main.scss', 'vuetify/lib/styles/main.sass'],
  build: {
    transpile: ['vuetify'],
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || '',
    },
  },
})

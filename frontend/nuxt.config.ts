import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'url'
import VueI18nVitePlugin from '@intlify/unplugin-vue-i18n/vite'

export default defineNuxtConfig({
  app: {
    head: {
      link: [{ rel: 'icon', type: 'image/png', href: '/favicon.ico' }],
    },
  },
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          // https://stackoverflow.com/a/71071183
          additionalData: `
            @use "@/assets/styles/_colors.scss" as *;
            @import "@/assets/styles/_variables.scss";
          `,
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

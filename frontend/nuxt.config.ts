// https://next.vuetifyjs.com/en/features/treeshaking/#automatic-treeshaking
// import vuetify from 'vite-plugin-vuetify'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'url'
import VueI18nVitePlugin from '@intlify/unplugin-vue-i18n/vite'
// import algoritmeService from './services/algoritme'

const envIsDev = process.env.ENV === 'DEV'

const nuxtConfig = defineNuxtConfig({
  app: {
    head: {
      link: [{ rel: 'icon', type: 'image/png', href: '/favicon.ico' }],
    },
  },
  modules: [
    'nuxt-icon',
    '@nuxtjs/i18n',
    'nuxt-security',
    'nuxt-simple-sitemap',
    '@piwikpro/nuxt-piwik-pro',
  ],
  i18n: {
    locales: ['nl', 'en', 'fy'],
    defaultLocale: 'nl',
    strategy: 'prefix',
    rootRedirect: 'nl',
    vueI18n: './i18n.config.ts',
  },
  sitemap: {
    exclude: ['/en/**', '/fy/**'], // No english versions
  },
  vite: {
    plugins: [
      VueI18nVitePlugin({
        include: [
          resolve(dirname(fileURLToPath(import.meta.url)), './locales/*.json'),
        ],
      }),
    ],
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
    tsConfig: {
      compilerOptions: {
        // baseUrl: "./",
        module: 'ESNext',
        paths: {
          '@/*': ['./*.ts'],
          '~/*': ['./*.ts'],
          '~~/*': ['./*.ts'],
        },
      },
    },
  },
  security: {
    headers: {
      crossOriginEmbedderPolicy: false,
      contentSecurityPolicy: {
        'default-src': ["'self'"],
        'base-uri': ["'self'"],
        'font-src': ["'self'"],
        'connect-src': [
          "'self'",
          'https://api.iconify.design',
        ],
        'form-action': ["'self'"],
        'frame-ancestors': ["'self'"],
        'img-src': ["'self'", 'data:'],
        'object-src': ["'none'"],
        'script-src-attr': ["'none'"],
        'script-src-elem': [
          "'self'",
          "'nonce-{{nonce}}'",
          "'sha256-FGCWaiGgvZVfrUaCByTcd17axhgA37SpuPSjBb0MUK0='",
        ],
        'script-src': [
          "'nonce-{{nonce}}'",
        ],
        'style-src': ["'self'", "'nonce-{{nonce}}'", 'https://www.w3.org'],
        'style-src-attr': ["'self'", "'nonce-{{nonce}}'"],
        'upgrade-insecure-requests': true,
      },
      referrerPolicy: 'strict-origin-when-cross-origin',
      xContentTypeOptions: 'nosniff',
      xDNSPrefetchControl: 'off',
      xFrameOptions: 'SAMEORIGIN',
      permissionsPolicy: {
        camera: ['()'],
        'display-capture': ['()'],
        fullscreen: ['()'],
        geolocation: ['()'],
        microphone: ['()'],
      },
    },
    csrf: true,
    nonce: true,
  },
})

// Overwrite security headers for local development
if (envIsDev) {
  nuxtConfig.security = {
    headers: {
      crossOriginEmbedderPolicy: false,
      contentSecurityPolicy: {
        'base-uri': ["'self'"],
        'font-src': ["'self'", 'https:', 'data:'],
        'form-action': ["'self' localhost:8000"], // Change to "'self' localhost:8000" to make forms works
        'frame-ancestors': ["'self'"],
        'img-src': ["'self'", 'data:'],
        'object-src': ["'none'"],
        'script-src-attr': ["'none'"],
        'style-src': ["'self'", 'https:', "'unsafe-inline'"],
        'upgrade-insecure-requests': true,
      },
      referrerPolicy: 'strict-origin-when-cross-origin',
      xContentTypeOptions: 'nosniff',
      xDNSPrefetchControl: 'off',
      xFrameOptions: 'SAMEORIGIN',
      permissionsPolicy: {
        camera: ['()'],
        'display-capture': ['()'],
        fullscreen: ['()'],
        geolocation: ['()'],
        microphone: ['()'],
      },
    },
    csrf: false,
  }
}

export default nuxtConfig

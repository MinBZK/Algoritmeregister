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
    '@nuxt/icon',
    '@nuxtjs/i18n',
    'nuxt-security',
    'nuxt-simple-sitemap',
  ],
  icon: {
    localApiEndpoint: '/_nuxt_icon',
    clientBundle: {
      icons: [
        'mdi:chevron-down',
        'mdi:close-thick',
        'mdi:chevron-left',
        'mdi:chevron-right',
        'fluent:arrow-sort-down-lines-24-filled',
        'material-symbols:arrow-forward-ios-rounded',
      ],
    },
  },
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
        strictMessage: false,
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
          additionalData: `@use "@/assets/styles/global.scss";`,
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
          
          "'sha256-pJt2pD9qzQdt9kh2YZHw2i0a3G4q//20TW7EJPLHcoU='",
          "'sha256-t7loI1AytHQc9jawaDi2PDNWqPYfJ5jL/+P4O169KoM='",
          "'sha256-kNIRDlh4tVh9qBCRCSaLSgkJrNRPgBpip9PXd1Xwq5Q='",
          "'sha256-MM3CG7szGAeVIKY58JGR+X+7xTDccDemqcIY0lQLrX8='",
          "'sha256-oh6ZTSefRfIBPlcye8dBjlQBkC0A32V1QIb2htJq7ao='",
          "'sha256-Wuuo8pjCq8p1DupaB6iKVd7xGXUV2cZ6FNKupyZkqtA='",
          "'sha256-ieoeWczDHkReVBsRBqaal5AFMlBtNjMzgwKvLqi/tSU='",
          "'sha256-MJNsa/gOJ9T4EeHV9oi5tSwWUA9DgLPaEP096lEeoOY='",
          "'sha256-0IO0VTm9VTAhHV1h/UyKqA9ndkFxJsKyO/a9jSqIDwE='",
        ],
        'script-src': [
          "'nonce-{{nonce}}'",
          
        ],
        'style-src': [
          "'self'",
          "'nonce-{{nonce}}'",
          'https://www.w3.org',
          "'sha256-iDKDruZR4zOvOdjHM4B2dMXZvPW+4KkfQQG24nQQIEg='",
          "'sha256-6CxUj+Gl+jkvAX0QSii1dyHCu+hsTslAx1w/fnxqGNA='",
          "'sha256-aoARGfqdSK6EfiBAN4OBW9aoO8G6gmyJwDX3qzjDG8M='",
          "'sha256-CQAYp0JUk1FawjpfNGhK6D0ysSyGTRTaXuLrXp3AOzU='",
          "'sha256-+Re7dUQMZHn3OLHLFqzeVp2gg7AH1OOuU8yfieqEZXQ='",
        ],
        'style-src-attr': [
          "'self'",
          "'nonce-{{nonce}}'",
          "'sha256-c3S09qVT1Da0LOWxHUdQWEXl+BoJq7pnbFkTr5xJHd8='",
          "'sha256-KLYmnZKIn+krdnHEOoROdy21vRMbchWRnWuDHz1dr4w='",
          "'sha256-noS5t5bV25YK2I9+HEBc94oxdx0JaXrQSR+dc0IO8EE='",
          "'sha256-BmBrB4CXMyF220V06lp5Y7dStmJdczpNT+Ch72jFwCM='",
          "'sha256-6GbXzamjhO51V6Kpu1/6wxeTUNsj/emnJkl56w8kEzk='",
        ],
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

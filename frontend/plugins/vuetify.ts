import { createVuetify } from 'vuetify'
// import * as components from 'vuetify/components'
// import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import { nl, en } from 'vuetify/locale'

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    locale: {
      locale: 'nl',
      messages: { nl, en },
    },
    ssr: true,
  })

  nuxtApp.vueApp.use(vuetify)
})

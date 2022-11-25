import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import { nl, en } from 'vuetify/locale'

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    components,
    directives,
    locale: {
      locale: 'nl',
      messages: { nl, en },
    },
    theme: {
      themes: {
        light: {
          dark: false,
          colors: {
            primary: '#007bc7',
            secondary: '#b2d7ee',
            tertiary: '#e5f1f9',
            quaternary: '#cae3f0',
            quinary: '#d2e5ee',
            accent: '#82B1FF',
            error: '#FF5252',
            info: '#2196F3',
            success: '#4CAF50',
            warning: '#FFC107',
            headerTextColour: '#000000',
            headerHoverColour: '#FCF29A',
          },
        },
      },
    },
  })

  nuxtApp.vueApp.use(vuetify)
})

import App from './App.vue'
import { createApp } from 'vue'
import { registerPlugins } from '@/plugins'

import { useAuthStore } from '@/store/auth'
import Keycloak from 'keycloak-js'
import axios from 'axios'
import Editor from 'primevue/editor'

// ----------------------------------------------- Setup -----------------------------------------------
let APIurl = 'http://localhost:8000/aanleverapi'
if (process.env.NODE_ENV === 'production') {
  APIurl = `${window.location.origin}/aanleverapi`
}

let keycloakConfigUrl = 'http://localhost:8000/api/config'
if (process.env.NODE_ENV === 'production') {
  keycloakConfigUrl = `${window.location.origin}/api/config`
}

export function getConfigs(): Promise<any> {
  // fetch configurations via backend
  return new Promise((resolve) => {
    axios
      .get(keycloakConfigUrl, { timeout: 2000 })
      .then((response: any) => {
        resolve(response.data)
      })
      .catch(function (err: any) {
        console.log('failed to get config ' + err)
      })
  })
}

// ----------------------------------------------- Create App -----------------------------------------------

getConfigs().then((response: any) => {
  const initOptions: any = {
    url: `${response.keycloak_uri}`,
    realm: `${response.keycloak_realm}`,
    clientId: `${response.keycloak_client}`,
    onLoad: 'login-required',
  }
  const keycloak = new Keycloak(initOptions)

  keycloak
    .init({ onLoad: initOptions.onLoad })
    .then(() => {
      // always add the authentication header to axios requests
      axios.interceptors.request.use(function (config: any) {
        const token = keycloak.idToken
        config.baseURL = APIurl
        config.headers!.Authorization = `Bearer ${token}`
        return config
      })

      const app = createApp(App)
      registerPlugins(app)
      // store keycloak object in pinia
      const authStore = useAuthStore()
      authStore.keycloak = keycloak
      authStore.APIurl = APIurl

      app.component('PEditor', Editor)
      app.mount('#app')

      //check token every 6 seconds
      setInterval(() => {
        keycloak.updateToken(70)
      }, 6000)
    })
    .catch((error) => {
      console.log(error)
    })
})

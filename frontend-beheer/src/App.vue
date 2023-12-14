<template>
  <div id="page-wrapper">
    <app-header />
    <v-container id="main" class="container mb-10">
      <router-view />
    </v-container>
    <app-footer id="footer" />
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

import { useLocalStorage } from '@vueuse/core'
import { Organisation } from './types/organisation'
import { useAuthStore } from './store/auth'
import { onMounted } from 'vue'

const authStore = useAuthStore()

// Handle pre-selected organisation from cookie.
const localStorage = useLocalStorage<Organisation | null>(
  'webform-selected-org',
  {} as Organisation | null
).value

onMounted(async () => {
  await authStore.fetchOrganisations()
  if (localStorage) {
    try {
      authStore.selectOrganisation(localStorage.code)
    } catch {
      // localStorage does not match authorization, default to first authorised org.
      authStore.selectedOrg = authStore.organisations[0]!
    }
  } else {
    // First time user, no localStorage.
    authStore.selectedOrg = authStore.organisations[0]!
  }
})
</script>

<style lang="scss">
@import '@/assets/styles/main.scss';

.container {
  max-width: 1500px;
  padding: 0 2rem;
  min-height: 65vh;
}
#page-wrapper {
  position: relative;
}
#main {
  padding-bottom: 2.5rem;
}
#footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 2.5rem;
  padding-top: 2.5rem;
}
</style>

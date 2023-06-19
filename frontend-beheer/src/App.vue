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
import { Organization } from './types'
import { useAuthStore } from './store/auth'

const authStore = useAuthStore()

// Handle pre-selected organization from cookie.
const localStorage = useLocalStorage<Organization | null>(
  'webform-selected-org',
  {} as Organization | null
).value
if (authStore.organizations.length != 0) {
  if (localStorage) {
    try {
      authStore.selectOrganization(localStorage.id)
    } catch {
      // localStorage does not match authorization, default to first authorised org.
      authStore.selectedOrg = authStore.organizations[0]!
    }
  } else {
    // First time user, no localStorage.
    authStore.selectedOrg = authStore.organizations[0]!
  }
}
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

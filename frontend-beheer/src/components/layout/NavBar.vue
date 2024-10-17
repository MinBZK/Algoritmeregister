<template>
  <div class="nav-row">
    <v-container class="nav-bar-centering">
      <v-row no-gutters>
        <v-col class="nav-grid">
          <router-link
            v-for="nav in navOptions"
            :key="nav.name"
            :class="`nav-item ${nav.highlight ? 'selected' : ''}`"
            :to="nav.to"
          >
            {{ nav.name }}
          </router-link>
        </v-col>
        <v-col class="d-flex align-right justify-end">
          <UserDetails />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth'
import { useRoute, useRouter } from 'vue-router'
import { ComputedRef, computed } from 'vue'
import UserDetails from '@/components/UserDetails.vue'

const route = useRoute()
const router = useRouter()

const authStore = useAuthStore()
// Re-direct on initial load
if (!authStore.selectedOrg) {
  router.push('/')
}

interface NavOptions {
  name: string
  to: string
  highlight: boolean
}

const navOptions: ComputedRef<NavOptions[]> = computed(() => {
  // Define ideal order of navigation tabs
  const options = [
    {
      name: 'Algoritmebeschrijvingen',
      to: '/',
      highlight: route.name == 'algorithm.index',
    },
    {
      name: 'Organisatiedetails',
      to: '/organisatie',
      highlight: route.name == 'organisation.index',
    },
    {
      name: 'Dashboard',
      to: '/dashboard',
      highlight: route.name == 'dashboard.index',
    },
  ]
  // Filter out tabs based on permissions
  return options.filter((option) => {
    if (!authStore.canAccesOrgPage && option.to === '/organisatie') return false
    if (!authStore.canAccesDashboard && option.to === '/dashboard') return false
    return true
  })
})
</script>

<style scoped lang="scss">
.nav-row {
  background-color: $primary;
  color: white;
  border-bottom: 10px solid $secondary;
}

.nav-bar-centering {
  max-width: 1450px;
  padding: 0;
}

.nav-grid {
  display: inline-flex;
}

.nav-item {
  padding: 0.75em 1em;
  color: white !important;
  text-decoration: none;

  &.selected {
    background-color: $secondary;
    color: $primary-darker !important;
  }
}
</style>

<template>
  <nav>
    <v-container class="inner-container">
      <v-row
        class="header-row"
        no-gutters
        align="center"
      >
        <div class="logo">
          <router-link to="/">
            <img
              src="../../assets/images/logo.svg"
              alt="Logo Overheid.nl, ga naar de startpagina"
            >
          </router-link>
        </div>
        <v-col class="breadcrumb">
          <Breadcrumb :items="breadcrumbItems || []" />
        </v-col>
      </v-row>
    </v-container>
  </nav>
  <NavBar class="nav-bar" />
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Breadcrumb from '@/components/layout/Breadcrumb.vue'
import { Breadcrumb as BreadcrumbType } from '@/types'
import NavBar from '@/components/layout/NavBar.vue'

const route = useRoute()

const menuExpanded = ref(false)
// set expanded to false after route change
watch(
  () => route.path,
  () => (menuExpanded.value = false)
)
const allBreadcrumbs: Record<string, BreadcrumbType[]> = {
  'algorithm.index': [],
  'algorithm.create': [{ title: 'Algoritme aanmaken', to: '#' }],
  'algorithm.edit': [{ title: 'Algoritme bewerken', to: '#' }],
}
const breadcrumbItems = computed(() => {
  return allBreadcrumbs[route.name as keyof typeof allBreadcrumbs]
})
</script>

<style scoped lang="scss">
.v-container {
  padding: 0;
}

nav {
  background-color: white;
  color: $primary-darker;

  a {
    color: white !important;
    text-decoration: none;
    font-size: 1.3rem;
    font-weight: 500;
  }

  a:hover {
    text-decoration: underline;
  }
}

.nav-bar {
  margin-bottom: 3em;
}

.logo {
  padding-top: 1em;
  padding-left: 1.5em;
  padding-right: 1.5em;
  background-color: white;
  height: 3.5em;
}

.header-row {
  height: 3.5em;
}
.inner-container {
  max-width: 1450px;
}
</style>

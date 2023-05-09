<template>
  <v-container fluid>
    <nav class="row">
      <v-container class="inner-container">
        <v-row class="row-no-margin">
          <div class="logo">
            <router-link to="/">
              <img
                src="../../assets/images/logo.svg"
                alt="Logo Overheid.nl, ga naar de startpagina"
              >
            </router-link>
          </div>
          <v-col class="breadcrumb">
            <breadcrumb :items="breadcrumbItems" />
          </v-col>
          <div class="logout-block">
            <div class="username">
              {{ authStore.keycloak.tokenParsed?.family_name }},
              {{ authStore.keycloak.tokenParsed?.given_name[0] }}. ({{
                authStore.keycloak.tokenParsed?.email
              }})
            </div>
            <button class="logout-button" @click="logout">
              Uitloggen
            </button>
          </div>
        </v-row>
      </v-container>
    </nav>
  </v-container>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Breadcrumb from '@/components/layout/Breadcrumb.vue'
import { Breadcrumb as BreadcrumbType } from '@/types'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

const route = useRoute()

const menuExpanded = ref(false)
// set expanded to false after route change
watch(
  () => route.path,
  () => (menuExpanded.value = false)
)
const allBreadcrumbs: Record<string, BreadcrumbType[]> = {
  'algorithm.index': [],
  'algorithm.create': [{ text: 'Algoritme aanmaken', to: '#' }],
  'algorithm.edit': [{ text: 'Algoritme bewerken', to: '#' }],
}
const breadcrumbItems = computed(() => {
  return allBreadcrumbs[route.name as any] as BreadcrumbType[] | undefined
})

const logout = () => {
  authStore.keycloak.logout()
}
</script>

<style scoped lang="scss">
.v-container {
  padding: 0;
}
nav {
  background-color: $primary;
  color: white;
  margin-bottom: 3rem;
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
.logo {
  padding-top: 1em;
  padding-left: 1.5em;
  padding-right: 1.5em;
  background-color: white;
}
.row-no-margin {
  margin: 0;
  height: 3.5em;
}
.breadcrumb {
  padding-top: 0.3em;
}
.username {
  text-align: end;
  padding-top: 0.25em;
}
.logout-button {
  font-size: 0.75em;
  color: $primary;
  background-color: $tertiary;
  margin-bottom: 0.5em;
  width: 5em;
  justify-self: end;
}

.inner-container {
  max-width: 1200px;
}
.logout-block {
  float: right;
  padding-right: 0.5em;
  display: grid;
  align-items: center;
}
</style>

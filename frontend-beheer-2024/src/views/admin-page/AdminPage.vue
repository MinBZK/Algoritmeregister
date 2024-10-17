<template>
  <h1 class="text-h4 mb-3 mt-0">
    Beheer van gebruikers en organisaties
  </h1>
  <v-tabs
    v-model="currentTab"
    :items="tabs"
    @update:model-value="goToPage"
  />
  <v-divider />
  <router-view />
</template>

<script setup lang="ts">
import router from '@/router'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const tabs = [
  { value: 'beheer.user', text: 'Gebruikers' },
  { value: 'beheer.organisation', text: 'Organisaties' },
]

// Needed to properly move tabs on path change
const currentTab = ref()
const route = useRoute()
watch(route, () => {
  currentTab.value = route.name
})

const goToPage = (e: any) => {
  router.push({ name: e as string })
}
</script>

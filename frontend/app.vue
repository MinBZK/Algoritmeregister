<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import AppContentBar from '@/components/views/AppContentBar.vue'
import AppHeader from '@/components/views/AppHeader.vue'
import AppBreadcrumb from '@/components/views/AppBreadcrumb.vue'
import AppFooter from '@/components/views/AppFooter.vue'

const { t } = useI18n()
</script>

<template>
  <div class="skiplinks container">
    <a href="#content">Direct naar content</a>
  </div>
  <AppHeader />
  <AppContentBar v-if="false" />
  <AppBreadcrumb />

  <div class="container columns columns--sidebar-left row">
    <NuxtPage />
  </div>

  <AppFooter />
</template>

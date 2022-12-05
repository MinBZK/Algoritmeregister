<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="skiplinks container">
    <a href="#content">Direct naar content</a>
  </div>
  <AppHeader />
  <AppContentBar v-if="false" />
  <AppBreadcrumb v-if="false" />

  <div class="container columns columns--sidebar-left row">
    <NuxtPage />
  </div>

  <AppFooter />
</template>

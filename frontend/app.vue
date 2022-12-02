<script setup lang="ts">
// // import AppHeader from '@/components/AppHeader.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
// const algoritmeRegister = computed(() => t('algoritmeRegister'))
</script>

<template>
  <div class="skiplinks container">
    <a href="#content">Direct naar content</a>
  </div>
  <AppHeader />
  <AppContentBar v-if="false" />
  <AppBreadcrumb v-if="false" />

  <div class="container columns columns--sidebar-left row">
    <div>
      <NuxtPage />
    </div>
  </div>

  <AppFooter />
</template>

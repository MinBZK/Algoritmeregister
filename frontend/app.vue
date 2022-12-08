<script setup lang="ts">
import AppContentBar from '@/components/views/AppContentBar.vue'
import AppHeader from '@/components/views/AppHeader.vue'
import AppBreadcrumb from '@/components/views/AppBreadcrumb.vue'
import AppFooter from '@/components/views/AppFooter.vue'
</script>

<template>
  <div class="skiplinks container">
    <a href="#content">Direct naar content</a>
  </div>
  <AppHeader />
  <AppContentBar v-if="false" />
  <AppBreadcrumb />

  <div class="container columns columns--sidebar-left row">
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>

  <AppFooter />
</template>

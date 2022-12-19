<template>
  <div>
    <div class="skiplinks container">
      <a href="#content">Direct naar content</a>
    </div>
    <AppHeader />
    <AppContentBar v-if="false" />
    <AppBreadcrumb />
    <div class="container columns columns--sidebar-left row">
      <div id="content">
        <slot />
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import AppContentBar from '@/components/views/AppContentBar.vue'
import AppHeader from '@/components/views/AppHeader.vue'
import AppBreadcrumb from '@/components/views/AppBreadcrumb.vue'
import AppFooter from '@/components/views/AppFooter.vue'

const { t, locale } = useI18n()
const title = computed(() => t('homepageTitle'))
useHead({ title, htmlAttrs: { lang: locale } })
</script>

<style scoped>
#layout {
  margin: 0 auto 10px auto;
}

.row {
  display: flex;
}

.align-right {
  margin-left: auto;
}

#content {
  margin-left: 0;
}
</style>

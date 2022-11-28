<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const algoritmeRegister = computed(() => t('algoritmeRegister'))
</script>

<template>
  <v-app>
    <div>
      <NuxtLoadingIndicator
        color="repeating-linear-gradient(to right,#01689b 0%,#81c0df 50%,#4fb6e9 100%)"
        :height="5"
      />

      <AppHeader :title="algoritmeRegister" :pages="['algoritme']" />

      <NuxtPage />
    </div>
    <AppFooter />
  </v-app>
</template>

<style lang="scss">
#content {
  max-width: $page-width;
  padding: 0.5em $page-side-padding 0 $page-side-padding;
  margin: 0 auto;
}
</style>

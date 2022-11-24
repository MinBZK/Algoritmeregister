<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
import { useI18n } from 'vue-i18n'
import LanguagePicker from '@/components/LanguagePicker.vue'

const { t } = useI18n()

const helloName = computed(() => t('hello', { name: 'Terry' }))
const algoritmeRegister = computed(() => t('algoritmeRegister'))
</script>

<template>
  <v-app>
    <NuxtLoadingIndicator
      color="repeating-linear-gradient(to right,#01689b 0%,#81c0df 50%,#4fb6e9 100%)"
      :height="5"
    />

    <LanguagePicker />

    <AppHeader :title="algoritmeRegister" :pages="['algoritme']" />

    <LanguagePicker />

    <NuxtPage />

    <AppFooter />
  </v-app>
</template>

<style lang="scss">
#content {
  width: $page-width;
  margin: 0 auto;
  padding-top: 0.5em;
}
</style>

<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
import { useI18n } from 'vue-i18n'
import LanguagePicker from '@/components/LanguagePicker.vue'
</script>

<template>
  <div>
    <NuxtLoadingIndicator
      color="repeating-linear-gradient(to right,#01689b 0%,#81c0df 50%,#4fb6e9 100%)"
      :height="5"
    />

    <AppHeader title="Algoritmeregister" :pages="['algoritme']" />

    <LanguagePicker />

    <NuxtPage />
  </div>
</template>

<style lang="scss">
#content {
  width: $page-width;
  margin: 0 auto;
  padding-top: 0.5em;
}
</style>

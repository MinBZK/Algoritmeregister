<template>
  <Page>
    <h1>{{ t('paths./toegankelijkheid') }}</h1>
  </Page>
</template>

<script setup lang="ts">
import Page from '~~/components/PageWrapper.vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
definePageMeta({
  title: 'Toegankelijkheid',
})
</script>

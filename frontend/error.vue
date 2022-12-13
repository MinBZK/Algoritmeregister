<template>
  <div>
    <AppHeader />
    <NuxtLayout>
      <div>
        <h1>{{ t('error.pageNotFound') }}</h1>
        <FormOverheidButton
          :label="t('error.goToHome')"
          @click="$router.push({ path: '/' })"
        />
      </div>
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import AppHeader from '@/components/views/AppHeader.vue'
const { t } = useI18n()

defineProps<{ error: Error }>()
</script>

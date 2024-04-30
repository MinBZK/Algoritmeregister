<template>
  <a :href="href" target="_blank" class="is-external-mail-icon">
    <span class="visually-hidden">{{ t('mailLink') }}</span>
    <slot />
  </a>
</template>

<script setup lang="ts">
const { t } = useI18n()

defineProps<{ href: string }>()
</script>

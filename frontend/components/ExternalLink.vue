<template>
  <a :href="href" target="_blank" class="is-external-link-icon">
    <span class="visually-hidden">{{ t('externalLink') }}</span>
    <slot />
  </a>
</template>

<script setup lang="ts">
const { t } = useI18n()

defineProps<{ href: string }>()
</script>

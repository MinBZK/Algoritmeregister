<template>
  <a :href="href" target="_blank">
    <slot />
    <img
      class="is-external-icon"
      :alt="t('externalLink')"
      src="@/assets/images/icons/icon-link-external-v2.svg"
    />
  </a>
</template>

<script setup lang="ts">
const { t } = useI18n()

defineProps<{ href: string }>()
</script>

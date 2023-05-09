<template>
  <a :href="href" target="_blank">
    <slot />
    <img
      class="is-external-icon"
      :alt="t('mailLink')"
      src="@/assets/images/icons/icon-mail.svg"
    />
  </a>
</template>

<script setup lang="ts">
const { t } = useI18n()

defineProps<{ href: string }>()
</script>

<template>
  <a :href="href" target="_blank">
    <slot />
    <img
      class="is-external-icon"
      alt="Externe link"
      src="@/assets/images/icons/icon-link-external-v2.svg"
    >
  </a>
</template>

<script setup lang="ts">
defineProps<{ href: string }>()
</script>

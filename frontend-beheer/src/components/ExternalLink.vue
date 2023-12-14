<template>
  <a
    :href="href"
    target="_blank"
    class="is-external-link-icon"
  >
    <slot />
  </a>
</template>

<script setup lang="ts">
defineProps<{ href: string }>()
</script>

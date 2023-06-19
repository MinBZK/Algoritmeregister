<template>
  <a :href="href" target="_blank" class="is-external-link-icon ">
    <slot />
    <span class="visually-hidden">(Externe link)</span>
  </a>
</template>

<script setup lang="ts">
defineProps<{ href: string }>()
</script>

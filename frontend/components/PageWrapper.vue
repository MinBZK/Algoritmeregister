<template>
  <NuxtLayout>
    <slot />
  </NuxtLayout>
</template>

<script setup lang="ts">
const props = defineProps<{ title?: string }>()
const route = useRoute()
const routeTitle = route.meta.title
const displayedTitle = props.title || routeTitle
</script>

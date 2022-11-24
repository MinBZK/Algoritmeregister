<template>
  <NuxtLayout>
    <h1>{{ displayedTitle }}</h1>
    <slot />
  </NuxtLayout>
</template>

<script setup lang="ts">
const props = defineProps<{ title?: string }>()
const route = useRoute()
const routeTitle = route.meta.title
const displayedTitle = props.title || routeTitle
</script>

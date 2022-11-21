<script setup lang="ts">
const route = useRoute()
</script>

<template>
  <div id="content">
    <h1>{{ route.meta.title }}</h1>
    <slot />
  </div>
</template>

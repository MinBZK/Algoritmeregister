<template>
  <Icon :name="props.name" class="nuxt-icon" size="24" />
</template>

<script setup lang="ts">
const props = defineProps<{ name: string }>()
</script>

<style scoped>
.nuxt-icon {
  display: inline-block !important;
  padding-left: 0;
}
</style>

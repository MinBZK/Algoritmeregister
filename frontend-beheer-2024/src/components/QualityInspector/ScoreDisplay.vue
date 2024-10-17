<template>
  <v-progress-linear
    color="#007BC7"
    :model-value="progress"
    height="50"
    class="progress-bar"
    bg-opacity="0.1"
  />
</template>

<script setup lang="ts">
defineProps<{
  progress: number
}>()
</script>

<style lang="scss">
.progress-bar {
  border: 1px solid #e0e0e0;
}
</style>

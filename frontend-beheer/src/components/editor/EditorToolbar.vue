<template>
  <!-- Define which rich text formats are available in toolbar -->
  <span class="ql-formats">
    <button
      v-for="(format, index) in formats"
      :key="index"
      :class="`ql-${format.class}`"
      :value="format.type"
    />
  </span>
</template>

<script setup lang="ts">
defineProps<{
  formats: { class: string, type: string }[]
}>()
</script>

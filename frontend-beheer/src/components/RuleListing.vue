<template>
  <v-list-item>
    {{ ruleName }}
    <template #append>
      <v-icon :icon="icon.name" :color="icon.color" />
    </template>
  </v-list-item>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  ruleName: string
  success: boolean | null
}>()

const icon = computed(() => {
  if (typeof props.success !== 'boolean')
    return { name: 'mdi-minus', color: 'grey' }
  if (props.success) return { name: 'mdi-check', color: 'green' }
  if (!props.success) return { name: 'mdi-alert', color: 'red' }
  return {}
})
</script>

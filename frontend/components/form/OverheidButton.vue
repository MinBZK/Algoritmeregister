<template>
  <button
    class="button button--primary button--nolabel"
    :class="fullWidth && 'button--block'"
    type="submit"
    @click="$emit('click')"
  >
    <span class="button__label"
      >{{ label }} <NuxtIcon v-if="icon" size="0.9em" :name="icon"
    /></span>
  </button>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{ label: string; icon?: string | null; fullWidth?: boolean }>(),
  {
    icon: null,
    fullWidth: false,
  }
)

defineEmits<{
  (e: 'click'): void
}>()
</script>

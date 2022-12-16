<template>
  <button
    class="button button--nolabel"
    :class="{
      'button--block': fullWidth,
      'button--primary': primary,
    }"
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
  defineProps<{
    label: string
    icon?: string | null
    fullWidth?: boolean
    primary?: boolean
  }>(),
  {
    icon: null,
    fullWidth: false,
    primary: true,
  }
)

defineEmits<{
  (e: 'click'): void
}>()
</script>

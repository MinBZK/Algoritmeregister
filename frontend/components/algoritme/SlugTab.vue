<template>
  <li>
    <a
      ref="tabHeaders"
      :key="tabProps.attributeGroupKey"
      :tabindex="toggled ? 0 : -1"
      :aria-selected="toggled"
      class="noselect"
      :class="[toggled ? 'is-selected' : '']"
      role="tab"
      :aria-controls="`panel-${index + 1}`"
      @click="$emit('click')"
      @keydown.enter="$emit('click')"
      @keydown.left.prevent="$emit('navigateTab', -1)"
      @keydown.right.prevent="$emit('navigateTab', 1)"
      >{{ tabProps.attributeGroupKeyLabel }}</a
    >
  </li>
</template>

<script setup lang="ts">
export interface Props {
  tabProps: {
    attributeGroupKey: string
    attributeGroupKeyLabel: string
    properties: {
      attributeKey: string
      attributeValue: string
      attributeKeyDescription: string
      attributeKeyLabel: string
    }[]
  }
  toggled?: boolean
  index: number
}

const props = withDefaults(defineProps<Props>(), {
  toggled: false,
})
const emit = defineEmits<{
  (e: 'navigateTab', direction: number): void
  (e: 'click'): void
}>()
</script>

<template>
  <div class="accordion">
    <AlgoritmeSlugAccordionRow
      v-for="(p, index) in algorithmProperties"
      :key="p.attributeGroupKey"
      :group-props="p"
      v-bind:toggled="toggledRows[index]"
      @toggle-this-row="toggleRows(index)"
    />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  algorithmProperties: {
    attributeGroupKey: string
    attributeGroupKeyLabel: string
    properties: {
      attributeKey: string
      attributeValue: string
      attributeKeyDescription: string
      attributeKeyLabel: string
    }[]
  }[]
}>()

const toggledRows = ref<boolean[]>(Array(props.algorithmProperties.length))
const toggleRows = (index: number) => {
  const currentRowToggled = toggledRows.value[index]
  toggledRows.value = Array(props.algorithmProperties.length).fill(false)
  toggledRows.value[index] = !currentRowToggled
  return 0
}
</script>

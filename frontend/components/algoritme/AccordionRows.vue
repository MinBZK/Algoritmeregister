<template>
  <div class="accordion">
    <AlgoritmeAccordionRow
      v-for="(p, index) in accordionProperties"
      :key="p.groupKey"
      :group-props="p"
      :toggled="toggledRows[index]"
      @toggle-this-row="toggleRows(index)"
    />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  accordionProperties: {
    groupKey: string
    groupKeyLabel: string
    properties: {
      key: string
      value: string
      keyDescription: string
      keyLabel: string
    }[]
  }[]
}>()

const toggledRows = ref<boolean[]>(Array(props.accordionProperties.length))
const toggleRows = (index: number) => {
  const currentRowToggled = toggledRows.value[index]
  toggledRows.value = Array(props.accordionProperties.length).fill(false)
  toggledRows.value[index] = !currentRowToggled
  return 0
}
</script>

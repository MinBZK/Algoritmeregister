<template>
  <div class="tabs" data-decorator="init-tabs">
    <AlgoritmeSlugTabs
      @focus-changed="(v) => (activeAttributeKey = v)"
      :algorithm-properties="algorithmProperties"
    />
    <AlgoritmeSlugTable :table-properties="activeAttributeProperties" />
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

const activeAttributeKey = ref(props.algorithmProperties[0].attributeGroupKey)
const activeAttributeProperties = computed(() => {
  return props.algorithmProperties.filter((groupedProperty) => {
    return groupedProperty.attributeGroupKey === activeAttributeKey.value
  })[0]?.properties
})
</script>

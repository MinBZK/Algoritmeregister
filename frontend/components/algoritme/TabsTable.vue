<template>
  <div class="tabs" data-decorator="init-tabs">
    <AlgoritmeAppTabs
      :tab-properties="tabProperties"
      @focus-changed="(v) => (activeKey = v)"
    />
    <AlgoritmeAppTable :table-properties="activeProperties" />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  tabsTableProperties: {
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

const tabProperties = props.tabsTableProperties.map((s) => {
  return {
    label: s.groupKeyLabel,
    key: s.groupKey,
  }
})

const activeKey = ref(props.tabsTableProperties[0].groupKey)
const activeProperties = computed(() => {
  return props.tabsTableProperties.filter((groupedProperty) => {
    return groupedProperty.groupKey === activeKey.value
  })[0]?.properties
})
</script>

<template>
  <div class="tabs" data-decorator="init-tabs">
    <AlgoritmeAppTabs
      v-if="activeKey"
      v-model:active-tab="activeKey"
      :tab-properties="tabProperties"
    />
    <AlgoritmeAppTable :table-properties="activeProperties" />
  </div>
</template>

<script setup lang="ts">
import { watch } from 'vue'

const props = defineProps<{
  tabsTableProperties: {
    groupKey: string
    properties: {
      key: string
      value: string
      keyDescription: string
      keyLabel: string
    }[]
  }[]
}>()

const tabProperties = computed(() =>
  props.tabsTableProperties.map((s) => {
    return {
      key: s.groupKey,
    }
  })
)

const activeKey = ref<string>(
  useRoute().hash.slice(1) || props.tabsTableProperties[0]?.groupKey
)

const activeProperties = computed(
  () =>
    props.tabsTableProperties.filter(
      (groupedProperty) => groupedProperty.groupKey === activeKey.value
    )[0]?.properties || []
)

watch(props, () => {
  if (!activeKey.value) {
    activeKey.value = props.tabsTableProperties[0]?.groupKey
  }
})
</script>

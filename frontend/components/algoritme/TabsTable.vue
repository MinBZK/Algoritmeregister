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
import { AlgorithmDisplay } from '~~/types/algoritme'

const props = defineProps<{
  tabsTableProperties: AlgorithmDisplay[]
}>()

const tabProperties = computed(() =>
  props.tabsTableProperties.map((group) => {
    return {
      key: group.key,
      keyLabel: group.keyLabel,
    }
  })
)

const activeKey = ref<string>(
  useRoute().hash.slice(1) || props.tabsTableProperties[0]?.key
)

const activeProperties = computed(
  () =>
    props.tabsTableProperties.filter(
      (groupedProperty) => groupedProperty.key === activeKey.value
    )[0]?.properties || []
)

watch(props, () => {
  if (!activeKey.value) {
    activeKey.value = props.tabsTableProperties[0]?.key
  }
})
</script>

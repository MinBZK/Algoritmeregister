<template>
  <v-breadcrumbs :items="breadCrumbItems">
    <template #divider>
      <v-icon
        end
        size="small"
        icon="mdi-chevron-right"
      />
    </template>
  </v-breadcrumbs>
</template>

<script lang="ts" setup>
import { Breadcrumb } from '@/types'
import { computed } from 'vue'

const props = defineProps<{
  items: Breadcrumb[]
}>()

const breadCrumbItems = computed(() => {
  const homeItem = [{ title: 'Algoritmeregister webformulier', to: '/' }]
  return homeItem?.concat(props.items)
})
</script>

<style lang="scss" scoped>
:deep(.v-breadcrumbs-item--disabled) {
  opacity: 1 !important;
}
</style>

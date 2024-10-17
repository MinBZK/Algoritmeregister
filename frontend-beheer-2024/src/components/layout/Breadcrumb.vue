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

import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

const props = defineProps<{
  items: Breadcrumb[]
}>()

const breadCrumbItems = computed(() => {
  const homeItem: Breadcrumb = {
    title: 'Algoritmeregister webformulier 2024',
    href: '/',
  }

  const currentOrganisation = {
    title: authStore.selectedOrg?.name || '',
    href: '#',
  }

  return [homeItem, currentOrganisation, ...props.items]
})
</script>

<style lang="scss" scoped>
:deep(.v-breadcrumbs-item--disabled) {
  opacity: 1 !important;
}
</style>

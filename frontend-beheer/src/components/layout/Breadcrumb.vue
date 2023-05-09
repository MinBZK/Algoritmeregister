<template>
  <div style="float: left; margin-top: 0.6em">
    <router-link to="/" class="nav-link">
      {{ appName }}
    </router-link>
    <v-icon
      v-if="showChevron"
      end
      size="small"
      icon="mdi-chevron-right"
    />
  </div>
  <v-breadcrumbs :items="items" divider=">" />
</template>

<script lang="ts" setup>
import { Breadcrumb } from '@/types'
import { computed } from 'vue'

const props = defineProps<{
  items?: Breadcrumb[]
}>()

const showChevron = computed(() => {
  return props.items ? props.items.length > 0 : false
})

const appName = import.meta.env.VITE_APP_NAME
</script>

<style lang="scss" scoped>
:deep(.v-breadcrumbs-item--disabled) {
  opacity: 1 !important;
  font-weight: bold;
}
.nav-link {
  color: white;
  color: white !important;
  text-decoration: none;
  font-size: 1.3rem;
  font-weight: 500;
}
.nav-link:hover {
  text-decoration: underline;
}
</style>

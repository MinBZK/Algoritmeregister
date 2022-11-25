<template>
  <div class="search-filters">
    <div
      v-for="aggregationType in props.aggregatedAlgoritmes"
      :key="aggregationType.aggregationAttribute"
    >
      <h4>{{ aggregationType.aggregationAttribute }}</h4>
      <div
        v-for="[k, v] in Object.entries(aggregationType.aggregatedValues)"
        :key="k"
      >
        <NuxtLink
          :to="{
            name: 'algoritme',
            query: {
              q: getEncodedQuery(aggregationType.aggregationAttribute, k),
            },
          }"
        >
          <span>{{ k || '-' }}</span
          >&nbsp;<span class="text-secondary">({{ v }})</span>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import qs from 'qs'

import type { AggregatedAlgoritmes } from '@/types/algoritme'

const props = defineProps<{ aggregatedAlgoritmes: AggregatedAlgoritmes[] }>()

const getEncodedQuery = (attribute: string, value: string): string => {
  const stringified = qs.stringify({
    filters: [
      { attribute, value },
      { attribute, value },
    ],
  })
  return stringified
}
</script>

<style scoped lang="scss">
.search-filters {
  background-color: $tertiary;
  padding: 1em;
}

.text-secondary {
  color: $primary !important;
}
</style>

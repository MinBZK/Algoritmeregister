<template>
  <div v-if="filterData && selectedFilters">
    <template v-if="!isMobile">
      <FilterSelectedFilters
        v-if="selectedFilters.length"
        :selected-filters="selectedFilters"
        class="selected-filter"
      />
      <template v-for="[key, thisFilterData] in filterDataEntries" :key="key">
        <FilterSingleSelect
          v-if="!filterConfig[key]?.isActive"
          :query-key="key"
          :options="thisFilterData"
          enable-read-more
          enable-read-less
          :max-size="filterConfig[key]?.maxSize"
        />
      </template>
    </template>
    <template v-else>
      <div class="mobile-filters">
        <FilterMobileFilter>
          <h1>Filters</h1>
          <FilterSelectedFilters
            v-if="selectedFilters.length"
            :selected-filters="selectedFilters"
            class="selected-filter"
          />
          <template v-for="[key, value] in filterDataEntries" :key="key">
            <FilterSingleSelect
              v-if="!filterConfig[key].isActive"
              :query-key="key"
              :options="value"
              enable-read-more
              enable-read-less
              :max-size="filterConfig[key].maxSize"
            />
          </template>
        </FilterMobileFilter>
        <FilterMobileSelectedFilters :selected-filters="selectedFilters" />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { useMobileBreakpoint } from '@/composables/mobile'
import type { FilterData } from '@/types/filter'
import type {
  AlgoritmeFilterData,
  AlgoritmeFilterQuery,
  AlgoritmeSelectedFilter,
} from '@/types/filter/algoritme'

const props = defineProps<{
  selectedFilters?: AlgoritmeSelectedFilter[]
  filterData?: AlgoritmeFilterData
}>()

const isMobile = useMobileBreakpoint().medium

interface FilterConfig {
  isActive: boolean
  maxSize: number
}

// Type-casting here so that the v-for does not give errors.
const filterDataEntries = computed(() => {
  if (!props.filterData) return []
  return Object.entries(props.filterData) as [
    keyof AlgoritmeFilterQuery,
    FilterData[],
  ][]
})

const filterConfig = computed(
  (): Record<keyof AlgoritmeFilterData, FilterConfig> => {
    const base = {
      impact_assessment: { isActive: false, maxSize: 7 },
      organisation: { isActive: false, maxSize: 7 },
      organisationtype: { isActive: false, maxSize: 7 },
      publicationcategory: { isActive: false, maxSize: 7 },
    }
    props.selectedFilters?.forEach((selectedFilter) => {
      if (selectedFilter.key === 'searchtext') return
      base[selectedFilter.key].isActive = true
    })
    return base
  }
)
</script>

<style scoped lang="scss">
.selected-filter {
  margin-bottom: 0.5em;
}

.mobile-filters {
  margin-bottom: 1.25em;
}
</style>

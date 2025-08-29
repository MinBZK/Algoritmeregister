<template>
  <FilterBlock :title="t('filter.selectedFilters')">
    <div v-for="filter in selectedFilters" :key="filter.key">
      <strong>{{ t('filter.selectedFilter.' + filter.key) }}:</strong> <br />
      <NuxtLink
        class="chosen-filter"
        :aria-label="$t('filter.aria/remove', { what: filter.value }) || ''"
        :to="filterRemoved(filter)"
      >
        {{ filter.value }}
        <img src="@/assets/images/icons/icon-close.svg" aria-hidden alt="" />
      </NuxtLink>
    </div>
    <template #append-title>
      <NuxtLink :to="{ query: { sort_option: SortOption.sortByName } }">
        {{ t('filter.removeAll') }}
      </NuxtLink>
    </template>
  </FilterBlock>
</template>

<script setup lang="ts">
import type { GenericSelectedFilter, GenericQuery } from '@/types/filter'
import { SortOption } from '@/types/filter/algoritme'

const { t } = useI18n()

defineProps<{
  selectedFilters: GenericSelectedFilter[]
}>()

const currentQuery = computed(() => useRoute().query as GenericQuery)

const filterRemoved = (filter: GenericSelectedFilter) => {
  const query = { ...currentQuery.value }
  if (filter.key in query) {
    delete query[filter.key]
  }
  return { query }
}
</script>

<style scoped lang="scss">
.chosen-filter {
  width: 100%;
  display: inline-flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;

  img {
    height: 0.75em;
  }
}
</style>

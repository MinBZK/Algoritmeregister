<template>
  <div class="search-filters">
    <template v-if="isMobile">
      <a
        tabindex="0"
        :aria-expanded="filtersExpanded ? 'true' : 'false'"
        @click="toggleFilters"
        @keyup.enter="toggleFilters"
        >{{ $t(filtersExpanded ? 'hideFilters' : 'showFilters') }}</a
      >
    </template>

    <template v-if="filtersExpanded">
      <div v-if="parsedFilters.length > 0" class="search-filter-item">
        <h2>{{ $t('selectedAlgorithms') }}</h2>
        <div v-for="f in parsedFilters" :key="f.attribute">
          <NuxtLink
            :to="localePath(getFilterPath(f, 'remove'))"
            :aria-label="$t('filters.aria/remove', { what: f.value }) || ''"
          >
            {{ f.value || '-' }}
            <NuxtIcon name="system-uicons:cross" class="text-secondary" />
          </NuxtLink>
        </div>
      </div>
      <template
        v-for="aggregation in props.aggregatedAlgoritmes"
        :key="aggregation.aggregation_attribute"
        ><div
          v-if="
            getAttributeFilters(aggregation.aggregation_attribute).length > 0
          "
          class="search-filter-item"
        >
          <h2>
            {{
              $t(
                `algorithmProperties.${aggregation.aggregation_attribute}.label`
              )
            }}
          </h2>

          <div
            v-for="aggregationValue in getAttributeFilters(
              aggregation.aggregation_attribute
            )"
            :key="aggregationValue.aggregation_value"
          >
            <NuxtLink
              :to="
                localePath(
                  getFilterPath(
                    {
                      attribute: aggregation.aggregation_attribute,
                      value: aggregationValue.aggregation_value,
                    },
                    'add'
                  )
                )
              "
            >
              <span>{{
                aggregationValue.aggregation_value || '-'
              }}</span></NuxtLink
            >

            <!-- <span class="link-disabled">{{ aggregationValue || '-' }}</span> -->

            &nbsp;<span class="text-secondary"
              >({{ aggregationValue.count }})</span
            >
          </div>
        </div>
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { stringify } from 'qs'
import type { AggregatedAlgoritme, AlgoritmeFilter } from '@/types/algoritme'
import { useMobileBreakpoint } from '~~/composables/mobile'

const props = defineProps<{ aggregatedAlgoritmes: AggregatedAlgoritme[] }>()

const isMobile = useMobileBreakpoint().medium
const localePath = useLocalePath()

const parsedQuery = computed(() => useRouteQuery())
const parsedFilters = computed(
  () => (parsedQuery.value.filters || []) as AlgoritmeFilter[]
)

const getFilterPath = (
  filter: AlgoritmeFilter,
  transaction: 'add' | 'remove'
) => {
  const filters =
    transaction === 'add' ? addFilter(filter) : removeFilter(filter)
  return getFilterRoute(filters)
}

const removeFilter = (filter: AlgoritmeFilter) => {
  const filterToBeRemoved = parsedFilters.value.find(
    (f) => f.attribute === filter.attribute
  )
  if (filterToBeRemoved) {
    const newFilters = [...parsedFilters.value]
    const filterIndex = newFilters.indexOf(filterToBeRemoved)
    newFilters.splice(filterIndex, 1)
    return newFilters
  } else {
    return parsedFilters.value
  }
}

const getFilterRoute = (filters: AlgoritmeFilter[]) => {
  const searchQuery = useRoute().query.search
  let query
  if (filters.length > 0) {
    query = { q: stringify({ filters }), search: searchQuery }
  } else if (searchQuery && searchQuery.length > 0) {
    query = { search: searchQuery }
  } else {
    query = {}
  }
  return {
    name: 'algoritme',
    query,
  }
}

const addFilter = (filter: AlgoritmeFilter): AlgoritmeFilter[] => {
  const { attribute, value } = filter
  return [{ attribute, value }, ...parsedFilters.value]
}

const getAttributeFilters = (attribute: string) => {
  const values = props.aggregatedAlgoritmes.find(
    (a) => a.aggregation_attribute === attribute
  )?.values

  const filteredValues = (values || []).filter((a) => {
    return (
      parsedFilters.value.filter(
        (pF) => pF.attribute === attribute && pF.value === a.aggregation_value
      ).length === 0
    )
  })

  return filteredValues.sort((a, b) =>
    a.aggregation_value > b.aggregation_value ? 1 : -1
  )
}

// mobile only
const showFilters = ref(false)
const filtersExpanded = computed(() => !isMobile.value || showFilters.value)
const toggleFilters = () => (showFilters.value = !showFilters.value)
</script>

<style scoped lang="scss">
.search-filters {
  background-color: $tertiary;
  padding: 1em;
}

.text-secondary {
  color: $primary !important;
}

.search-filter-item:first-child {
  padding-top: 0px;
}

.search-filter-item {
  padding-top: 1.5em;
}

.search-filters a {
  cursor: pointer;
}

.link-disabled {
  cursor: not-allowed;
  color: #7ca1c9;
}

h2 {
  font-size: 1em;
}
</style>

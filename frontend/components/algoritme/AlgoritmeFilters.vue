<template>
  <div
    class="search-filters"
    :aria-expanded="filtersExpanded ? 'true' : 'false'"
  >
    <template v-if="isMobile">
      <a @click="toggleFilters" @keyup.enter="toggleFilters" tabindex="0">{{
        $t(filtersExpanded ? 'hideFilters' : 'showFilters')
      }}</a>
    </template>
    <template v-if="filtersExpanded">
      <div v-if="parsedFilters.length > 0" class="search-filter-item">
        <h4>{{ $t('selectedAlgorithms') }}</h4>
        <div
          v-for="f in parsedFilters"
          @click="removeFilter(f)"
          @keyup.enter="removeFilter(f)"
          tabindex="0"
        >
          <a>
            {{ f.value || '-' }}
          </a>
          <NuxtIcon name="system-uicons:cross" class="text-secondary" />
        </div>
      </div>
      <template
        v-for="aggregationType in props.aggregatedAlgoritmes"
        :key="aggregationType.aggregationAttribute"
        ><div
          class="search-filter-item"
          v-if="
            getAttributeFilters(aggregationType.aggregationAttribute).length > 0
          "
        >
          <h4>
            {{
              $t(
                `algorithmProperties.algemeneInformatie.${aggregationType.aggregationAttribute}.label`
              )
            }}
          </h4>

          <div
            v-for="[attributeValue, count] in getAttributeFilters(
              aggregationType.aggregationAttribute
            )"
            :key="attributeValue"
          >
            <NuxtLink
              v-if="
                !hasFilter(aggregationType.aggregationAttribute, attributeValue)
              "
              :to="{
                name: 'algoritme',
                query: {
                  q: getEncodedFiltersQuery(
                    aggregationType.aggregationAttribute,
                    attributeValue
                  ),
                  page: 1,
                },
              }"
            >
              <span>{{ attributeValue || '-' }}</span></NuxtLink
            >

            <span
              v-if="
                hasFilter(aggregationType.aggregationAttribute, attributeValue)
              "
              class="link-disabled"
              >{{ attributeValue || '-' }}</span
            >

            &nbsp;<span class="text-secondary">({{ count }})</span>
          </div>
        </div>
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import qs from 'qs'
import type { AggregatedAlgoritmes, AlgoritmeFilter } from '@/types/algoritme'

const props = defineProps<{ aggregatedAlgoritmes: AggregatedAlgoritmes[] }>()

const getEncodedFiltersQuery = (attribute: string, value: string): string => {
  const stringified = qs.stringify({
    filters: [{ attribute, value }, ...parsedFilters.value],
  })
  return stringified
}

const isMobile = useMobileBreakpoint()

const parsedQuery = computed(() => useRouteQuery())
const parsedFilters = computed(
  () => (parsedQuery.value.filters || []) as AlgoritmeFilter[]
)

const removeFilter = (filter: AlgoritmeFilter) => {
  const filterToBeRemoved = parsedFilters.value.find(
    (f) => f.attribute == filter.attribute
  )
  if (filterToBeRemoved) {
    const newFilters = [...parsedFilters.value]
    const filterIndex = newFilters.indexOf(filterToBeRemoved)
    newFilters.splice(filterIndex, 1)
    const router = useRouter()
    router.push({
      name: 'algoritme',
      query: { q: qs.stringify({ filters: newFilters }) },
    })
  }
}

const getAttributeFilters = (attribute: string) => {
  const values = props.aggregatedAlgoritmes.find(
    (a) => a.aggregationAttribute == attribute
  )?.aggregatedValues

  const filterdValues = Object.entries(values || []).filter(
    ([filterAttributeValue]) => {
      return (
        parsedFilters.value.filter(
          (pF) => pF.attribute == attribute && pF.value == filterAttributeValue
        ).length == 0
      )
    }
  )

  return filterdValues
}

const hasFilter = (attribute: string, attributeValue: string): boolean =>
  parsedFilters.value.filter(
    (pF) => pF.attribute == attribute && pF.value == attributeValue
  ).length > 0

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
</style>

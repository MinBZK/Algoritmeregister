<template>
  <div
    class="search-filters"
    :aria-expanded="filtersExpanded ? 'true' : 'false'"
  >
    <template v-if="mdAndDown"
      ><v-icon icon="mdi-filter" /><a
        @click="toggleFilters"
        @keyup.enter="toggleFilters"
        tabindex="0"
        >{{ $t(filtersExpanded ? 'hideFilters' : 'showFilters') }}</a
      >
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
          <v-icon icon="mdi-close" size="small"></v-icon>
        </div>
      </div>

      <div
        v-for="aggregationType in props.aggregatedAlgoritmes"
        :key="aggregationType.aggregationAttribute"
        class="search-filter-item"
      >
        <h4>
          {{
            $t(
              `algorithmProperties.algemeneInformatie.${aggregationType.aggregationAttribute}.label`
            )
          }}
        </h4>

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
    </template>
  </div>
</template>

<script setup lang="ts">
import qs from 'qs'
import type { AggregatedAlgoritmes, AlgoritmeFilter } from '@/types/algoritme'
import { useDisplay } from 'vuetify'

const display = useDisplay()

const { mdAndDown } = useDisplay()

const props = defineProps<{ aggregatedAlgoritmes: AggregatedAlgoritmes[] }>()

const getEncodedQuery = (attribute: string, value: string): string => {
  const stringified = qs.stringify({
    filters: [{ attribute, value }, ...parsedFilters.value],
  })
  return stringified
}

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
    console.log({ filterIndex, newFilters, filterToBeRemoved })
    const router = useRouter()
    router.push({
      name: 'algoritme',
      query: { q: qs.stringify({ filters: newFilters }) },
    })
  }
}

// mobile only
const showFilters = ref(false)
const filtersExpanded = computed(() => !mdAndDown.value || showFilters.value)
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
</style>

<template>
  <SearchBar v-bind:value="searchQuery" @input="(v) => (searchQuery = v)" />

  <div class="row container columns">
    <div class="column-d-3">
      <AlgoritmeFilters
        :aggregatedAlgoritmes="aggregatedAlgoritmes"
        v-if="paginatedAlgoritmes.length != 0"
      />
    </div>
    <div class="column-d-9">
      <h1>{{ t(`foundResults`, { n: filteredAlgoritmes.length }) }}</h1>
      <Pagination
        v-if="nPages > 1"
        :current-page="page"
        :page-length="nPages"
        @setPage="(p) => setPage(p)"
      />
      <!-- <Sort /> -->
      <div class="result--list result--list__data">
        <ul v-if="paginatedAlgoritmes.length != 0">
          <SearchResultCard
            :algoritme="algoritme"
            v-for="algoritme in paginatedAlgoritmes"
          ></SearchResultCard>
        </ul>
        <div v-if="paginatedAlgoritmes.length == 0">
          {{ t('noResults') }}
        </div>
      </div>
      <Pagination
        v-if="nPages > 1"
        :current-page="page"
        :page-length="nPages"
        @setPage="(p) => setPage(p)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import algoritmeService from '@/services/algoritme'
import { useI18n } from 'vue-i18n'
import type {
  Algoritme,
  AggregatedAlgoritmes,
  AlgoritmeFilter,
} from '@/types/algoritme'
import AlgoritmeFilters from '@/components/algoritme/AlgoritmeFilters.vue'

const { t } = useI18n()

definePageMeta({
  title: 'Algoritmeoverzicht',
})

const parsedQuery = computed(() => useRouteQuery())
const searchQuery = ref<string>((parsedQuery.value.search as string) || '')
const parsedFilters = computed(
  () => parsedQuery.value.filters as AlgoritmeFilter[]
)

const { data } = await algoritmeService.getAll()
let algoritmes = ref(data.value as Algoritme[])

const filteredAlgoritmes = computed(() => {
  const searchQueryString = String(searchQuery.value)

  return algoritmes.value.filter((algoritme) => {
    const includedSearchFields = ['organization', 'name', 'description_short']

    const allowedBySearch =
      searchQueryString.length > 0
        ? includedSearchFields
            .map((field) => {
              const value = algoritme[field as keyof typeof algoritme]
              return value
                ? value.toLowerCase().includes(searchQueryString.toLowerCase())
                : false
            })
            .some((v) => v)
        : true

    const allowedByQueryFilters = (parsedFilters.value || [])
      .map(
        ({ attribute, value }) =>
          algoritme[attribute as keyof Algoritme] == value
      )
      .every((v) => v)

    return allowedByQueryFilters && allowedBySearch
  })
})

const page = computed(() => {
  const route = useRoute()
  const page = Array.isArray(route.query.page)
    ? route.query.page[0]
    : route.query.page
  return parseInt(page || '1')
})

const pageLength = 10
const nPages = computed(() =>
  Math.ceil(filteredAlgoritmes.value.length / pageLength)
)
const paginatedAlgoritmes = computed(() =>
  filteredAlgoritmes.value.slice(
    (page.value - 1) * pageLength,
    page.value * pageLength
  )
)

const aggregatedAlgoritmes = computed(() => {
  const groupOnAttributes = ['organization']
  const result: AggregatedAlgoritmes[] = groupOnAttributes.map(
    (aggregationAttribute) => {
      return {
        aggregationAttribute,
        aggregationType: 'count',
        aggregatedValues: filteredAlgoritmes.value.reduce((obj, algoritme) => {
          const value = algoritme[aggregationAttribute as keyof Algoritme]
          if (obj[value]) {
            obj[value] = obj[value] + 1
          } else {
            obj[value] = 1
          }
          return obj
        }, {} as Record<string, number>),
      }
    }
  )
  return result
})

const setPage = (newPage: number) => {
  const router = useRouter()
  const route = useRoute()
  router.push({
    name: 'algoritme',
    query: { ...route.query, page: newPage },
  })
}

watch(searchQuery, () => {
  setPage(1)
})
</script>

<style scoped lang="scss">
.item-header {
  margin-bottom: 15px;
}
.word-break {
  word-break: break-word;
}
</style>

<template>
  <div>
    <SearchBar :value="searchQuery" @input="(v) => (searchQuery = v)" />

    <div class="row container columns" id="search-container">
      <div class="column-d-3">
        <AlgoritmeFilters
          v-if="aggregations.length > 0"
          :aggregated-algoritmes="aggregations"
        />
      </div>
      <div class="column-d-9">
        <h1>{{ t(`foundResults`, { n: totalCount }) }}</h1>
        <div class="row container columns">
          <div class="column-d-6">
            <TablePagination
              v-if="nPages > 1"
              :current-page="page"
              :page-length="nPages"
              @set-page="(p) => setPage(p)"
            />
          </div>
          <div class="column-d-6" :class="!isMobile && 'align-right'">
            <a :href="algoritmeService.downloadUrl()">
              <FormOverheidButton
                label="Download alle algoritmes (.csv)"
                class="no-margin"
                icon="mdi:download"
                :primary="false"
              />
            </a>
          </div>
        </div>
        <!-- <Sort /> -->
        <div class="result--list result--list__data">
          <ul v-if="algoritmes.length != 0">
            <SearchResultCard
              v-for="algoritme in algoritmes"
              :key="algoritme.slug"
              :algoritme="algoritme"
              mode="compact"
            ></SearchResultCard>
          </ul>
          <div v-if="algoritmes.length == 0">
            {{ t('noResults') }}
          </div>
        </div>
        <TablePagination
          v-if="nPages > 1"
          :current-page="page"
          :page-length="nPages"
          @set-page="(p) => setPage(p)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDebounceFn } from '@vueuse/core'
import algoritmeService from '@/services/algoritme'
import type { AlgoritmeFilter } from '@/types/algoritme'
import AlgoritmeFilters from '@/components/algoritme/AlgoritmeFilters.vue'

const { t } = useI18n()

const isMobile = useMobileBreakpoint()

definePageMeta({
  title: 'Algoritmeoverzicht',
})

const parsedQuery = computed(() => useRouteQuery())
const searchQuery = ref<string>((parsedQuery.value.search as string) || '')
const parsedFilters = computed(
  () => (parsedQuery.value.filters || []) as AlgoritmeFilter[]
)

const page = computed(() => {
  const route = useRoute()
  const page = Array.isArray(route.query.page)
    ? route.query.page[0]
    : route.query.page
  return parseInt(page || '1')
})

const pageLength = 10

let { data } = await algoritmeService.getAll({
  filters: parsedFilters.value,
  page: page.value,
  limit: pageLength,
  search: searchQuery.value,
})

const updateData = async () => {
  const response = await algoritmeService.getAll({
    filters: parsedFilters.value,
    page: page.value,
    limit: pageLength,
    search: searchQuery.value,
  })
  data = response.data
}

const totalCount = computed(() => data.value?.total_count || 0)
const aggregations = computed(() => data.value?.aggregations || [])
const algoritmes = computed(() => data.value?.results || [])

const nPages = computed(() => Math.ceil(totalCount.value / pageLength))

const setPage = (newPage: number) => {
  const router = useRouter()
  const route = useRoute()
  router.push({
    name: 'algoritme',
    query: { ...route.query, page: newPage },
  })
}

const debouncedUpdate = useDebounceFn(async () => {
  await updateData()
  setPage(1)
}, 500)

watch(searchQuery, () => debouncedUpdate())

watch(parsedFilters, () => updateData())
</script>

<style scoped lang="scss">
.item-header {
  margin-bottom: 15px;
}
.word-break {
  word-break: break-word;
}

.no-margin {
  margin-top: 9px;
}

.align-right {
  justify-content: right;
}

#search-container {
  padding: 0 0;
}
</style>

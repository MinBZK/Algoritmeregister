<template>
  <div>
    <SearchBar @do-search="reactToSearch()" />

    <div class="row container columns no-padding">
      <div v-if="algoritmes.length != 0 || loading" class="column-d-3">
        <AlgoritmeFilters :aggregated-algoritmes="aggregations" />
      </div>
      <div class="column-d-9">
        <h1 role="status">
          {{ t(`foundResults`, { n: totalCount }) }}
          {{ readTitle ? '&nbsp;' : null }}
        </h1>
        <div
          v-if="algoritmes.length != 0"
          class="row container columns no-padding"
        >
          <div class="column-d-6">
            <TablePagination
              v-if="nPages > 1"
              :current-page="page"
              :page-length="nPages"
              @set-page="(p) => setPage(p)"
            />
          </div>
          <div
            v-if="algoritmes.length != 0"
            class="column-d-6"
            :class="!isMobile && 'align-right'"
          >
            <FormOverheidButton
              :label="t('downloadAllAlgorithms')"
              :action="algoritmeService.downloadUrl()"
              :style="'secondary'"
              class="no-margin"
              icon="mdi:download"
            />
          </div>
        </div>
        <div
          v-if="algoritmes.length != 0"
          class="result--list result--list__data"
        >
          <ul>
            <li
              v-for="(algoritme, index) in algoritmes"
              :key="algoritme.algoritme_id"
            >
              <SearchResultCard
                :set-focus="index == 0 && newFocusIsRequested"
                :algoritme="algoritme"
                mode="compact"
                @focus-has-been-set="newFocusIsRequested = false"
              >
              </SearchResultCard>
            </li>
          </ul>
        </div>
        <TablePagination
          v-if="nPages > 1"
          :current-page="page"
          :page-length="nPages"
          @set-page="(p) => setPage(p)"
        />
        <div v-if="algoritmes.length == 0 && !loading">
          <p>{{ t('algoritmeIndex.noResults.p1') }}</p>
          <ul class="no-results">
            <li>
              {{ t('algoritmeIndex.noResults.l1') }}
            </li>
            <li>
              {{ t('algoritmeIndex.noResults.l2') }}
            </li>
            <li>
              {{ t('algoritmeIndex.noResults.l3') }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import algoritmeService from '@/services/algoritme'
import type { AlgoritmeFilter } from '@/types/algoritme'
import AlgoritmeFilters from '@/components/algoritme/AlgoritmeFilters.vue'

const { t } = useI18n()

const isMobile = useMobileBreakpoint().medium

const parsedQuery = computed(() => useRouteQuery())
const searchQuery = computed(() => (useRoute().query.search as string) || '')

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

const loading = ref(false)
const updateData = async () => {
  loading.value = true
  if (data.value) {
    data.value.results = []
  }
  const response = await algoritmeService.getAll({
    filters: parsedFilters.value,
    page: page.value,
    limit: pageLength,
    search: searchQuery.value,
  })
  data = response.data
  loading.value = false
}

const totalCount = computed(() => data.value?.total_count || 0)
const aggregations = computed(() => data.value?.aggregations || [])
const algoritmes = computed(() => data.value?.results || [])

const nPages = computed(() => Math.ceil(totalCount.value / pageLength))

const localePath = useLocalePath()
const setPage = (newPage: number) => {
  const router = useRouter()
  const route = useRoute()
  router.push(
    localePath({
      name: 'algoritme',
      query: { ...route.query, page: newPage.toString() },
    })
  )
  scroll(0, 0)
}

const searchPageTitle = computed(() =>
  searchQuery.value
    ? t(`foundResults`, { n: totalCount.value }).concat(
        t(`forSearch`, { searchQuery: searchQuery.value })
      )
    : t(`algoritmeIndex.pageTitle`)
)

// default value is true, so that when we search from the homepage the focus is always placed correctly.
const readTitle = ref<boolean>(false)
const newFocusIsRequested = ref<boolean>(false)
const reactToSearch = async () => {
  await updateData()
  setPage(1)
  newFocusIsRequested.value = true

  // In some situations, say the page title again. Everytime state changes, the title is updated and read.
  readTitle.value = !readTitle.value
}

watch(searchQuery, () => {
  reactToSearch()
})

watch(parsedFilters, () => updateData())

useHead({ title: searchPageTitle })
providePageTitle({
  title: 'algoritmeIndex.pageTitle',
  labelType: 'locale-index',
})
</script>

<style scoped lang="scss">
.item-header {
  margin-bottom: 15px;
}

.word-break {
  word-break: break-word;
}

.align-right {
  justify-content: right;
}

ul.no-results {
  list-style-image: url(@/assets/images/icons/icon-dart-right-blue.svg);
  line-height: 2 !important;
  padding-left: 3em;
}

li {
  padding-left: 1em;
}

h1.no-margin {
  margin: 0em;
}
</style>

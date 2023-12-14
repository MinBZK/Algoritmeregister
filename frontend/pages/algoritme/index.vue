<template>
  <div>
    <LanguageDisclaimer
      v-if="locale == 'en'"
      class="language-disclaimer"
      :density="isMobile ? 'compact' : 'default'"
    />
    <SearchBar type="no-link" @do-search="doSearch" />

    <div class="row container columns no-padding">
      <div v-if="!loading" class="column-d-3">
        <FilterGroup
          :filter-data="data?.filter_data"
          :selected-filters="data?.selected_filters"
        />
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
              :current-page="+page"
              :page-length="nPages"
              @set-page="(p) => setPage(p)"
            />
          </div>
          <div
            v-if="algoritmes.length != 0"
            class="column-d-6 center-with-pagination"
            :class="!isMobile && 'align-right'"
          >
            <FormOverheidButton
              :label="t('downloadAllAlgorithms')"
              :action="
                algoritmeService.downloadAllUrl(
                  mapLocaleName(locale as 'en' | 'nl')
                )
              "
              :hidden-query="[{ name: 'filetype', value: 'excel' }]"
              :style="'secondary'"
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
                @focus-has-been-set="newFocusIsRequested = false"
              >
              </SearchResultCard>
            </li>
          </ul>
        </div>
        <TablePagination
          v-if="nPages > 1"
          :current-page="+page"
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
import type { AlgoritmeQuery } from '@/services/algoritme'
import { mapLocaleName } from '@/utils'
import algoritmeService from '@/services/algoritme'
import FilterGroup from '@/components/filter/FilterGroup.vue'

const { t, locale } = useI18n()
const router = useRouter()
const localePath = useLocalePath()
const isMobile = useMobileBreakpoint().medium

const query = computed(() => useRoute().query as AlgoritmeQuery)
const pageLength = '10'

let { data } = await algoritmeService.getAll(
  {
    page: '1',
    limit: pageLength,
    ...query.value,
  },
  mapLocaleName(locale.value as 'en' | 'nl')
)

// Refresh data based on the URL query
const loading = ref(false)
watch(query, async () => {
  loading.value = true
  if (data.value) {
    data.value.results = []
  }
  const response = await algoritmeService.getAll(
    query.value,
    mapLocaleName(locale.value as 'en' | 'nl')
  )
  data = response.data
  loading.value = false
})

const page = computed(() => query.value.page || '1')
const totalCount = computed(() => data.value?.total_count || 0)
const algoritmes = computed(() => data.value?.results || [])
const nPages = computed(() => Math.ceil(totalCount.value / +pageLength))

const setPage = (newPage: number) => {
  router.push(
    localePath({ query: { ...query.value, page: newPage.toString() } })
  )
  scroll(0, 0)
}

// default value is true, so that when we search from the homepage the focus is always placed correctly.
const readTitle = ref<boolean>(false)
const newFocusIsRequested = ref<boolean>(false)
const doSearch = (searchtext: string) => {
  const newQuery = {
    ...query.value,
    searchtext: searchtext || undefined,
    page: '1',
  }
  router.push(localePath({ query: newQuery }))

  newFocusIsRequested.value = true
  // In some situations, say the page title again. Everytime state changes, the title is updated and read.
  readTitle.value = !readTitle.value
}

const searchPageTitle = computed(() =>
  query.value.searchtext
    ? t(`foundResults`, { n: totalCount.value }).concat(
        t(`forSearch`, { searchQuery: query.value.searchtext })
      )
    : t(`algoritmeIndex.pageTitle`)
)

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
  padding: 1em !important;
}

.center-with-pagination {
  display: flex;
  align-items: center;
}

.language-disclaimer {
  @media (min-width: 65em) {
    margin: 0em 9em 1em 9em;
  }
  @media (max-width: 65em) {
    margin: 0 0 1em 0;
  }
}
</style>

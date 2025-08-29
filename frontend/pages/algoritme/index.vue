<template>
  <div>
    <LanguageDisclaimer
      v-if="locale !== 'nl'"
      class="language-disclaimer"
      :density="isMobile ? 'compact' : 'default'"
    />
    <SearchBar type="default" @do-search="doSearch" />

    <div class="row container columns no-padding">
      <div class="column-d-3">
        <div>
          <AlgoritmeFilters
            :filter-data="data?.filter_data"
            :selected-filters="data?.selected_filters"
          />
        </div>
      </div>
      <div class="column-d-9">
        <h1 role="status">
          {{ t(`foundResults`, { n: totalCount }) }}
          {{ readTitle ? '&nbsp;' : null }}
        </h1>
        <div class="row container columns no-padding">
          <div class="column-d-6">
            <TablePagination
              v-if="nPages > 1"
              :current-page="+page"
              :page-length="nPages"
              @set-page="(p) => setPage(p)"
            />
          </div>
          <div
            class="column-d-6 center-with-pagination"
            :class="{ 'mobile-center': isMobile, 'align-right': !isMobile }"
          >
            <DownloadDropdown
              :label="t('downloadAllAlgorithms')"
              :action="{
                currentPublished: algoritmeService.downloadAllUrl(
                  mapLocaleName(locale as 'en' | 'nl')
                ),
                allPublished: algoritmeService.downloadAllPublishedVersionsUrl(
                  mapLocaleName(locale as 'en' | 'nl')
                ),
              }"
            />
          </div>
        </div>
        <div v-if="!loading" class="result--list result--list__data">
          <ul>
            <li
              v-for="(algoritme, index) in algoritmes"
              :key="algoritme.algoritme_id"
            >
              <GenericResultCard
                :set-focus="index == 0 && newFocusIsRequested"
                :algoritme="algoritme"
                :query="query"
                @focus-has-been-set="newFocusIsRequested = false"
              >
              </GenericResultCard>
            </li>
          </ul>
        </div>
        <div v-if="loading" class="result--list result--list__data">
          <ul>
            <li v-for="index in 10" :key="index" class="skeleton-card">
              <SkeletonAlgoritmes />
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
import type { AlgoritmeQuery } from '@/types/filter/algoritme'
import { mapLocaleName } from '@/utils'
import algoritmeService from '@/services/algoritme'
import organisationService from '@/services/organisation'
import AlgoritmeFilters from '@/components/algoritme/AlgoritmeFilters.vue'
import SkeletonAlgoritmes from '@/components/skeleton/SkeletonAlgoritmes.vue'

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
const doSearch = async (searchtext: string) => {
  const response = await organisationService.getFullNameOrganisation(
    searchtext,
    mapLocaleName(locale.value as 'nl' | 'en')
  )
  const newQuery = {
    ...(response.data.value
      ? {
          ...query.value,
          organisation: response.data.value?.organisations[0].name,
          searchtext: undefined,
          page: '1',
        }
      : {
          ...query.value,
          searchtext: searchtext || undefined,
          page: '1',
        }),
  }
  router.push(localePath({ query: newQuery }))

  newFocusIsRequested.value = true
  // In some situations, say the page title again. Everytime state changes, the title is updated and read.
  readTitle.value = !readTitle.value
}

const { p } = useTextLoader()
const titleTag = computed(() => {
  const search = query.value.searchtext
  if (search) {
    return search + `${p('Algoritmes-overzicht.title-tag-on-append')}`
  } else {
    return p('Algoritmes-overzicht.title-tag')
  }
})

useSeoMeta({
  description: p('Algoritmes-overzicht.meta-description'),
  ogDescription: p('Algoritmes-overzicht.meta-description'),
})

useHead({ title: titleTag })
providePageTitle({
  title: 'Algoritmes-overzicht.title-tag',
  labelType: 'preditor-index',
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
  justify-content: flex-end;
}

.mobile-center {
  justify-content: center;
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

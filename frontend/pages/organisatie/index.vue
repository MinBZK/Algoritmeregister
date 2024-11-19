<template>
  <div>
    <LanguageDisclaimer
      v-if="locale !== 'nl'"
      class="language-disclaimer"
      :density="isMobile ? 'compact' : 'default'"
    />
    <SearchBar
      type="default"
      placeholder-hint="Zoekbalk.hintOrganisatie"
      keypath="searchExplanationOrganisations"
      :total-count="nOrganisations.data.value"
      @do-search="doSearch"
    />

    <div class="row container columns no-padding">
      <div class="column-d-3">
        <div>
          <OrganisationFilters
            :filter-data="data?.filter_data"
            :selected-filters="data?.selected_filters"
            title="Filters"
          />
        </div>
      </div>
      <div class="column-d-9">
        <h1 role="status">
          {{ t(`foundResultsOrganisations`, { n: totalCount }) }}
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
        </div>
        <div v-if="organisations.length != 0" class="org-result-list">
          <div
            v-for="organisation in organisations"
            :key="organisation.code"
            class="org-result"
          >
            <NuxtLink
              :to="localePath({ path: `/organisatie/${organisation.code}` })"
              class="org-name"
            >
              {{ organisation.name }}</NuxtLink
            >
            <div class="org-count">
              {{ organisation.count ? organisation.count : '-' }}
            </div>
          </div>
        </div>
        <div v-if="loading">
          <div
            v-for="index in 10"
            :key="index"
            class="skeleton-organisations"
          ></div>
        </div>
        <TablePagination
          v-if="nPages > 1"
          :current-page="+page"
          :page-length="nPages"
          @set-page="(p) => setPage(p)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { OrganisationQuery } from '@/types/filter/organisation'
import { mapLocaleName } from '@/utils'
import organisationService from '@/services/organisation'
import OrganisationFilters from '@/components/organisation/OrganisationFilters.vue'

const { t, locale } = useI18n()
const router = useRouter()
const localePath = useLocalePath()
const isMobile = useMobileBreakpoint().medium

const query = computed(() => useRoute().query as OrganisationQuery)
const pageLength = '10'

let { data } = await organisationService.getMany(
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
  const response = await organisationService.getMany(
    query.value,
    mapLocaleName(locale.value as 'en' | 'nl')
  )
  data = response.data
  loading.value = false
})

const nOrganisations = await organisationService.getCountOrganisation(
  mapLocaleName(locale.value as 'en' | 'nl')
)
const page = computed(() => query.value.page || '1')
const totalCount = computed(() => data.value?.total_count || 0)
const organisations = computed(() => data.value?.results || [])
const nPages = computed(() =>
  Math.ceil(totalCount.value / +(query.value.limit || pageLength))
)

const setPage = (newPage: number) => {
  router.push(
    localePath({ query: { ...query.value, page: newPage.toString() } })
  )
  scroll(0, 0)
}

// default value is true, so that when we search from the homepage the focus is always placed correctly.
const doSearch = (searchtext: string) => {
  const newQuery = { searchtext: searchtext || undefined }
  router.push(localePath({ path: '/organisatie', query: newQuery }))
}

const { p } = useTextLoader()
useSeoMeta({
  description: p('Organisatie-overzicht.meta-description'),
  ogDescription: p('Organisatie-overzicht.meta-description'),
})

const titleTag = computed(() => {
  const search = query.value.searchtext
  if (search) {
    return search + `${p('Organisatie-overzicht.title-tag-on-append')}`
  } else {
    return p('Organisatie-overzicht.title-tag')
  }
})

useHead({ title: titleTag })
providePageTitle({
  title: 'Organisatie-overzicht.title-tag',
  labelType: 'preditor-index',
})
</script>

<style scoped lang="scss">
.language-disclaimer {
  @media (min-width: 65em) {
    margin: 0em 9em 1em 9em;
  }
  @media (max-width: 65em) {
    margin: 0 0 1em 0;
  }
}

.org-result-list {
  margin-bottom: 1em;
}

.org-result-list-skeleton {
  min-height: 2em;
}

.org-result {
  margin-left: 0.5em;
  display: flex;
  justify-content: space-between;
}
@media (min-width: 700px) {
  .org-result {
    width: 60%;
  }
}

.org-name:not(:focus) {
  border: 0px !important;
}
</style>

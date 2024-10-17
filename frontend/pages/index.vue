<template>
  <div>
    <LanguageDisclaimer
      v-if="locale !== 'nl'"
      class="language-disclaimer"
      :density="isMobile ? 'compact' : 'default'"
    />
    <div>
      <h1 class="homepage-title">
        {{ t('homepageTitle') }}
      </h1>
    </div>
    <div :class="[isMobile ? 'card-margins-xs' : 'card-margins']">
      <SearchBar @do-search="doSearch" />
      <div class="rows">
        <div class="row">
          <div class="columns">
            <div class="column">
              <FrontpageHighlightedAlgorithms />
            </div>
            <div class="column">
              <FrontpageInfoBlock :html="p('Home.aboutRegister')" />
            </div>
          </div>
        </div>
        <div class="row">
          <div class="columns">
            <div class="column">
              <FrontpageInfoBlock :html="p('Home.about')" class="info-block" />
            </div>
            <div class="column">
              <FrontpageInfoBlock
                :html="p('Home.collaborate')"
                class="info-block"
              />
            </div>
            <div class="column">
              <FrontpageInfoBlock :html="p('Home.toDo')" class="info-block" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMobileBreakpoint } from '~~/composables/mobile'
import organisationService from '@/services/organisation'
const isMobile = useMobileBreakpoint().medium
const { t, locale } = useI18n()
const { p } = useTextLoader()
const localePath = useLocalePath()

const doSearch = async (searchtext: string) => {
  const router = useRouter()
  let query
  if (searchtext) {
    const response = await organisationService.getFullNameOrganisation(
      searchtext,
      mapLocaleName(locale.value as 'nl' | 'en')
    )
    query = {
      ...(response.data.value
        ? {
            organisation: response.data.value?.organisations[0].name,
            page: '1',
          }
        : { searchtext, page: '1' }),
    }
  }
  router.push(
    localePath({
      name: 'algoritme',
      query,
    })
  )
}

useSeoMeta({
  description: p('Home.meta-description'),
  ogDescription: p('Home.meta-description'),
})

useHead({ title: p('Home.title-tag') })
providePageTitle({
  title: 'Home.title-tag',
  labelType: 'preditor-index',
})
</script>

<style scoped lang="scss">
@import '/assets/styles/main.scss';
.btn-dark {
  background-color: $primary;
  color: white;
}

.card-margins {
  padding: 40px 80px 60px 80px;
}

.card-margins-xs {
  padding: 10px 10px 0px 10px;
}

.homepage-title {
  color: $primary-darker;
  text-align: center;
  margin-bottom: 0px;
}

.column {
  margin-bottom: 1em;
}
.row {
  margin-bottom: 0;
}

:deep(.info-block > div) {
  @media (min-width: 65em) {
    min-height: 14em;
  }
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

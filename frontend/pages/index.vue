<template>
  <div>
    <div>
      <h1 class="homepage-title">
        {{ homepageTitle }}
      </h1>
    </div>
    <div :class="[isMobile ? 'card-margins-xs' : 'card-margins']">
      <SearchBar
        :value="searchQuery"
        @input="(v) => (searchQuery = v)"
        @do-search="doSearch"
      />
      <div class="columns">
        <div class="column">
          <HighlightedAlgorithms />
        </div>
        <div class="column">
          <HomePageText />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { stringify } from 'qs'
import { useMobileBreakpoint } from '~~/composables/mobile'
const isMobile = useMobileBreakpoint()
const { t } = useI18n()
const homepageTitle = computed(() => t('homepageTitle'))

const searchQuery = ref('')

const doSearch = () => {
  const router = useRouter()
  const stringifiedQuery = stringify({
    search: searchQuery.value,
  })
  router.push(`/algoritme?q=${stringifiedQuery}`)
}
</script>

<style scoped lang="scss">
@import '/assets/styles/main.scss';
.btn-dark {
  background-color: $primary;
  color: white;
}
.card-margins {
  padding-left: 80px;
  padding-top: 40px;
  padding-right: 80px;
  padding-bottom: 0px !important;
}
.card-margins-xs {
  padding-left: 10px;
  padding-top: 10px;
  padding-right: 10px;
  padding-bottom: 0px;
}
.homepage-title {
  color: $primary-darker;
  text-align: center;
  margin-bottom: 0px;
}
</style>

<template>
  <div>
    <div>
      <h1 class="homepage-title">
        {{ homepageTitle }}
      </h1>
    </div>
    <div :class="[isMobile ? 'card-margins-xs' : 'card-margins']">
      <SearchBar />
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
import { useMobileBreakpoint } from '~~/composables/mobile'
const isMobile = useMobileBreakpoint().medium
const { t } = useI18n()
const homepageTitle = computed(() => t('homepageTitle'))

definePageMeta({
  title: 'Home',
})
providePageTitle({
  title: 'homepageTitle',
  labelType: 'locale-index',
})
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

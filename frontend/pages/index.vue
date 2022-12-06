<template>
  <Page>
    <div>
      <h1 class="homepage-title">
        {{ homepageTitle }}
      </h1>
    </div>
    <v-card elevation="0" color="tertiary">
      <ClientOnly>
        <div :class="[isMobile ? 'card-margins-xs' : 'card-margins']">
          <h4 class="homepage-subtitle">
            {{ homepageSubtitle }}
          </h4>
          <SearchFunction
            v-bind:value="searchQuery"
            @input="(v) => (searchQuery = v)"
            @doSearch="doSearch"
          >
          </SearchFunction>
        </div>
      </ClientOnly>
    </v-card>
  </Page>
</template>

<script setup>
import Page from '@/components/PageWrapper.vue'
import { useI18n } from 'vue-i18n'
import qs from 'qs'
import SearchFunction from '@/components/SearchFunction.vue'
const isMobile = useMobileBreakpoint()

const { t } = useI18n()
const homepageTitle = computed(() => t('homepageTitle'))

const searchQuery = ref('')

const doSearch = () => {
  const router = useRouter()
  const stringifiedQuery = qs.stringify({
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
  padding-bottom: 40px;
}
.card-margins-xs {
  padding-left: 10px;
  padding-top: 10px;
  padding-right: 10px;
  padding-bottom: 10px;
}
.homepage-title {
  color: #154273;
  text-align: center;
  margin-bottom: 50px;
}
</style>

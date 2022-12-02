<template>
  <Page>
    <div>
      <h1 class="homepage-title">
        {{ homepageTitle }}
      </h1>
    </div>
    <SearchFunction
      v-bind:value="searchQuery"
      @input="(v) => (searchQuery = v)"
      @doSearch="doSearch"
    >
    </SearchFunction>
  </Page>
</template>

<script setup>
import Page from '@/components/PageWrapper.vue'
import { useI18n } from 'vue-i18n'
import qs from 'qs'
import SearchFunction from '@/components/SearchFunction.vue'

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
.homepage-title {
  color: #154273;
  text-align: center;
  margin-bottom: 50px;
}
</style>

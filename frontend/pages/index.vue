<template>
  <Page>
    <div>
      <h1 class="homepage-title">
        {{ homepageTitle }}
      </h1>
    </div>
    <v-card elevation="0" color="tertiary">
      <div class="card-margins">
        <h4 class="homepage-subtitle">
          {{ homepageSubtitle }}
        </h4>
        <v-row>
          <SearchFunction
            v-bind:value="searchQuery"
            @input="(v) => (searchQuery = v)"
            @doSearch="doSearch"
          >
          </SearchFunction>
        </v-row>
      </div>
    </v-card>
  </Page>
</template>

<script setup>
import Page from '@/components/PageWrapper.vue'
import { useI18n } from 'vue-i18n'
import qs from 'qs'
import { useDisplay } from 'vuetify'
import SearchFunction from '@/components/SearchFunction.vue'

const { mdAndDown } = useDisplay()
const { t } = useI18n()
const searchHint = computed(() => t('searchHint'))
const homepageTitle = computed(() => t('homepageTitle'))
const homepageSubtitle = computed(() => t('homepageSubtitle'))
const search = computed(() => t('search'))

const searchQuery = ref('')

const showChange = computed(() => {
  console.log('trigger')
  return 1
})
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
.homepage-title {
  color: #154273;
  text-align: center;
  margin-bottom: 50px;
}
.homepage-subtitle {
  color: #154273;
  margin-bottom: 5px;
}
</style>

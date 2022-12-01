<template>
  <Page>
    <v-card elevation="0" color="tertiary">
      <div class="card-margins">
        <v-card-title>
          <h2>
            {{ homepageTitle }}
          </h2></v-card-title
        >
        <v-card-subtitle
          ><h4>
            {{ homepageSubtitle }}
          </h4></v-card-subtitle
        >
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
</style>

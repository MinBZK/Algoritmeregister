<template>
  <Page>
    <v-container>
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
            <v-col :cols="10">
              <v-text-field
                bg-color="white"
                color="primary"
                v-model="searchQuery"
                :label="searchHint"
                variant="outlined"
                @keyup.enter="doSearch"
                prepend-inner-icon="mdi-magnify"
              ></v-text-field></v-col
            ><v-col>
              <ButtonVue :label="search" icon="mdi-magnify" @click="doSearch" />
            </v-col>
          </v-row>
        </div>
      </v-card>
    </v-container>
  </Page>
</template>

<script setup>
import Page from '@/components/PageWrapper.vue'
import { useI18n } from 'vue-i18n'
import qs from 'qs'
import ButtonVue from '@/components/form/Button.vue'

const { t } = useI18n()
const searchHint = computed(() => t('searchHint'))
const homepageTitle = computed(() => t('homepageTitle'))
const homepageSubtitle = computed(() => t('homepageSubtitle'))
const search = computed(() => t('search'))

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
</style>

<template>
  <Page :title="`Homepage`">
    {{ $i18n.locale }}
    <h1>{{ $t('hello', { name: 'vue-i18n' }) }}</h1>
    <v-row>
      <v-col :cols="10">
        <v-text-field
          v-model="searchQuery"
          :label="searchHint"
          variant="outlined"
          @keyup.enter="doSearch"
        ></v-text-field>
      </v-col>
      <v-col :cols="2"
        ><v-btn color="secondary" size="x-large" @click="doSearch"
          >Zoek</v-btn
        ></v-col
      >
    </v-row>
  </Page>
</template>

<script setup>
import Page from '@/components/PageWrapper.vue'
import { useI18n } from 'vue-i18n'
const x = useI18n()
const { t } = x
const searchHint = computed(() => t('searchHint'))

const searchQuery = ref('')

const doSearch = () => {
  const router = useRouter()
  router.push(`/algoritme?q=${searchQuery.value}`)
}
</script>

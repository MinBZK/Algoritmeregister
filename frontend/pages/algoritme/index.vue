<template>
  <Page>
    <v-container>
      <div class="text-field-sheet">
        <v-col>
          <v-text-field
            bg-color="white"
            v-model="searchQuery"
            :label="searchHint"
            variant="outlined"
          >
            <template v-slot:append>
              <v-btn class="btn-dark" block variant="text"> Zoeken </v-btn>
            </template>
          </v-text-field>
        </v-col>
      </div>

      <v-row>
        <v-col :cols="6"
          ><h2>{{ filteredAlgoritmes.length }} resultaten gevonden</h2></v-col
        >
      </v-row>

      <div v-for="algoritme in paginatedAlgoritmes">
        <h3>
          <NuxtLink :to="`/algoritme/${algoritme.id}`">
            {{ algoritme.name }}
          </NuxtLink>
        </h3>
        <v-row>
          <v-col>
            {{ algoritme.description_short }}
          </v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col v-for="sT in summaryTiles" :key="sT.key"
            ><h4>{{ sT.label }}</h4>
            {{ algoritme[sT.key as keyof typeof algoritme] }}</v-col
          >
        </v-row>
        <v-divider></v-divider>
      </div>

      <div v-if="paginatedAlgoritmes.length == 0">
        Geen algoritmes gevonden voor de huidige zoekopdracht.
      </div>

      <v-row
        v-if="filteredAlgoritmes.length > 1"
        align="center"
        justify="center"
      >
        <v-col :cols="6" class="text-grey"
          >{{ filteredAlgoritmes.length }} algoritmes gevonden</v-col
        >
        <v-col :cols="6"
          ><v-pagination v-model="page" :length="nPages"></v-pagination
        ></v-col>
      </v-row>
    </v-container>
  </Page>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Page from '~~/components/PageWrapper.vue'
import algoritmeService from '@/services/algoritme'
import { useI18n } from 'vue-i18n'
import { summaryTiles } from '~~/config/config'
import type { Algoritme } from '@/types/algoritme'

const x = useI18n()
const { t } = x
const searchHint = computed(() => t('searchHint'))

definePageMeta({
  title: 'Algoritmeoverzicht',
})

const { data } = await algoritmeService.getAll()
let algoritmes = ref(data.value as Algoritme[])

const searchQuery = ref(useRoute().query.q || '')

const filteredAlgoritmes = computed(() =>
  algoritmes.value.filter((algoritme) => {
    const algoritmeName = algoritme.name
    const searchQueryString = String(searchQuery.value)
    const allowed =
      searchQueryString.length > 0 && typeof algoritmeName === 'string'
        ? algoritmeName.toLowerCase().includes(searchQueryString.toLowerCase())
        : true
    return allowed
  })
)

const page = ref(1)
const pageLength = 10
const nPages = computed(() =>
  Math.ceil(filteredAlgoritmes.value.length / pageLength)
)
const paginatedAlgoritmes = computed(() =>
  filteredAlgoritmes.value.slice(
    (page.value - 1) * pageLength,
    page.value * pageLength
  )
)

watch(searchQuery, () => {
  page.value = 1
})
</script>

<style scoped lang="scss">
@import '/assets/styles/main.scss';
.v-divider {
  margin: 1em 0;
}
.text-field-sheet {
  background-color: $quaternary;
}
.btn-dark {
  background-color: $primary;
  color: white;
}
</style>

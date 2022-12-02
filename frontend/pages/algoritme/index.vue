<template>
  <Page>
    <SearchFunction
      v-bind:value="searchQuery"
      @input="(v) => (searchQuery = v)"
    >
    </SearchFunction>
    <v-row>
      <v-col :cols="useMobile ? 12 : 3">
        <AlgoritmeFilters :aggregatedAlgoritmes="aggregatedAlgoritmes" />
      </v-col>

      <v-col>
        <v-row>
          <v-col
            ><h2>
              {{ $t(`foundResults`, { n: filteredAlgoritmes.length }) }}
            </h2></v-col
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
          <v-row class="mt-3">
            <v-col v-for="sT in summaryTiles"
              ><h4>
                {{ $t(`algorithmProperties.algemeneInformatie.${sT}.label`) }}
              </h4>
              {{ algoritme[sT as keyof typeof algoritme] }}</v-col
            >
          </v-row>
          <v-divider></v-divider>
        </div>

        <div v-if="paginatedAlgoritmes.length == 0">
          {{ $t('noResults') }}
        </div>

        <v-row
          v-if="filteredAlgoritmes.length > 1"
          align="center"
          justify="center"
        >
          <v-col :cols="6" class="text-grey"
            >{{ $t(`foundResults`, { n: filteredAlgoritmes.length }) }}
          </v-col>
          <v-col :cols="6"
            ><v-pagination
              v-if="nPages > 1"
              v-model="page"
              :length="nPages"
            ></v-pagination
          ></v-col>
        </v-row>
      </v-col>
    </v-row>
  </Page>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Page from '~~/components/PageWrapper.vue'
import algoritmeService from '@/services/algoritme'
import { useI18n } from 'vue-i18n'
import { summaryTiles } from '@/config/config'
import type {
  Algoritme,
  AggregatedAlgoritmes,
  AlgoritmeFilter,
} from '@/types/algoritme'
import AlgoritmeFilters from '@/components/algoritme/AlgoritmeFilters.vue'
import ButtonVue from '@/components/form/Button.vue'
import { useDisplay } from 'vuetify'

const { mdAndDown } = useDisplay()

const useMobile = ref(mdAndDown)

const { t } = useI18n()
const searchHint = computed(() => t('searchHint'))
const search = computed(() => t('search'))

definePageMeta({
  title: 'Algoritmeoverzicht',
})

const parsedQuery = computed(() => useRouteQuery())
const searchQuery = ref((parsedQuery.value.search || '') as string)
const parsedFilters = computed(
  () => parsedQuery.value.filters as AlgoritmeFilter[]
)

const { data } = await algoritmeService.getAll()
let algoritmes = ref(data.value as Algoritme[])

const filteredAlgoritmes = computed(() => {
  const searchQueryString = String(searchQuery.value)

  return algoritmes.value.filter((algoritme) => {
    const includedSearchFields = ['organization', 'name', 'description_short']

    const allowedBySearch =
      searchQueryString.length > 0
        ? includedSearchFields
            .map((field) => {
              const value = algoritme[field as keyof typeof algoritme]
              return value
                ? value.toLowerCase().includes(searchQueryString.toLowerCase())
                : false
            })
            .some((v) => v)
        : true

    const allowedByQueryFilters = (parsedFilters.value || [])
      .map(
        ({ attribute, value }) =>
          algoritme[attribute as keyof Algoritme] == value
      )
      .every((v) => v)

    return allowedByQueryFilters && allowedBySearch
  })
})

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

const aggregatedAlgoritmes = computed(() => {
  const groupOnAttributes = ['organization', 'type']
  const result: AggregatedAlgoritmes[] = groupOnAttributes.map(
    (aggregationAttribute) => {
      return {
        aggregationAttribute,
        aggregationType: 'count',
        aggregatedValues: filteredAlgoritmes.value.reduce((obj, algoritme) => {
          const value = algoritme[aggregationAttribute as keyof Algoritme]
          if (obj[value]) {
            obj[value] = obj[value] + 1
          } else {
            obj[value] = 1
          }
          return obj
        }, {} as Record<string, number>),
      }
    }
  )
  return result
})

watch(searchQuery, () => {
  page.value = 1
})

watch(
  mdAndDown,
  () => {
    useMobile.value = mdAndDown.value
  },
  { immediate: true }
)
</script>

<style scoped lang="scss">
@import '/assets/styles/main.scss';
.v-divider {
  margin: 1em 0;
}
.text-field-sheet {
  background-color: $quaternary;
}
</style>

<template>
  <Page :title="title">
    <p v-for="o in algoritme.omschrijving" :key="o">
      {{ o }}
    </p>
    <v-row class="mt-5">
      <v-col v-for="sT in summaryTiles" :key="sT.key"
        ><h4>{{ sT.label }}</h4>
        {{ algoritme[sT.key] }}</v-col
      >
    </v-row>

    <v-expansion-panels variant="default" class="mt-5">
      <v-expansion-panel
        v-for="i in 3"
        :key="i"
        title="Title"
        elevation="1"
        text="Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi, ratione debitis quis est labore voluptatibus! Eaque cupiditate minima"
        expand-icon="mdi-menu-down"
      >
      </v-expansion-panel>
    </v-expansion-panels>
  </Page>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Page from '~~/components/PageWrapper.vue'
import algoritmeService from '@/services/algoritme'

const route = useRoute()
const id = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
const algoritme: { [key: string]: any } = await algoritmeService.getOne(id)
const title = computed(() => (algoritme?.value ? algoritme.value['naam'] : ''))

type SummaryTile = {
  label: string
  key: string
}
const summaryTiles: SummaryTile[] = [
  {
    label: 'Organisatie',
    key: 'ministerie_afkorting',
  },
  {
    label: 'Status',
    key: 'status_omschrijving',
  },
]

definePageMeta({
  title: 'Algoritme details',
})
</script>

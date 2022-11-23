<template>
  <Page>
    <v-text-field
      v-model="searchQuery"
      label="Zoek algoritme"
      variant="outlined"
    ></v-text-field>

    <!-- <v-row align="center" justify="center">
      <v-col :cols="6" class="text-grey"
        >{{ filteredAlgoritmes.length }} algoritmes gevonden</v-col
      >
      <v-col :cols="6">
        <v-pagination
          v-if="paginatedAlgoritmes.length > 0"
          v-model="page"
          :length="nPages"
        ></v-pagination
      ></v-col>
    </v-row> -->

    <div v-for="algoritme in paginatedAlgoritmes" :key="algoritme[keys.id]">
      <h3>
        <NuxtLink :to="`/algoritme/${algoritme[keys.id]}`">
          {{ algoritme[keys.name] }}
        </NuxtLink>
      </h3>
      <p>
        {{ algoritme[keys.description][0] }}
      </p>
      <v-divider></v-divider>
    </div>

    <div v-if="paginatedAlgoritmes.length == 0">
      Geen algoritmes gevonden voor de huidige zoekopdracht.
    </div>

    <v-row v-if="filteredAlgoritmes.length > 1" align="center" justify="center">
      <v-col :cols="6" class="text-grey"
        >{{ filteredAlgoritmes.length }} algoritmes gevonden</v-col
      >
      <v-col :cols="6"
        ><v-pagination v-model="page" :length="nPages"></v-pagination
      ></v-col>
    </v-row>
  </Page>
</template>

<script setup>
import { computed } from 'vue'
import Page from '~~/components/PageWrapper.vue'
import algoritmeService from '@/services/algoritme'

definePageMeta({
  title: 'Algoritmeoverzicht',
})

const keys = {
  id: 'project_id',
  name: 'naam',
  description: 'omschrijving',
}

let algoritmes = ref([])
algoritmes = await algoritmeService.getAll()

const searchQuery = ref(useRoute().query.q || '')

const filteredAlgoritmes = computed(() =>
  algoritmes.value.filter((a) => {
    const algoritmeName = a[keys.name]
    const allowed =
      searchQuery.value.length > 0 && typeof algoritmeName === 'string'
        ? algoritmeName.toLowerCase().includes(searchQuery.value.toLowerCase())
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

<style>
.v-divider {
  margin: 1em 0;
}
</style>

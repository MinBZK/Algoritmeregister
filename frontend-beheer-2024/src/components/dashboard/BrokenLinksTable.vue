<template>
  <h1 class="text-h5 px-0">
    Gebroken Links
  </h1>
  <p class="text-body-1 py-3">
    Hier wordt per dag getoond hoeveel verwijzingen in gepubliceerde
    algoritmebeschrijvingen voorkomen welke niet (meer) werken of waarvan de
    reactietijd te langzaam is (meer dan 5 seconden). Deze controle is in
    ontwikkeling. Het is mogelijk dat wel-werkende verwijzingen onterecht
    gerapporteerd worden.
  </p>
  <v-row>
    <v-col>
      <v-data-table
        items-per-page="10"
        :headers="headers"
        :items="brokenLinksResults"
      >
        <template #item.create_dt="item">
          {{ formatDate(item!.value) }}
        </template>
        <template #item.lars="item">
          <a
            :href="`https://algoritmes.overheid.nl/nl/algoritme/${item!.value}`"
            target="_blank"
            rel="noopener noreferrer"
          >{{ item!.value }}</a>
        </template>
        <template #item.broken_link="props">
          <ul class="remove-bullet-point-list">
            <li v-for="(link, index) in props!.item.broken_links" :key="index">
              <a
                :href="formatLink(link[0])"
                target="_blank"
                rel="noopener noreferrer"
              >
                {{ link[0] }}
              </a>
            </li>
          </ul>
        </template>
        <template #item.code="props">
          <ul class="remove-bullet-point-list">
            <li v-for="(link, index) in props!.item.broken_links" :key="index">
              {{ link[1] }}
            </li>
          </ul>
        </template>
      </v-data-table>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { getBrokenLinks } from '@/services/brokenlinks'
import type { BrokenLink } from '@/types/brokenlink'
import { formatDate } from '@/utils/datetime'
import { ref } from 'vue'

const headers = [
  { title: 'Algoritme', key: 'lars', width: '5%' },
  { title: 'Organisatie', key: 'organisation', width: '15%' },
  { title: 'Gebroken link', key: 'broken_link' },
  { title: 'Code', key: 'code', width: '5%' },
  { title: 'Datum', key: 'create_dt', sortable: false, width: '10%' },
]

const brokenLinksResults = ref<BrokenLink[]>([])
const retrieveBrokenLinks = async () => {
  const result = await getBrokenLinks()
  brokenLinksResults.value = result.data
}
retrieveBrokenLinks()

const formatLink = (link: string) => {
  if (!link.startsWith('http://') && !link.startsWith('https://')) {
    return `http://${link}`
  }
  return link
}
</script>

<style scoped lang="scss">
.remove-bullet-point-list {
  list-style-type: none;
}

.table {
  width: 100%;
  display: block;
  overflow-x: auto;
  white-space: nowrap;
}

.table td {
  word-wrap: break-word;
}

.blue-bg {
  background-color: #e5f1f9;
}
</style>

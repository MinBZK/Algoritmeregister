<template>
  <Page :title="title">
    <v-container>
      <div class="text-field-sheet">
        <v-col>
          <NuxtLink to="/algoritme"> terug </NuxtLink>
        </v-col>
      </div>

      <h2>
        {{ algoritme[keys.name] }}
      </h2>
      <v-row>
        <v-col>
          {{ algoritme[keys.description] }}
        </v-col>
      </v-row>

      <p v-for="o in algoritme.omschrijving" :key="o">
        {{ o }}
      </p>
      <v-row class="mt-5">
        <v-col v-for="sT in summaryTiles"
          ><h4>{{ sT.label }}</h4>
          {{ algoritme[sT.key] }}</v-col
        >
      </v-row>
      <v-expansion-panels variant="default" class="mt-5">
        <v-expansion-panel
          v-for="subtable in expansionContent"
          :title="subtable.label"
          elevation="1"
          expand-icon="mdi-menu-down"
        >
          <v-expansion-panel-text>
            <v-row v-for="content in getExpansionContent(subtable.key)">
              <v-col>
                <p><b> some text </b></p>
                <br />
                <p color="grey"><i> some explanation </i></p>
                <br />
                <p>{{ content }}</p>
              </v-col>
              <v-divider></v-divider>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-container>
  </Page>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Page from '~~/components/PageWrapper.vue'
import algoritmeService from '@/services/algoritme'
import { summaryTiles, keys } from '~~/config'

const route = useRoute()
const id = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
const algoritme: { [key: string]: any } = await algoritmeService.getOne(id)
const title = computed(() => (algoritme?.value ? algoritme.value['naam'] : ''))

function getExpansionContent(key: string) {
  if (key == '') {
    return algoritme.value.filter((a: any) => {
      console.log(a)
      return true
    })
  }
  return algoritme.value
}
const expansionContent = computed(() => {
  return [
    {
      label: 'Algemene informatie',
      key: '',
    },
    {
      label: 'Inzet',
      key: 'inzet_entity',
    },
    {
      label: 'Toepassing',
      key: 'inzet_entity',
    },
    {
      label: 'Toezicht',
      key: 'inzet_entity',
    },
    {
      label: 'Juridisch',
      key: 'inzet_entity',
    },
    {
      label: 'Metadata',
      key: 'inzet_entity',
    },
  ]
})

definePageMeta({
  title: 'Algoritme details',
})
</script>

<style scoped lang="scss">
.text-field-sheet {
  background-color: $quaternary;
}
</style>

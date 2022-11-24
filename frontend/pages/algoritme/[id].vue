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
      {{ example }}
      <v-expansion-panels variant="default" class="mt-5">
        <v-expansion-panel
          bg-color="quaternary"
          v-for="subtable in algorithmProperties"
          :title="subtable.label"
          elevation="1"
          expand-icon="mdi-menu-down"
        >
          <v-expansion-panel-text>
            <v-row v-for="content in subtable.content">
              <v-col>
                <p>
                  <b> {{ content.label }} </b>
                </p>
                <br />
                <p color="grey">
                  <i> {{ content.description }} </i>
                </p>
                <br />
                <p>{{ content.value }}</p>
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
import { useI18n } from 'vue-i18n'

const route = useRoute()
const id = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
const algoritme: { [key: string]: any } = await algoritmeService.getOne(id)
const title = computed(() => (algoritme?.value ? algoritme.value['naam'] : ''))

const { t } = useI18n()
const example = computed(() => t(`algorithmProperties.inzet.goal.label`))

const filteredData = computed(() => {
  const nestedData = Object.fromEntries(
    Object.entries(algoritme.value).filter(([k, v]) => typeof v == 'object')
  )
  const algemeneInformatie = Object.fromEntries(
    Object.entries(algoritme.value).filter(([k, v]) => typeof v != 'object')
  )
  console.log(algemeneInformatie)
  nestedData['algemeneInformatie'] = algemeneInformatie
  console.log(nestedData)
  const filtered = algoritme.value
  return filtered
})

const algorithmProperties = computed(() => {
  // This property uses nicely ordered data from database (without excluded keys) and the translation data from i18n
  const result = expansionConfig.map((row) => {
    return {
      label: row.label,
      content: Object.entries(filteredData.value[row.key]).map(([k, v]) => {
        return {
          label: t(`algorithmProperties.${row.key}.${k}.label`),
          description: t(`algorithmProperties.${row.key}.${k}.description`),
          value: v,
        }
      }),
    }
  })
  return result
})

const excludedData = ['id', 'algoritme_id']
const expansionConfig = [
  {
    label: 'Inzet',
    key: 'inzet',
  },
  // {
  //   label: 'Toepassing',
  //   key: 'toepassing',
  // },
  // {
  //   label: 'Toezicht',
  //   key: 'toezicht',
  // },
  // {
  //   label: 'Juridisch',
  //   key: 'juridisch',
  // },
  // {
  //   label: 'Metadata',
  //   key: 'metadata',
  // },
]

definePageMeta({
  title: 'Algoritme details',
})
</script>

<style scoped lang="scss">
.text-field-sheet {
  background-color: $quaternary;
}
</style>

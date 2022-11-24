<template>
  <Page :title="title">
    <v-container>
      <div class="text-field-sheet">
        <v-col>
          <NuxtLink to="/algoritme"> terug </NuxtLink>
        </v-col>
      </div>

      <h2>
        {{ algoritme.name }}
      </h2>
      <v-row>
        <v-col>
          {{ algoritme.description_short }}
        </v-col>
      </v-row>

      <v-row class="mt-5">
        <v-col v-for="sT in summaryTiles"
          ><h4>{{ sT.label }}</h4>
          {{ algoritme[sT.key as keyof typeof algoritme] }}</v-col
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
import type { Algoritme } from '~~/types/algoritme'

// get data
const route = useRoute()
const id = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
// const algoritme: { [key: string]: any } = await algoritmeService.getOne(id)

const { data } = await algoritmeService.getOne(id)
let algoritme = ref(data.value as Algoritme)

const title = computed(() => algoritme?.value.name)
const excludedData = ['id', 'algoritme_id']

const { t } = useI18n()
const example = computed(() => t(`algorithmProperties.inzet.goal.label`))

const filteredData = computed(() => {
  const nestedData = Object.fromEntries(
    Object.entries(algoritme.value).filter(([k, v]) => typeof v == 'object')
  )
  nestedData['algemeneInformatie'] = Object.fromEntries(
    Object.entries(algoritme.value).filter(([k, v]) => {
      console.log(!excludedData.includes(k))
      return typeof v != 'object'
    })
  )
  const result = Object.fromEntries(
    Object.entries(nestedData).map((x: [string, any]) => {
      return [
        x[0],
        Object.fromEntries(
          Object.entries(x[1]).filter(([k, v]) => !excludedData.includes(k))
        ),
      ]
    })
  )
  return result
})

const algorithmProperties = computed(() => {
  // This property uses nicely ordered data from database (without excluded keys) and the translation data from i18n
  const result = expansionConfig.map((row) => {
    // console.log('properties', filteredData.value['inzet'])
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

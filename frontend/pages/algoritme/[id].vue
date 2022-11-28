<template>
  <Page>
    <div class="text-field-sheet">
      <v-col>
        <NuxtLink to="/algoritme"> {{ i18nGoBack }} </NuxtLink>
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
    <!-- {{ structuredProperties }} -->
    <v-row class="mt-3">
      <v-col v-for="sT in summaryTiles"
        ><h4>
          {{ $t(`algorithmProperties.algemeneInformatie.${sT}.label`) }}
        </h4>
        {{ algoritme[sT as keyof typeof algoritme] }}</v-col
      >
    </v-row>
    <v-row class="mt-8">
      <v-expansion-panels variant="default">
        <v-expansion-panel
          bg-color="quaternary"
          v-for="groupedProperty in structuredProperties"
          :title="groupedProperty.attributeGroupKeyLabel"
          elevation="1"
          expand-icon="mdi-menu-down"
        >
          <v-expansion-panel-text>
            <v-row v-for="property in groupedProperty.properties">
              <v-col>
                <p class="mt-2">
                  <b> {{ property.attributeKeyLabel }} </b>
                </p>
                <p class="mb-1">
                  <i> {{ property.attributeKeyDescription }} </i>
                </p>
                <p class="mb-1">
                  {{ property.attributeValue || t('Ontbreekt') }}
                </p>
              </v-col>
              <v-divider></v-divider>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-row>
    <div>''</div>
  </Page>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Page from '~~/components/PageWrapper.vue'
import algoritmeService from '@/services/algoritme'
import { summaryTiles, keys } from '~~/config/config'
import { useI18n } from 'vue-i18n'
import type { Algoritme } from '~~/types/algoritme'
import requiredFields from '~~/config/fields.json'
import { assertJSXAttribute } from '@babel/types'

// get data
const route = useRoute()
const id = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id

const { data } = await algoritmeService.getOne(id)
let algoritme = ref(data.value as Algoritme)

const enrichedAlgoritme = computed(() => {
  // add algemene informatie as object
  const groupKey = 'algemeneInformatie'
  const nestedKeys = [
    'name',
    'organization',
    'department',
    'description_short',
    'type',
    'category',
    'website',
    'status',
    'id',
  ]
  const group = nestedKeys.reduce((obj, key) => {
    obj[key as keyof Algoritme] = algoritme.value[key as keyof Algoritme]
    return obj
  }, {} as Algoritme)

  return { [groupKey]: group, ...algoritme.value }
})

// const title = computed(() => algoritme?.value.name)

const { t } = useI18n()
const i18nGoBack = computed(() => t(`goBack`))

const structuredProperties = computed(() => {
  const algoritme = enrichedAlgoritme
  const keysWithObjectValues = Object.keys(algoritme.value).filter(
    (key) =>
      typeof algoritme.value[key as keyof typeof algoritme.value] == 'object'
  )
  const excludedKeys = ['id', 'algoritme_id']
  return keysWithObjectValues.map((attributeGroupKey) => {
    return {
      attributeGroupKey,
      attributeGroupKeyLabel:
        t(`algorithmProperties.${attributeGroupKey}.label`) ||
        attributeGroupKey,
      properties: Object.entries(
        algoritme.value[attributeGroupKey as keyof typeof algoritme.value]
      )
        .filter(([key]) => !excludedKeys.includes(key))
        .map(([key, value]) => {
          const parsedValue =
            typeof value != 'boolean'
              ? value
              : value == true
              ? t(`yes`)
              : t(`no`)
          return {
            attributeKey: key,
            attributeValue: parsedValue,
            attributeKeyDescription: t(
              `algorithmProperties.${attributeGroupKey}.${key}.description`
            ),
            attributeKeyLabel: t(
              `algorithmProperties.${attributeGroupKey}.${key}.label`
            ),
          }
        })
        .filter((attribute) => {
          console.log(
            requiredFields.properties[
              attribute.attributeKey as keyof typeof requiredFields.properties
            ]?.required,
            attribute.attributeKey
          )
          return (
            requiredFields.properties[
              attribute.attributeKey as keyof typeof requiredFields.properties
            ]?.required == true || !!attribute.attributeValue
          )
        }),
    }
  })
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

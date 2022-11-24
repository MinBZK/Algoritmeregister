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
      <v-expansion-panels variant="default" class="mt-5">
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
                  {{ property.attributeValue }}
                </p>
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

const { data } = await algoritmeService.getOne(id)
let algoritme = ref(data.value as Algoritme)

const title = computed(() => algoritme?.value.name)

const { t } = useI18n()
const example = computed(() => t(`algorithmProperties.inzet.goal.label`))

const structuredProperties = computed(() => {
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
          return {
            attributeKey: key,
            attributeValue: value,
            attributeKeyDescription: t(
              `algorithmProperties.${attributeGroupKey}.${key}.description`
            ),
            attributeKeyLabel: t(
              `algorithmProperties.${attributeGroupKey}.${key}.label`
            ),
          }
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

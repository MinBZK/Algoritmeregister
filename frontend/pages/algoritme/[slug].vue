<template>
  <div>
    <div class="container row">
      <NuxtLink class="link cta__backwards" :to="`/algoritme/`">
        {{ t('goBack') }}
      </NuxtLink>
    </div>
    <div class="container row container--centered">
      <h1>{{ algoritme.name }}</h1>
      <SearchResultCard
        :algoritme="algoritme"
        mode="default"
      ></SearchResultCard>
      <AlgoritmeAccordionRows
        v-if="isMobile"
        :accordion-properties="structuredProperties"
      />
      <AlgoritmeTabsTable
        v-if="!isMobile"
        :tabs-table-properties="structuredProperties"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { Algoritme } from '~~/types/algoritme'
import requiredFields from '~~/config/fields.json'
import algoritmeService from '@/services/algoritme'
import { useMobileBreakpoint } from '~~/composables/mobile'
const { t } = useI18n()

const isMobile = useMobileBreakpoint()

// get data
const route = useRoute()
const slug = Array.isArray(route.params.slug)
  ? route.params.slug[0]
  : route.params.slug

const { setAlgoritme } = useAlgoritme()
const { data } = await algoritmeService.getOne(slug)
const algoritme = ref(data.value as Algoritme)
if (!algoritme.value) {
  throw createError({
    statusCode: 404,
  })
}

setAlgoritme(algoritme.value)

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

// construct the list of data
const structuredProperties = computed(() => {
  const algoritme = enrichedAlgoritme
  const keysWithObjectValues = Object.keys(algoritme.value).filter(
    (key) =>
      typeof algoritme.value[key as keyof typeof algoritme.value] === 'object'
  )
  const excludedKeys = ['id', 'algoritme_id']
  return keysWithObjectValues.map((groupKey) => {
    return {
      groupKey,
      groupKeyLabel: t(`algorithmProperties.${groupKey}.label`) || groupKey,
      properties: Object.entries(
        algoritme.value[groupKey as keyof typeof algoritme.value]
      )
        .filter(([key]) => !excludedKeys.includes(key))
        .map(([key, value]) => {
          const parsedValue =
            typeof value !== 'boolean'
              ? value
              : value === true
              ? t(`yes`)
              : t(`no`)
          return {
            key,
            value: parsedValue,
            keyDescription: t(`algorithmProperties.${key}.description`),
            keyLabel: t(`algorithmProperties.${key}.label`),
          }
        })
        // only show field that are either required or not empty. An empty string is considered empty.
        .filter(
          (attribute) =>
            requiredFields.properties[
              attribute.key as keyof typeof requiredFields.properties
            ]?.required === true || !!attribute.value
        ),
    }
  })
})

definePageMeta({
  title: 'Algoritme details',
})
</script>

<template>
  <div>
    <div class="container row header-width">
      <div class="header-spacing">
        <NuxtLink class="link cta__backwards" :to="localePath(`/algoritme/`)">
          {{ t('goBack') }}
        </NuxtLink>
        <FormOverheidButton
          label="Download dit algoritme (.xlsx)"
          :action="
            algoritmeService.downloadOneUrl(
              data?.lars || '',
              mapLocaleName(locale as 'en' | 'nl')
            )
          "
          :hidden-query="[{ name: 'filetype', value: 'excel' }]"
          :style="'secondary'"
          icon="mdi:download"
        />
      </div>
    </div>
    <div class="container row container--centered">
      <LanguageDisclaimer
        v-if="locale == 'en'"
        class="language-disclaimer"
        :density="isMobile ? 'compact' : 'default'"
      />
      <h1>{{ algoritme.name }}</h1>

      <HeaderCard :algoritme="algoritme"></HeaderCard>
      <AlgoritmeAccordionRows
        v-if="isMobile"
        :accordion-properties="structuredAlgoritme"
      />
      <AlgoritmeTabsTable
        v-if="!isMobile"
        :tabs-table-properties="structuredAlgoritme"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ComputedRef } from 'nuxt/dist/app/compat/capi'
import type { AlgorithmDisplay, Algoritme } from '~~/types/algoritme'
import { AlgorithmIn } from '@/types/apiStandard'
import algoritmeService from '@/services/algoritme'
import { useMobileBreakpoint } from '~~/composables/mobile'
import { objectMap } from '@/utils'
import { tabsGrouping } from '@/types/layout'
import { textVersionMapping } from '~~/config/config'

const { t, locale } = useI18n()
const localePath = useLocalePath()

const isMobile = useMobileBreakpoint().medium

// get data
const route = useRoute()
const lars = Array.isArray(route.params.lars)
  ? route.params.lars[0]
  : route.params.lars

const { setAlgoritme } = useAlgoritme()
const { data } = await algoritmeService.getOne(
  lars,
  mapLocaleName(locale.value as 'en' | 'nl')
)
const algoritme = ref(data.value as Algoritme)
if (!algoritme.value) {
  throw createError({
    statusCode: 404,
    fatal: true,
  })
}
setAlgoritme(algoritme.value)

const columnGrouping = ref<tabsGrouping[]>([])
const getGrouping = async (version: string) => {
  const layoutUrl = '/layouts/v' + version.replace(/\./g, '_') + '.json'
  const fetchResponse = await fetch(layoutUrl)
  const layout = await fetchResponse.json()
  columnGrouping.value = layout.tabsGrouping
}
const apiStandard = ref<AlgorithmIn>()
const getApiStandard = async (version: string) => {
  // Temp, replace with commented code* once aanleverapi is live on production
  const layoutUrl = '/standards/v' + version.replace(/\./g, '_') + '.json'
  const fetchResponse = await fetch(layoutUrl)
  const layout = await fetchResponse.json()
  apiStandard.value = layout.AlgorithmIn.properties

  // // *replace with this commented code
  // await algoritmeService.getApiStandard(version).then((response) => {
  //   apiStandard.value =
  //     response.data.value.components.schemas.AlgorithmIn.properties
  // })
}

onMounted(() => {
  getApiStandard(algoritme.value.standard_version)
  getGrouping(algoritme.value.standard_version)
})

const parsedAlgoritme = computed(() => {
  // Any pre-processing to be done on the data itself, before display.
  return objectMap(algoritme.value, (value: any) => {
    return typeof value !== 'boolean'
      ? value
      : value === true
      ? t(`yes`)
      : t(`no`)
  })
})

const structuredAlgoritme: ComputedRef<AlgorithmDisplay[]> = computed(() => {
  const helpTextVersion = textVersionMapping[algoritme.value.standard_version]

  // Uses the columnGrouping config to map the flat algoritme fields into groups.
  return columnGrouping.value.map((grouping) => {
    const key = grouping.key
    // Builds property list of a single group.
    const properties = grouping.rows
      .map((key) => {
        return {
          key,
          value: parsedAlgoritme.value[key as keyof Algoritme],
          keyDescription: t(
            `algorithmProperties.${helpTextVersion}.${key}.description`
          ),
          keyLabel: t(`algorithmProperties.${helpTextVersion}.${key}.label`),
        }
      })
      // Filters empty and not required fields. An empty string is considered empty.
      .filter((field) => {
        return apiStandard.value
          ? apiStandard.value[field.key].show_always || !!field.value
          : false
      })
    return {
      key,
      keyLabel: t(`algorithmProperties.${helpTextVersion}.headers.${key}`),
      properties,
    }
  })
})

definePageMeta({
  title: 'Algoritme details',
})
useHead({ title: ` ${algoritme.value.name} - ${algoritme.value.organization}` })
providePageTitle({
  title: ` ${algoritme.value.name} - ${algoritme.value.organization}`,
  labelType: 'page-title',
})
</script>

<style lang="scss">
.language-disclaimer {
  @media (min-width: 65em) {
    margin: 0em 2em 1em 2em;
  }
  @media (max-width: 65em) {
    margin: 0 0 1em 0;
  }
}

.header-width {
  max-width: 49em;
  width: 100%;
}

.header-spacing {
  width: inherit;
  display: inline-flex;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 40em) {
  .header-spacing {
    flex-direction: column !important;
    row-gap: 0.5em;
  }
  .header-width {
    width: auto;
  }
}
</style>

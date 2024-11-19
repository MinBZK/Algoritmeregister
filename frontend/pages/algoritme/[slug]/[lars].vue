<template>
  <div>
    <div class="container row header-width">
      <div class="header-spacing">
        <NuxtLink class="link cta__backwards" :to="localePath(`/algoritme/`)">
          {{ t('goBack') }}
        </NuxtLink>
        <DownloadDropdown
          :label="t('downloadThisAlgorithm')"
          :action="
            algoritmeService.downloadOneUrl(
              algoritme?.lars || '',
              mapLocaleName(locale as 'en' | 'nl')
            )
          "
        />
      </div>
    </div>
    <div class="container row container--centered">
      <LanguageDisclaimer
        v-if="locale !== 'nl'"
        class="language-disclaimer"
        :density="isMobile ? 'compact' : 'default'"
      />
      <div class="header-card">
        <h1>{{ algoritme!.name }}</h1>
        <GenericResultCard :algoritme="algoritme!"></GenericResultCard>
      </div>
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
import type { AlgorithmDisplay, Algoritme } from '~~/types/algoritme'
import type { AlgorithmIn } from '@/types/apiStandard'
import algoritmeService from '@/services/algoritme'
import { useMobileBreakpoint } from '~~/composables/mobile'
import { objectMap, mapLocaleName } from '@/utils'
import type { tabsGrouping } from '@/types/layout'
import { textVersionMapping } from '~~/config/config'
import type { LanguageCode } from '@/types/preditor'

const { t, locale } = useI18n()
const localePath = useLocalePath()

const isMobile = useMobileBreakpoint().medium

// get data
const route = useRoute()
const lars = Array.isArray(route.params.lars)
  ? route.params.lars[0]
  : route.params.lars

const { getAndSetAlgoritme, algoritme } = useAlgoritme()

if (!algoritme.value) {
  await getAndSetAlgoritme(lars, locale.value as LanguageCode)
}

if (!algoritme.value) {
  throw createError({
    statusCode: 404,
    fatal: true,
  })
}

const columnGrouping = ref<tabsGrouping[]>([])
const getGrouping = (version: string) => {
  const layoutVersion = 'v' + version.replace(/\./g, '_')
  const layout = getLayoutConfig(layoutVersion)
  columnGrouping.value = layout.tabsGrouping
}
const apiStandard = ref<AlgorithmIn>()
const getApiStandard = (version: string) => {
  // Temp, replace with commented code* once aanleverapi is live on production
  const standardVersion = 'v' + version.replace(/\./g, '_')
  const layout = getStandardConfig(standardVersion)
  apiStandard.value = layout.AlgorithmIn.properties

  // // *replace with this commented code
  // await algoritmeService.getApiStandard(version).then((response) => {
  //   apiStandard.value =
  //     response.data.value.components.schemas.AlgorithmIn.properties
  // })
}

getGrouping(algoritme.value.standard_version)
getApiStandard(algoritme.value.standard_version)

const parsedAlgoritme = computed(() => {
  // Any pre-processing to be done on the data itself, before display.
  return objectMap(algoritme.value!, (value: any) => {
    return typeof value !== 'boolean'
      ? value
      : value === true
        ? t(`yes`)
        : t(`no`)
  })
})

const structuredAlgoritme: ComputedRef<AlgorithmDisplay[]> = computed(() => {
  const helpTextVersion = textVersionMapping[algoritme.value!.standard_version]

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

const length = 157
const truncatedDescription = computed(() => {
  const truncatedString = (
    algoritme.value?.description_short as string | null
  )?.substring(0, length)
  return truncatedString === algoritme.value?.description_short
    ? truncatedString
    : truncatedString + '...'
})

useSeoMeta({
  description: truncatedDescription.value,
  ogDescription: truncatedDescription.value,
})

useHead({ title: `${algoritme.value.name} - ${algoritme.value.organization}` })
providePageTitle({
  title: `${algoritme.value.name} - ${algoritme.value.organization}`,
  labelType: 'plain-text',
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

.header-card {
  border: 9px solid #e5f1f9;
  padding: 1em;
}

h1 {
  hyphens: auto;
}
</style>

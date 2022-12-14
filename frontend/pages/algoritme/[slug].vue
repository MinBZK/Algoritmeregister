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
        :key="algoritme.slug"
        :algoritme="algoritme"
        mode="default"
      ></SearchResultCard>
      <div class="accordion" v-if="isMobile">
        <AlgoritmeSlugAccordionRow
          v-for="(p, index) in structuredProperties"
          :key="p.attributeGroupKey"
          :group-props="p"
          v-bind:toggled="toggledRows[index]"
          @toggle-this-row="toggleRows(index)"
        />
      </div>

      <div
        v-if="!isMobile && tabHeaders"
        class="tabs"
        data-decorator="init-tabs"
      >
        <ul class="tabs__list" role="tablist">
          <AlgoritmeSlugTab
            v-for="(p, index) in structuredProperties"
            :key="p.attributeGroupKey"
            :tab-props="p"
            :index="index"
            :toggled="toggledRows[index]"
            role="presentation"
            @navigate-tab="(v) => navigateTab(v, index)"
            @click="toggleRows(index)"
          />
        </ul>

        <table class="table__data-overview">
          <tbody>
            <tr
              v-for="property in activeAttributeProperties"
              :key="property.attributeKey"
            >
              <th scope="row">
                {{ property.attributeKeyLabel }}
                <span
                  class="question-mark"
                  role="button"
                  tabindex="0"
                  @click="toggleKey(property.attributeKey)"
                  @keydown.enter="toggleKey(property.attributeKey)"
                ></span>
                <p v-if="isKeyToggled(property.attributeKey)">
                  <i>
                    <ParseUrl>
                      {{
                        `${property.attributeKeyDescription || t('Ontbreekt')}`
                      }}
                    </ParseUrl>
                  </i>
                </p>
              </th>

              <td>
                <ParseUrl :key="property.attributeValue">
                  {{ property.attributeValue || t('Ontbreekt') }}
                </ParseUrl>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useActiveElement } from '@vueuse/core'
import type { Algoritme } from '~~/types/algoritme'
import requiredFields from '~~/config/fields.json'
import algoritmeService from '@/services/algoritme'
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

const activeAttributeKey = ref('')
const activeAttributeProperties = computed(() => {
  return structuredProperties.value.filter((groupedProperty) => {
    return groupedProperty.attributeGroupKey === activeAttributeKey.value
  })[0]?.properties
})

// Handle toggling of description of the keys
const keyToggles = ref<string[]>([])
const toggleKey = (key: string) => {
  if (keyToggles.value.includes(key)) {
    keyToggles.value = keyToggles.value.filter((e: any) => e !== key)
  } else {
    keyToggles.value.push(key)
  }
}

const isKeyToggled = (key: string) => keyToggles.value.includes(key)

const clearToggledKeys = () => (keyToggles.value = [])

// construct the list of data
const structuredProperties = computed(() => {
  const algoritme = enrichedAlgoritme
  const keysWithObjectValues = Object.keys(algoritme.value).filter(
    (key) =>
      typeof algoritme.value[key as keyof typeof algoritme.value] === 'object'
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
            typeof value !== 'boolean'
              ? value
              : value === true
              ? t(`yes`)
              : t(`no`)
          return {
            attributeKey: key,
            attributeValue: parsedValue,
            attributeKeyDescription: t(
              `algorithmProperties.${key}.description`
            ),
            attributeKeyLabel: t(`algorithmProperties.${key}.label`),
          }
        })
        // only show field that are either required or not empty. An empty string is considered empty.
        .filter(
          (attribute) =>
            requiredFields.properties[
              attribute.attributeKey as keyof typeof requiredFields.properties
            ]?.required === true || !!attribute.attributeValue
        ),
    }
  })
})

const activeElement = useActiveElement()

const focusedTabIndex = computed(() => {
  const currentIndexSelected = structuredProperties.value
    .map((sP) => sP.attributeGroupKey)
    .indexOf(activeAttributeKey.value)

  console.log('currentIndexSelected', currentIndexSelected)
  const currentIndexWithFocus = activeElement.value
    ? tabHeaders.value.indexOf(activeElement.value as HTMLAnchorElement)
    : -1

  console.log('currentIndexWithFocus', currentIndexWithFocus)
  const currentIndex =
    currentIndexWithFocus > -1 ? currentIndexWithFocus : currentIndexSelected

  console.log('currentIndex', currentIndex)
  return currentIndex
})

const tabHeaders = ref<HTMLAnchorElement[]>([])
const navigateTab = (increment: number, index: number) => {
  // const newTabHeaderIndex = index + direction
  // console.log(toggledRows.value, index)
  // toggledRows.value = Array(structuredProperties.value.length).fill(false)
  // toggledRows.value[newTabHeaderIndex] = true
  // console.log(toggledRows.value)
  // // tabHeaders.value[newTabHeaderIndex].focus()
  // console.log(focusedTabIndex.value)
  const newIndex = focusedTabIndex.value + increment
  clearToggledKeys()
  if (newIndex >= 0 && newIndex < structuredProperties.value.length) {
    tabHeaders.value[newIndex].focus()
  }
}

const selectTab = () => {
  activeAttributeKey.value =
    structuredProperties.value[focusedTabIndex.value].attributeGroupKey
}

const toggledRows = ref<boolean[]>(
  Array(structuredProperties.value.length).fill(false)
)
const toggleRows = (index: number) => {
  const currentRowToggled = toggledRows.value[index]
  toggledRows.value = Array(structuredProperties.value.length).fill(false)
  toggledRows.value[index] = !currentRowToggled
  return 0
}

definePageMeta({
  title: 'Algoritme details',
})

if (!isMobile.value) {
  activeAttributeKey.value = structuredProperties.value[0].attributeGroupKey
}

watch(
  isMobile,
  (newValue) =>
    // Closes tabs if the screen is becoming smaller.
    (activeAttributeKey.value = newValue
      ? ''
      : structuredProperties.value[0].attributeGroupKey)
)
</script>

<style scoped lang="scss">
.accordion__item__header {
  cursor: pointer;
}

.word-break {
  word-break: break-word;
}

dl.columns--data div {
  padding: 0.5em;
}
.tabs__list a {
  cursor: pointer;
}

.question-mark {
  padding-left: 0;
}

li a:focus {
  box-shadow: 0 0 0 0 #000 !important;
  outline: 0;
  background-color: $grey;
}

li a:link {
  color: red;
}

.well--pageblock {
  padding: 1.5em 10% !important;
}
</style>

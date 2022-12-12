<template>
  <div class="skiplinks container">
    <a href="#content">Direct naar content</a>
  </div>
  <div class="container row">
    <NuxtLink class="link cta__backwards" :to="`/algoritme/`">
      {{ t('goBack') }}
    </NuxtLink>
  </div>
  <div class="container row container--centered">
    <h1>{{ algoritme.name }}</h1>
    <div class="well well--pageblock">
      <!-- <h3>{{ shortDescription }}</h3> -->
      <p>{{ algoritme.description_short || shortDescriptionMissing }}</p>
      <!-- <p>
            <a href="#" class="link link--forward">Alle datasets van deze eigenaar</a>
          </p> -->
      <dl class="dl columns--data">
        <div v-for="sT in summaryTiles">
          <dt>
            {{ $t(`algorithmProperties.algemeneInformatie.${sT}.label`) }}
          </dt>
          <dd>
            <span>{{
              algoritme[sT as keyof typeof algoritme] || t('Ontbreekt')
            }}</span>
          </dd>
        </div>
      </dl>
    </div>
    <div v-if="isMobile" class="accordion" data-decorator="init-accordion">
      <div v-for="(p, index) in structuredProperties" class="accordion__item">
        <div class="accordion__item__header">
          <h3 class="accordion__item__heading">
            <span
              class="accordion__item__header-trigger"
              aria-expanded="false"
              aria-controls="con1"
              id="header1"
              @click="
                ;[toggleAccordion(p.attributeGroupKey), clearToggledKeys()]
              "
            >
              <span
                :class="
                  p.attributeGroupKey == activeAttributeKey
                    ? 'accordion-arrow-up'
                    : 'accordion-arrow-right'
                "
              ></span>
              {{ p.attributeGroupKeyLabel }}
            </span>
          </h3>
        </div>
        <div
          v-if="p.attributeGroupKey == activeAttributeKey"
          v-for="(property, index) in p.properties"
          class="accordion__item__content"
          id="con1"
          role="region"
          aria-labelledby="header1"
        >
          <div>
            <b>
              {{ property.attributeKeyLabel }}
            </b>
            <span
              @click="toggleKey(property.attributeKey)"
              class="question-mark"
            ></span>
          </div>
          <div class="word-break" v-if="isKeyToggled(property.attributeKey)">
            <i
              >{{
                `${explanation}: ${
                  property.attributeKeyDescription || t('Ontbreekt')
                }`
              }}
            </i>
          </div>
          <div class="word-break">
            {{ property.attributeValue || t('Ontbreekt') }}
          </div>
        </div>
      </div>
    </div>

    <div v-if="!isMobile" class="tabs" data-decorator="init-tabs">
      <ul class="tabs__list" role="tablist">
        <li role="presentation" v-for="(p, index) in structuredProperties">
          <a
            @click="activeAttributeKey = p.attributeGroupKey"
            :class="[
              p.attributeGroupKey == activeAttributeKey ? 'is-selected' : '',
            ]"
            role="tab"
            :aria-controls="`panel-${index + 1}`"
            >{{ p.attributeGroupKeyLabel }}</a
          >
        </li>
      </ul>

      <table class="table__data-overview">
        <tbody>
          <tr v-for="(property, index) in activeAttributeProperties">
            <th scope="row">
              {{ property.attributeKeyLabel }}
              <span
                @click="toggleKey(property.attributeKey)"
                class="question-mark"
              ></span>
              <p v-if="isKeyToggled(property.attributeKey)">
                <i>
                  {{
                    `${explanation}: ${
                      property.attributeKeyDescription || t('Ontbreekt')
                    }`
                  }}
                </i>
              </p>
            </th>

            <td>
              {{ property.attributeValue || t('Ontbreekt') }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { summaryTiles } from '~~/config/config'
import { useI18n } from 'vue-i18n'
import type { Algoritme } from '~~/types/algoritme'
import requiredFields from '~~/config/fields.json'
// import algoritmeStore from '@/stores/algoritme'
import algoritmeService from '@/services/algoritme'

const isMobile = useMobileBreakpoint()

// get data
const route = useRoute()
const slug = Array.isArray(route.params.slug)
  ? route.params.slug[0]
  : route.params.slug

// get store
// const store = useAlgoritmeStore()

const { setAlgoritme } = useAlgoritme()
const { data } = await algoritmeService.getOne(slug)
let algoritme = ref(data.value as Algoritme)
setAlgoritme(algoritme.value)

// algoritmeStore.state.currentAlgoritme = algoritme.value
// store.currentAlgoritme = algoritme

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

const { t } = useI18n()
const shortDescriptionMissing = computed(() => t('short-description-missing'))
const explanation = computed(() => t('explanation'))

let activeAttributeKey = ref('')
const activeAttributeProperties = computed(() => {
  return structuredProperties.value.filter((groupedProperty) => {
    return groupedProperty.attributeGroupKey == activeAttributeKey.value
  })[0]?.properties
})

// Handle accordion
const toggleAccordion = (key: string) =>
  (activeAttributeKey.value = activeAttributeKey.value == key ? '' : key)

// Handle toggling of description of the keys
let keyToggles = ref<string[]>([])
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
        // only show field that are either required or not empty. An empty string is considered empty.
        .filter(
          (attribute) =>
            requiredFields.properties[
              attribute.attributeKey as keyof typeof requiredFields.properties
            ]?.required == true || !!attribute.attributeValue
        ),
    }
  })
})

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
</style>

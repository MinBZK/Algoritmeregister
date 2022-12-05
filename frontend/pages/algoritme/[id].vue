
<!-- <template>
  <Page>
    <h2>
      {{ algoritme.name }}
    </h2>
    <v-row>
      <v-col>
        {{ algoritme.description_short }}
      </v-col>
    </v-row>
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
                  <h4> {{ property.attributeKeyLabel }} </h4>
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
</template> -->

<template>
  <Page>
    <ClientOnly>
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
          <p> {{ algoritme.description_short || shortDescriptionMissing }}</p>
          <!-- <p>
            <a href="#" class="link link--forward">Alle datasets van deze eigenaar</a>
          </p> -->
          <dl class="dl columns--data">
            <div v-for="sT in summaryTiles">
              <dt>
                {{ $t(`algorithmProperties.algemeneInformatie.${sT}.label`) }}
              </dt>
              <dd>
                <span class="icon icon--housing">{{
                    algoritme[sT as keyof typeof algoritme] || t('Ontbreekt')
                }}</span>
              </dd>
            </div>
          </dl>
        </div>
        <div class="tabs" data-decorator="init-tabs">
          <ul class="tabs__list" role="tablist">
            <li role="presentation" v-for="(p, index) in structuredProperties">
              <span @click="activeAttributeKey = p.attributeGroupKey" :class="[
                p.attributeGroupKey == activeAttributeKey ? 'is-selected' : '',
              ]" role="tab" :aria-controls="`panel-${index + 1}`">{{ p.attributeGroupKeyLabel }}</span>
            </li>
          </ul>
          <div class="tabs__panels">
            <div v-for="(property, index) in activeAttributeProperties" role="tabpanel"
              :aria-labelledby="`tab-${index + 1}`">
              <p class="mt-2">
              <h4> {{ property.attributeKeyLabel }} </h4>
              </p>
              <p class="mb-1">
                <i> {{ property.attributeKeyDescription }} </i>
              </p>
              <p class="mb-1">
                {{ property.attributeValue || t('Ontbreekt') }}
              </p>
            </div>
          </div>
        </div>
      </div>

    </ClientOnly>

  </Page>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Page from '@/components/PageWrapper.vue'
import algoritmeService from '@/services/algoritme'
import { summaryTiles } from '~~/config/config'
import { useI18n } from 'vue-i18n'
import type { Algoritme } from '~~/types/algoritme'
import requiredFields from '~~/config/fields.json'

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

const { t } = useI18n()
const shortDescription = computed(() => t('short-description'))
const shortDescriptionMissing = computed(() => t('short-description-missing'))

let activeAttributeKey = ref('')
const activeAttributeProperties = computed(() => {
  return structuredProperties.value.filter((groupedProperty) => {
    return groupedProperty.attributeGroupKey == activeAttributeKey.value
  })[0]?.properties
})

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

onMounted(() => activeAttributeKey = ref(structuredProperties.value[0].attributeGroupKey))
</script>

<style scoped lang="scss">
// These are similar styles to '.tabs__list a' options from _koop_main.scss
.tabs__list span {
  display: inline-block;
  text-align: center;
  padding: 0.5em 0.75em;
  background: #fff;
  text-decoration: none;
  position: relative;
  border-top: 2px solid transparent;
  cursor: pointer;
}

.tabs__list span:hover {
  color: #154273;
  background-color: #f3f3f3;
}

.tabs__list span.is-selected,
.tabs__list span[aria-selected='true'] {
  border-left: 1px solid #e6e6e6;
  border-right: 1px solid #e6e6e6;
  border-top: 2px solid #154273;
  border-bottom-color: #fff;
  bottom: -1px;
}

.tabs__list span.is-selected:hover,
.tabs__list span[aria-selected='true']:hover {
  background-color: #fff;
}
</style>
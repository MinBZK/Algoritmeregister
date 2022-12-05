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
          <p>{{ algoritme.description_short || shortDescriptionMissing }}</p>
          <!-- <p>
            <a href="#" class="link link--forward">Alle datasets van deze eigenaar</a>
          </p> -->
          <dl class="dl columns--data">
            <div v-for="sT in summaryTiles">
              <dt>
                {{ $t(`algorithmProperties.algemeneInformatie.${sT}.label`) }}
              </dt>
              <dd class="word-break">
                <span>{{
                  algoritme[sT as keyof typeof algoritme] || t('Ontbreekt')
                }}</span>
              </dd>
            </div>
          </dl>
        </div>
        <div v-if="smAndDown" class="accordion" data-decorator="init-accordion">
          <div
            v-for="(p, index) in structuredProperties"
            class="accordion__item"
          >
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
                {{ property.attributeKeyLabel }}
                <span
                  @click="toggleKey(property.attributeKey)"
                  class="bg-image"
                ></span>
              </div>
              <div
                class="word-break"
                v-if="isKeyToggled(property.attributeKey)"
              >
                <i
                  >{{
                    `Uitleg: ${
                      property.attributeKeyDescription || t('Ontbreekt')
                    }`
                  }}
                </i>
              </div>
              <div
                class="word-break"
                v-if="!isKeyToggled(property.attributeKey)"
              >
                {{ property.attributeValue || t('Ontbreekt') }}
              </div>
            </div>
          </div>
        </div>

        <div v-if="!smAndDown" class="tabs" data-decorator="init-tabs">
          <ul class="tabs__list" role="tablist">
            <li role="presentation" v-for="(p, index) in structuredProperties">
              <span
                @click="activeAttributeKey = p.attributeGroupKey"
                :class="[
                  p.attributeGroupKey == activeAttributeKey
                    ? 'is-selected'
                    : '',
                ]"
                role="tab"
                :aria-controls="`panel-${index + 1}`"
                >{{ p.attributeGroupKeyLabel }}</span
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
                    class="bg-image"
                  ></span>
                </th>
                <td v-if="!isKeyToggled(property.attributeKey)">
                  {{ property.attributeValue || t('Ontbreekt') }}
                </td>
                <td v-if="isKeyToggled(property.attributeKey)">
                  <i>
                    {{
                      `Uitleg: ${
                        property.attributeKeyDescription || t('Ontbreekt')
                      }`
                    }}
                  </i>
                </td>
              </tr>
            </tbody>
          </table>
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
import { useDisplay } from 'vuetify'

const { smAndDown } = useDisplay()

// get data
const route = useRoute()
const id = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id

const { data } = await algoritmeService.getOne(id)
let algoritme = ref(data.value as Algoritme)

function ping() {
  console.log('ping!')
}
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

const swapInfo = ref(false)

const { t } = useI18n()
const shortDescription = computed(() => t('short-description'))
const shortDescriptionMissing = computed(() => t('short-description-missing'))

let activeAttributeKey = ref('')
const activeAttributeProperties = computed(() => {
  return structuredProperties.value.filter((groupedProperty) => {
    return groupedProperty.attributeGroupKey == activeAttributeKey.value
  })[0]?.properties
})

function toggleAccordion(key: string) {
  if (activeAttributeKey.value == key) {
    activeAttributeKey.value = ''
  } else {
    activeAttributeKey.value = key
  }
}

let keyToggles = ref([''])
function toggleKey(key: string) {
  if (keyToggles.value.includes(key)) {
    keyToggles.value = keyToggles.value.filter((e: any) => e !== key)
  } else {
    keyToggles.value.push(key)
  }
}

function isKeyToggled(key: string) {
  return keyToggles.value.includes(key)
}

function clearToggledKeys() {
  keyToggles.value = ['']
}

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

onMounted(() => {
  if (!smAndDown) {
    activeAttributeKey = ref(structuredProperties.value[0].attributeGroupKey)
  }
})

watch(smAndDown, (newValue, oldValue) => {
  if (newValue == true) {
    activeAttributeKey.value = ''
  } else {
    activeAttributeKey = ref(structuredProperties.value[0].attributeGroupKey)
  }
})
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
.accordion__item__header {
  cursor: pointer;
}
.word-break {
  // word-break: break-all;
  word-break: break-word;
}
</style>

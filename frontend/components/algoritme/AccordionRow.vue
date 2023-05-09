<template>
  <div class="accordion__item">
    <div class="accordion__item__header">
      <h2 class="accordion__item__heading">
        <span
          class="accordion__item__header-trigger"
          :aria-expanded="expanded ? 'true' : 'false'"
          tabindex="0"
          role="button"
          @keydown.enter="toggleTab()"
          @keydown.space.prevent="toggleTab()"
          @click="toggleTab()"
        >
          <span
            :class="expanded ? 'accordion-arrow-up' : 'accordion-arrow-right'"
          ></span>
          {{ t(`algorithmProperties.${groupProps.groupKey}.label`) }}
        </span>
      </h2>
    </div>
    <div v-if="expanded">
      <div
        v-for="property in groupProps.properties"
        :key="property.key"
        class="accordion__item__content"
        aria-labelledby="header1"
      >
        <div>
          <h2>
            {{ property.keyLabel }}
            <span
              class="question-mark"
              role="button"
              :title="
                t('getAlgorithmPropertyExplanation', {
                  field: property.keyLabel.toLowerCase(),
                })
              "
              tabindex="0"
              :aria-expanded="isKeyToggled(property.key) ? 'true' : 'false'"
              @click="toggleKey(property.key)"
              @keydown.enter="toggleKey(property.key)"
              @keydown.space="
                (e) => [e.preventDefault(), toggleKey(property.key)]
              "
            ></span>
          </h2>
        </div>
        <div v-if="isKeyToggled(property.key)" class="word-break">
          <i>
            <ParseUrl :key="property.keyDescription">
              {{ property.keyDescription }}
            </ParseUrl>
          </i>
        </div>
        <div class="word-break">
          <ParseUrl :key="property.value || t('ontbreekt')">
            {{ property.value || t('ontbreekt') }}
          </ParseUrl>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { changeHash } from '~~/utils'

interface Property {
  key: string
  value: string
  keyDescription: string
  keyLabel: string
}

interface Props {
  groupProps: {
    groupKey: string
    properties: Property[]
  }
}
const { t } = useI18n()

const props = defineProps<Props>()

const expandedTab = useState<string | undefined>('expandedTab', () => undefined)

// Handle accordion
const resetScroll = async () => {
  const header = document.getElementById(`header-${props.groupProps.groupKey}`)
  const storePosition = header?.getBoundingClientRect().y || 0
  await nextTick()
  if (header) window.scrollTo(0, header.offsetTop - storePosition)
}

const toggleTab = () => {
  if (expandedTab.value === props.groupProps.groupKey) {
    expandedTab.value = undefined
  } else {
    expandedTab.value = props.groupProps.groupKey
  }
  changeHash(expandedTab.value)
  resetScroll()
}

const expanded = computed(() => expandedTab.value === props.groupProps.groupKey)

const keyToggles = ref<string[]>([])
const toggleKey = (key: string) => {
  if (keyToggles.value.includes(key)) {
    keyToggles.value = keyToggles.value.filter((e: any) => e !== key)
  } else {
    keyToggles.value.push(key)
  }
}
const isKeyToggled = (key: string) => keyToggles.value.includes(key)
</script>

<style scoped langs="scss">
.accordion__item__header {
  cursor: pointer;
}
.word-break {
  word-break: break-word;
}
.question-mark {
  padding-left: 0;
}
h2 {
  font-size: 1.125em !important;
}
.accordion__item__heading {
  font-size: 1em !important;
}
</style>

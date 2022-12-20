<template>
  <div :id="`header-${groupProps.groupKey}`" class="accordion__item">
    <div class="accordion__item__header">
      <h3 class="accordion__item__heading">
        <span
          class="accordion__item__header-trigger"
          aria-expanded="false"
          @click=";[toggleAccordion(), clearToggledKeys()]"
        >
          <span
            :class="toggled ? 'accordion-arrow-up' : 'accordion-arrow-right'"
          ></span>
          {{ groupProps.groupKeyLabel }}
        </span>
      </h3>
    </div>
    <div v-if="toggled">
      <div
        v-for="property in groupProps.properties"
        :key="property.key"
        class="accordion__item__content"
        role="region"
        aria-labelledby="header1"
      >
        <div>
          <b>
            {{ property.keyLabel }}
          </b>
          <span class="question-mark" @click="toggleKey(property.key)"></span>
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
import { useI18n } from 'vue-i18n'
export interface Props {
  groupProps: {
    groupKey: string
    groupKeyLabel: string
    properties: {
      key: string
      value: string
      keyDescription: string
      keyLabel: string
    }[]
  }
  toggled?: boolean
}
const { t } = useI18n()

const props = withDefaults(defineProps<Props>(), {
  toggled: false,
})
const emit = defineEmits<{
  (e: 'toggleThisRow'): void
}>()

// Handle accordion
const toggleAccordion = async () => {
  const header = document.getElementById(`header-${props.groupProps.groupKey}`)
  const storePosition = header?.getBoundingClientRect().y || 0

  emit('toggleThisRow')

  await new Promise((resolve) => setTimeout(resolve, 1)).then(() => {
    if (header) {
      window.scrollTo(0, header.offsetTop - storePosition)
    }
  })
}

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
</script>

<style langs="scss">
.accordion__item__header {
  cursor: pointer;
}
.word-break {
  word-break: break-word;
}
.question-mark {
  padding-left: 0;
}
</style>

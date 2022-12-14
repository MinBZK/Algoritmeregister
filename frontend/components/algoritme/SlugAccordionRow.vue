<template>
  <div :id="`header-${groupProps.attributeGroupKey}`" class="accordion__item">
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
          {{ groupProps.attributeGroupKeyLabel }}
        </span>
      </h3>
    </div>
    <div v-if="toggled">
      <div
        v-for="property in groupProps.properties"
        :key="property.attributeKey"
        class="accordion__item__content"
        role="region"
        aria-labelledby="header1"
      >
        <div>
          <b>
            {{ property.attributeKeyLabel }}
          </b>
          <span
            class="question-mark"
            @click="toggleKey(property.attributeKey)"
          ></span>
        </div>
        <div v-if="isKeyToggled(property.attributeKey)" class="word-break">
          <i>
            <ParseUrl>
              {{ `${property.attributeKeyDescription || t('ontbreekt')}` }}
            </ParseUrl>
          </i>
        </div>
        <div class="word-break">
          <ParseUrl>
            {{ property.attributeValue || t('Ontbreekt') }}
          </ParseUrl>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface Props {
  groupProps: {
    attributeGroupKey: string
    attributeGroupKeyLabel: string
    properties: {
      attributeKey: string
      attributeValue: string
      attributeKeyDescription: string
      attributeKeyLabel: string
    }[]
  }
  toggled?: boolean
}
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const props = withDefaults(defineProps<Props>(), {
  toggled: false,
})
const emit = defineEmits<{
  (e: 'toggleThisRow'): void
}>()

// Handle accordion
const toggleAccordion = async () => {
  const header = document.getElementById(
    `header-${props.groupProps.attributeGroupKey}`
  )
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

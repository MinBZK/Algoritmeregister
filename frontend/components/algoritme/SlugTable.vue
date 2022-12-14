<template>
  <table class="table__data-overview">
    <tbody>
      <tr v-for="property in tableProperties" :key="property.attributeKey">
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
                {{ `${property.attributeKeyDescription || t('Ontbreekt')}` }}
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
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const props = defineProps<{
  tableProperties: {
    attributeKey: string
    attributeValue: string
    attributeKeyDescription: string
    attributeKeyLabel: string
  }[]
}>()

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
</script>

<style lang="scss">
.question-mark {
  padding-left: 0;
}
</style>

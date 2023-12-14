<template>
  <table class="table__data-overview">
    <tbody>
      <tr v-for="property in tableProperties" :key="property.key">
        <th scope="row">
          <div class="space-for-question-mark">
            {{ property.keyLabel }}
            <span
              class="question-mark"
              role="button"
              tabindex="0"
              :aria-expanded="isKeyToggled(property.key) ? 'true' : 'false'"
              :title="
                t('getAlgorithmPropertyExplanation', {
                  field: property.keyLabel.toLowerCase(),
                })
              "
              @click="toggleKey(property.key)"
              @keydown.enter="toggleKey(property.key)"
            ></span>
            <p v-if="isKeyToggled(property.key)">
              <i>
                <ParseUrl :key="property.keyDescription">
                  {{ property.keyDescription }}
                </ParseUrl>
              </i>
            </p>
          </div>
        </th>

        <td :lang="backendContentLanguage">
          <ParseUrl :key="property.value || t('ontbreekt')">
            <ListifyString
              list-style="padding-left: 1em;"
              :text="property.value || t('ontbreekt')"
            />
          </ParseUrl>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import { backendContentLanguage } from '@/config/config'

defineProps<{
  tableProperties: {
    key: string
    value: string
    keyDescription: string
    keyLabel: string
  }[]
}>()

const { t } = useI18n()
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
</script>

<style lang="scss">
.question-mark {
  padding-left: 0;
}
.space-for-question-mark {
  padding-right: 1em !important;
}
</style>

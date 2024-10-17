<template>
  <table class="table__data-overview">
    <tbody>
      <tr
        v-for="property in tableProperties"
        :key="property.key"
        class="row-styling"
      >
        <th scope="row">
          <div>
            {{ property.keyLabel }}
            <div class="float-right">
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
            </div>
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
              :list-style="true"
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

<style scoped lang="scss">
.question-mark {
  padding-left: 0;
}
.row-styling {
  th {
    width: 35%;
  }
}
.float-right {
  float: right;
}
</style>

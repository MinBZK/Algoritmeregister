<template>
  <div class="bar">
    <b class="highlight-text">
      {{ t('home-highlight-algorithm-text') }}
    </b>
    <div class="bottom-margin"></div>
    <ul class="bar__list">
      <li v-for="algo in selectedAlgorithms" class="bar__list__item">
        <p class="bar__list__item-icon">
          <NuxtIcon
            size="0.8em"
            name="material-symbols:arrow-forward-ios-rounded"
          />&nbsp;
          <a :href="`/algoritme/${algo.id}`" class="link"
            >{{ algo.name || '' }} | {{ algo.organization || '' }}</a
          >
        </p>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import algoritmeService from '@/services/algoritme'
import { AlgNameIdOrg } from '~~/types/algoritme'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const { data } = await algoritmeService.getNameIdOrg()
let nameList = ref(data.value as AlgNameIdOrg[])

const selectedAlgorithmIds = ['32', '25', '1']

const selectedAlgorithms = computed(() => {
  return selectedAlgorithmIds.map((id) => {
    const alg = nameList.value.find((alg) => alg.id == id) || {
      id: null,
      name: null,
      organization: null,
    }
    return alg
  })
})
</script>
<style lang="scss">
.bottom-margin {
  padding-bottom: 15px;
}
</style>
